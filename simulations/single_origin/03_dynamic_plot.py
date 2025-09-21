import os
import click
import h5py
import numpy as np
from scipy.spatial import distance_matrix
from multiprocessing import Pool, cpu_count
import matplotlib.pyplot as plt
import click

@click.command()
@click.option("--base_dir", type=str, help="Folder with store simulation results")
def find_all_blocks_files(base_dir):

    blocks_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.startswith("blocks_") and file.endswith(".h5"):
                file_path = os.path.join(root, file)
                blocks_files.append(file_path)
    return sorted(blocks_files)


def load_positions(file_path, frame_range):

    dataset_name = 'pos'

    with h5py.File(file_path, 'r') as f:

        block_names = [str(i) for i in sorted([int(name) for name in f.keys()])]

        if frame_range[1] > len(block_names):
            raise ValueError(f"Frame range {frame_range} exceeds available frames in {file_path}")

        selected_blocks = block_names[frame_range[0]:frame_range[1]]

        positions = np.array([f[block_name][dataset_name][:] for block_name in selected_blocks])

    return positions


def compute_contact_matrix(positions, cutoff=6):

    dist_matrix = distance_matrix(positions, positions)
    contact_matrix = (dist_matrix < cutoff).astype(int)
    np.fill_diagonal(contact_matrix, 0)
    return contact_matrix


def process_single_file(file_path, frame_range, cutoff, frame_step=10):

    try:
        print(f"Processing {file_path} ...")
        positions = load_positions(file_path, frame_range)
        file_contact_matrices = []

        for frame_idx in range(0, positions.shape[0], frame_step):
            file_contact_matrices.append(compute_contact_matrix(positions[frame_idx], cutoff=cutoff))

        return file_contact_matrices
    except (KeyError, ValueError) as e:
        print(f"Error processing file {file_path}: {e}")
        return []


def pileup_contact_matrices(blocks_files, frame_range, cutoff=6):

    all_contact_matrices = []
    with Pool(cpu_count()) as pool:

        results = pool.starmap(process_single_file, [(file, frame_range, cutoff) for file in blocks_files]) 

        for matrices in results:
            all_contact_matrices.extend(matrices)

    return np.array(all_contact_matrices)

@click.command()
@click.option(
    "--base_dir",
    help="Folder with store simulation results",
    type=str
)

def plot(base_dir, cutoff=6):
    blocks_files = find_all_blocks_files(base_dir)
    contact_matrices = []

    for file in blocks_files:
        try:

            base_name = os.path.basename(file)
            frame_range = base_name.split('_')[-1].replace('.h5', '')
            start_frame, end_frame = map(int, frame_range.split('-'))
    
            frame_range = (start_frame, end_frame)
            matrices = process_single_file(file, frame_range, cutoff, frame_step=2) 
            contact_matrices.extend(matrices)
        except Exception as e:
            print(f"{file} error: {e}")
    print(f"contact matrix length: {len(contact_matrices)}")
    contact_matrices_mean = np.nanmean(contact_matrices, axis=0)
    fig, ax = plt.subplots(figsize=(5, 5), dpi=250)
    ax.imshow(contact_matrices_mean,  vmax=.05, vmin=0, cmap='OrRd')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.savefig(f"{base_dir}/contactmap.png")


if __name__ == "__main__":
    plot()
