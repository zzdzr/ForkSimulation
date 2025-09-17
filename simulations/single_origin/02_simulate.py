import click
import h5py
import time
import json
import numpy as np

from polychrom.simulation import Simulation
from polychrom.starting_conformations import grow_cubic
from polychrom.hdf5_format import HDF5Reporter
from polychrom import forces
from polychrom import forcekits
from polychrom.simulation import Simulation
from polychrom.starting_conformations import grow_cubic
from polychrom.hdf5_format import HDF5Reporter
from adaptBond import bondUpdater

@click.command()
@click.option(
    "--folder",
    help="Folder to store simulation results",
    type=str
)
@click.option(
    "--myfile",
    help="Input HDF5 file containing LEF positions",
    type=str
)

def run_simulations(folder, myfile):
    """
    Main function to run the polymer simulations. Loads LEF positions from an input file and 
    runs multiple simulations, storing the results in a specified folder.

    Args:
        folder (str): Directory to save simulation results.
        myfile (str): Path to the input HDF5 file with LEF positions and simulation parameters.
    """
    print(f"Running simulation with folder: {folder}, file: {myfile}")

    # Load pre-saved single molecule positions and coupled states
    with h5py.File(myfile, 'r') as f:
        positions = f['positions'][:]
        N = f.attrs['N']
        # coupled states
        coupled_state_str = f['coupled_states']
        coupled_states = [np.array(json.loads(state.decode('utf-8'))) for state in coupled_state_str]
    
        segments = f.attrs["segments"] 
        simInitsTotal = f.attrs["total_simulations"]

    steps = 750  # MD steps per step of cohesin
    dens = 0.1
    box = (N / dens) ** 0.33 * 1.8 # Density = 0.1, this might depend on the size of chromatin, so be cautious # N=1000
    # Initialize polymer configuration using a cubic lattice
    data = grow_cubic(N, int(box) - 2)  # Create a compact conformation 


    # parameters for smc bonds
    smcBondWiggleDist = 0.2 # 
    smcBondDist = 0.5 # 
 
    # # Define how often to save simulation data (every block)
    saveEveryBlocks = 1

    # Initialize bond updater for dynamic bond updates during the simulatio
    milker = bondUpdater(positions=positions) 

    # Open h5py file for storing results
    for sim_count in range(simInitsTotal): 
        milker.index_tracker = 0
        milker.allBonds = []
        milker.allStates = []

        simulation_filename = f"{folder}/simulation_{sim_count + 1}_results.h5" 
        print(f"Creating HDF5 file for simulation {sim_count + 1}: {simulation_filename}")
           
        # calculate max_data_length
        max_data_length = segments[sim_count] // saveEveryBlocks

        # Initialize a new HDF5Reporter for this simulation
        reporter = HDF5Reporter(
            folder=simulation_filename, 
            max_data_length=max_data_length, 
            overwrite=False, 
            blocks_only=False,
            check_exists=False,
        )

        # Create a new simulation instance
        sim = Simulation(
            platform="CUDA",
            integrator="variableLangevin",
            error_tol=0.01,
            collision_rate=0.03,
            N=len(data),
            reporters=[reporter],
            PBCbox=[box,box,box],
            precision="mixed"
        )

        # Set initial polymer data and add forces
        sim.set_data(data)
        sim.add_force(
            forcekits.polymer_chains(
                sim,
                chains=[(0, None, False)],

                # By default the library assumes you have one polymer chain
                # If you want to make it a ring, or more than one chain, use self.setChains
                # self.setChains([(0,50,1),(50,None,0)]) will set a 50-monomer ring and a chain from monomer 50 to the end

                bond_force_func=forces.harmonic_bonds,
                bond_force_kwargs={
                    'bondLength': 1.0,
                    'bondWiggleDistance': 0.1,  # Bond distance will fluctuate +- 0.05 on average
                },

                angle_force_func=forces.angle_force,
                angle_force_kwargs={
                    'k': 1.5
                    # K is more or less arbitrary, k=4 corresponds to presistence length of 4,
                    # k=1.5 is recommended to make polymer realistically flexible; k=8 is very stiff
                },

                nonbonded_force_func=forces.polynomial_repulsive,
                nonbonded_force_kwargs={
                    'trunc': 1.5,  # this will let chains cross sometimes
                    'radiusMult': 1.05,  # this is from old code
                    # 'trunc':10.0, # this will resolve chain crossings and will not let chain cross anymore
                },

                except_bonds=True,

                )
        )

        # Initialize bond parameters
        kbond = sim.kbondScalingFactor / (smcBondWiggleDist ** 2)
        bondDist = smcBondDist * sim.length_scale
        activeParams = {"length": bondDist, "k": kbond}
        inactiveParams = {"length": bondDist, "k": 0}
        milker.setParams(activeParams, inactiveParams)

        # Set up bond updater with bond force and current segment
        milker.setup(
            bondForce=sim.force_dict['harmonic_bonds'], 
            blocks=segments[sim_count],
            coupled_states=coupled_states[sim_count]
        )

        sim.local_energy_minimization() 
        
        # # Run the simulation for each block in the current segment
        save_count = 0
        for i in range(segments[sim_count]):
            if i % saveEveryBlocks == (saveEveryBlocks - 1): 
                # Perform simulation block and save data
                sim.do_block(steps=steps)
            else:
                # Otherwise, continue with the integrator step
                sim.integrator.step(steps)
            
            if i < segments[sim_count] - 1:
                milker.step(sim.context)

        
        data = sim.get_data()
        del sim

        time.sleep(0.1)



if __name__ == '__main__':
    run_simulations()