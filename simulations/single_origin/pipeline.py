import os
import numpy as np
from stable_block import run_1d
from simulate import run_simulations
from dynamic_plot import plot

def run_full_pipeline(args, n_sims=500, base_dir="./results"):
    # Step 1: 1D simulation
    os.makedirs(base_dir, exist_ok=True)
    file_1d = os.path.join(base_dir, "01_simulations.h5")
    run_1d(args, n_sims, file_1d)

    # Step 2: 3D simulation
    folder_3d = os.path.join(base_dir, "3D_results")
    os.makedirs(folder_3d, exist_ok=True)
    run_simulations(folder=folder_3d, myfile=file_1d)

    # Step 3: contact map
    plot(folder_3d)

if __name__ == "__main__":
    args = {
        'N': 1000,
        'loadStart': 500,
        'loadEnd': 501,
        'norm_scale': 15,
        'speed_left': 1,
        'speed_right': 1,
        'termCenters': np.array([100, 900]),
        'termStd': 50,
        'barrier_centers': [650],
        'barrier_std': 40,
        'k': 0.5,
        'sigma_c': 0.05,
        'sigma_A': 0.2,
        'sigma_B': 0.2,
        'alpha': 4e-5,
        'time': 0,
        'p_fixed': 1e-10,
        'decoupled_p': 0.3,
        'add_noise': True
    }
    run_full_pipeline(args, n_sims=50, base_dir="./pipeline_test")
