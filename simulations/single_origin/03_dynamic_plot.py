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
    """
    递归遍历 base_dir 目录，找到所有 `blocks_*.h5` 文件。

    Parameters:
    - base_dir: 根目录（results 文件夹）

    Returns:
    - blocks_files: 包含所有 blocks 文件路径的列表
    """
    blocks_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.startswith("blocks_") and file.endswith(".h5"):
                file_path = os.path.join(root, file)
                blocks_files.append(file_path)
    return sorted(blocks_files)


def load_positions(file_path, frame_range):
    """
    从指定的 blocks 文件中提取给定范围的帧数据。

    Parameters:
    - file_path: str, h5 文件路径
    - frame_range: tuple, 提取的帧范围 (start, end)

    Returns:
    - positions: 形状为 (num_frames, num_particles, 3) 的 numpy 数组
    """
    dataset_name = 'pos'

    with h5py.File(file_path, 'r') as f:

        # 获取所有 block 的帧名称，并按顺序排序
        block_names = [str(i) for i in sorted([int(name) for name in f.keys()])]

        # 检查给定的帧范围是否有效
        if frame_range[1] > len(block_names):
            raise ValueError(f"Frame range {frame_range} exceeds available frames in {file_path}")

        # 获取给定范围内的帧名称列表
        selected_blocks = block_names[frame_range[0]:frame_range[1]]

        # 初始化数组并提取所有指定范围内帧的数据
        positions = np.array([f[block_name][dataset_name][:] for block_name in selected_blocks])

    return positions


def compute_contact_matrix(positions, cutoff=6):
    """
    基于提供的分子位置计算接触矩阵 (矢量化计算版本)。

    Parameters:
    - positions: 粒子的空间位置（N, 3）
    - cutoff: 距离的阈值，超过此距离的点将不会形成接触
    """
    # 使用 scipy.spatial.distance_matrix 快速计算两两距离
    dist_matrix = distance_matrix(positions, positions)
    # 构建接触矩阵（使用 numpy 矩阵运算）
    contact_matrix = (dist_matrix < cutoff).astype(int)
    # 去除对角线（因为自己和自己的距离总是 0）
    np.fill_diagonal(contact_matrix, 0)
    return contact_matrix


def process_single_file(file_path, frame_range, cutoff, frame_step=10):
    """
    单文件处理函数：加载文件中的指定帧范围，并生成 contact matrices。

    Parameters:
    - file_path: h5 文件路径
    - frame_step: 每个 contact matrix 使用的帧步长
    - cutoff: 计算接触矩阵时的距离阈值

    Returns:
    - file_contact_matrices: 该文件中的 contact matrices
    """
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
    """
    遍历所有找到的 blocks_*.h5 文件，读取前 frame_step 帧，并堆叠形成 contact matrix。

    Parameters:
    - blocks_files: 所有 blocks 文件列表
    - frame_step: 每个 contact matrix 使用的帧步长
    - cutoff: 计算接触矩阵时的距离阈值

    Returns:
    - all_contact_matrices: (total_frames, num_particles, num_particles) 的 numpy 数组 # total_frames: 所有block file中提取的所有帧的总和; num_particles: N 1000
    """
    all_contact_matrices = []
    # 使用多进程并行处理文件
    with Pool(cpu_count()) as pool:
        # 并行计算每个文件的 contact matrix，并将结果合并
        results = pool.starmap(process_single_file, [(file, frame_range, cutoff) for file in blocks_files]) # 对每个block file进行process_single_file 
        # 对于一个block file，process_single_file返回的结果是len=帧数的list，list中每个元素是一帧的contact matrix，matrix中只有0和1，表示接触/不接触。假设有M帧，返回的是个M长的list
        # 对于block_files遍历一遍，假设有N个block file，results是len为N的list，每个list里有M帧的contact matrix

        
        # 展平
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
            # 处理每个文件
            base_name = os.path.basename(file)
            frame_range = base_name.split('_')[-1].replace('.h5', '')
            start_frame, end_frame = map(int, frame_range.split('-'))
    
            frame_range = (start_frame, end_frame)
            matrices = process_single_file(file, frame_range, cutoff, frame_step=2) # 每10帧再做处理
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
