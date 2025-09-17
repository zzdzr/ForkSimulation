import numpy as np
import polychrom

class bondUpdater:

    def __init__(self, positions: np.ndarray) -> None:
        """
        Initializes the bondUpdater with positions and coupled states of molecules.
        
        Args:
            positions (array): Array of positions for molecules.
            coupled_states (list): List of coupled states for molecules.
        """
        self.positions = positions
        self.curtime = 0
        self.index_tracker = 0
        self.index_direction = 1

        self.allBonds = []
        self.allStates = []

    def setParams(self, activeParamDict: dict, inactiveParamDict: dict) -> None:
        """
        Sets the parameters for active and inactive bonds.
        
        Args:
            activeParamDict (dict): Parameters for active bonds.
            inactiveParamDict (dict): Parameters for inactive bonds.
        """
        self.activeParamDict = activeParamDict
        self.inactiveParamDict = inactiveParamDict
        
    def setup(self, bondForce: polychrom.forces.harmonic_bonds, blocks: int, coupled_states: list) -> None:
        """
        Set up the bonds for the simulation using the bond force and segment blocks.
        
        Args:
            bondForce: Bond force to be used for simulation.
            blocks (int): Number of blocks in the current segment.
        
        Raises:
            ValueError: If there are unused bonds from the previous run.
        """
        import copy

        if len(self.allBonds) != 0:
            raise ValueError("Not all bonds were used; {0} sets left".format(
                len(self.allBonds))
            )
        self.bondForce = bondForce

        # load positions and coupled states
        print("This is {0}".format(self.curtime + blocks))

        loaded_positions = self.positions[self.curtime: self.curtime + blocks]
        loaded_states = coupled_states[:blocks]
        
        # all bonds/states
        allBonds = [[(int(loaded_positions[i, j, 0]), int(loaded_positions[i, j, 1]))
                     for j in range(loaded_positions.shape[1])] for i in range(blocks)]

        # Ensure bonds and states have the same length
        assert len(allBonds) == len(loaded_states), "Mismatch between bonds and states"

        self.allBonds = sum(allBonds, [])
        self.allStates = list(loaded_states)  # These are already lists

        # Assign initial bonds and states
        self.curBonds = self.allBonds[0]
        self.curState = self.allStates[0]
 
        print("AllStates{0}".format(self.allStates))
        print('AllBonds{0}'.format(self.allBonds))

        # indicator for bonds
        self.index = 1

        self.bondToInd = {}
        # Add forces and assign bond parameters based on initial states
        for i, bond in enumerate(self.allBonds):
            is_coupled = (self.allStates[i] == 1)
            # unique indicator
            time_based_key = (i, bond[0], bond[1])
            paramset = self.activeParamDict if ((bond in [self.curBonds]) and (is_coupled)) else self.inactiveParamDict
            ind = bondForce.addBond(bond[0], bond[1], **paramset)
            self.bondToInd[time_based_key] = ind
        
        self.allBonds.pop(0)
        self.allStates.pop(0)
        self.curtime += blocks 
        print("--------------bondInds{0}--------------".format(self.bondToInd))
        
    def step(self, context, verbose: bool = False) -> None:
        """
        Update bonds dynamically in the simulation context.
        
        Args:
            context (SimulationContext): Simulation context.
            verbose (bool): Whether to print verbose output (default: False).
        
        Raises:
            ValueError: If no bonds are left to update.
        """
        if len(self.allBonds) == 0:
            raise ValueError("No bonds left to run; you should restart simulation and run setup again")
        
        # pastBonds = [self.curBonds]
        # self.curBonds = [allBonds.pop(0)]

        # pastState = [self.curState]
        # self.curState = [allStates.pop(0)]

        pastBonds = [self.curBonds] if self.index_tracker==0 else self.curBonds
        pastState = self.curState

        self.curBonds = [self.allBonds.pop(0)]
        self.curState = self.allStates.pop(0)

        print('Current bonds are {0}'.format(self.curBonds))
        print('Past Bonds are {0}'.format(pastBonds))
        print('Current state are {0}'.format(self.curState))

        bondsRemove = [i for i in pastBonds if i not in self.curBonds] #  [(477, 555)]
        bondsAdd = [i for i in self.curBonds if i not in pastBonds] # [(475, 557)]
        bondsStay = [i for i in pastBonds if i in self.curBonds]

        if self.curBonds == pastBonds:
            bondsRemove = self.curBonds
            bondsAdd = self.curBonds

        bondsToChange = bondsAdd + bondsRemove
        bondsIsAdd = [True] * len(bondsAdd) + [False] * len(bondsRemove)

        bondsIsCoupled = [self.curState==1] * len(bondsAdd) + [False] * len(bondsRemove)
        print('bondsIsCoupled!!!!!!!{0}'.format(bondsIsCoupled))
        print('bondsToAdd!!!!!!{0}'.format(bondsAdd))
        print('bondsToRemove!!!!!!{0}'.format(bondsRemove))
        # Update bond parameters based on coupling and addition/removal state
        for bond, isAdd, isCoupled in zip(bondsToChange, bondsIsAdd, bondsIsCoupled):

            time_based_key = (self.index, bond[0], bond[1])
            print('time-key is {0}'.format(time_based_key))
            print("Add is {0}".format(isAdd))
            print('Bond is {0}'.format(bond))
            ind = self.bondToInd.get(time_based_key)

            print("Ind is {0}".format(ind))
            paramset = self.activeParamDict if (isAdd and isCoupled) else self.inactiveParamDict
            print("paramset is {0}".format(paramset))
            self.bondForce.setBondParameters(ind, bond[0], bond[1], **paramset)

            # Update self.index following the pattern: (1, 0, 2, 1, 3, 2, 4, 3, 5, 4, ...)
            if self.index_direction == -1:
                self.index += 2
                self.index_direction = 1
            else:
                self.index -= 1
                self.index_direction = -1
            
            self.index_tracker += 1

        # Apply updated bond parameters in the simulation context
        self.bondForce.updateParametersInContext(context)
        