import numpy as np
import pandas as pd
import h5py
import json
from typing import Dict
import os

class Fork:
    def __init__(self, pos: int, attrs: Dict[str, bool] = None) -> None:
        self.pos = pos
        self.attrs = attrs or {'terminated': False, 'direction': 'upstream', 'decoupled_p': None}
        self.direction = -1 if self.attrs['direction'] == 'upstream' else 1
        self.speed = 1

    def move(self, termination_sites: np.ndarray, barrier_sites: np.ndarray, N: int) -> str:
        step = self.speed * self.direction
        new_pos = self.pos + step
        crossed_barrier = None
        if new_pos < 0 or new_pos >= N:
            self.attrs['terminated'] = True
            return 'terminated', crossed_barrier
        if (self.direction == -1 and new_pos <= np.min(termination_sites)) or \
           (self.direction == 1 and new_pos >= np.max(termination_sites)):
            self.attrs['terminated'] = True
            return 'terminated', crossed_barrier
        for barrier in barrier_sites:
            if (self.pos - barrier) * (new_pos - barrier) <= 0:
                crossed_barrier = True
        self.pos = new_pos
        return 'moved', crossed_barrier

    def is_terminated(self) -> bool:
        return self.attrs['terminated']


class RepFactory:
    def __init__(self, left_fork: Fork, right_fork: Fork) -> None:
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.coupled_state = 1

    def update_speed(self, k: float, sigma_c: float = 0, add_noise: bool = False):
        if self.coupled_state != 1:
            return
        dW_c = np.random.normal(0, 0.1) if add_noise else 0
        dt = 1
        v_l, v_r = self.left_fork.speed, self.right_fork.speed
        v_l = v_l if v_l > 0 else 1
        v_r = v_r if v_r > 0 else 1
        v_l += -k * (v_l - v_r) * dt + (sigma_c * dW_c if add_noise else 0)
        v_r += -k * (v_r - v_l) * dt + (sigma_c * dW_c if add_noise else 0)
        self.left_fork.speed = max(v_l, 0)
        self.right_fork.speed = max(v_r, 0)

    def update_coupled_state(self, alpha: float, p_fixed: float, time: int):
        p_11 = np.exp(-alpha * time)
        p_10 = 1 - p_11
        p_01 = p_fixed
        p_00 = 1 - p_fixed
        P = np.array([[p_01, p_00],
                      [p_11, p_10]])
        self.coupled_state = np.random.choice([1, 0], p=P[self.coupled_state])


class BarrierTerminationManager:
    def __init__(self, args: Dict):
        self.N = args['N']
        self.termCenters = args['termCenters']
        self.termStd = args['termStd']
        self.barrier_centers = args.get('barrier_centers', [300, 700])
        self.barrier_std = args.get('barrier_std', 10)

    def set_termination_sites(self) -> np.ndarray:
        sites = np.random.normal(loc=self.termCenters, scale=self.termStd).astype(int)
        return np.clip(sites, 0, self.N - 1)

    def set_barrier_site(self) -> np.ndarray:
        center = np.random.choice(self.barrier_centers)
        site = int(np.random.normal(center, self.barrier_std))
        return np.array([np.clip(site, 0, self.N - 1)])


class SingleMoleculeSimulator:
    def __init__(self, args: Dict) -> None:
        self.args = args
        self.trajectories_data = []
        self.barrier_term_manager = BarrierTerminationManager(args)

    def simulate_one_factory(self, sim_id: int) -> Dict:
        load_start = self.args['loadStart']
        load_end = self.args['loadEnd']
        norm_scale = self.args['norm_scale']
        time_ = self.args['time']
        decoupled_p = self.args['decoupled_p']

        loc = int(np.random.normal(loc=(load_start + load_end) // 2, scale=norm_scale))
        left_fork = Fork(pos=loc, attrs={'direction': 'upstream', 'terminated': False, 'decoupled_p': decoupled_p})
        right_fork = Fork(pos=loc + 1, attrs={'direction': 'downstream', 'terminated': False, 'decoupled_p': decoupled_p})
        left_fork.speed = self.args['speed_left']
        right_fork.speed = self.args['speed_right']
        factory = RepFactory(left_fork, right_fork)

        termination_sites = self.barrier_term_manager.set_termination_sites()
        barrier_sites = self.barrier_term_manager.set_barrier_site()

        path_data = []
        coupled_states_data = []

        while factory.coupled_state != 0:
            path_data.append((factory.left_fork.pos, factory.right_fork.pos))
            coupled_states_data.append(factory.coupled_state)
            for fork in [factory.left_fork, factory.right_fork]:
                status, crossed_barrier = fork.move(termination_sites, barrier_sites, self.args['N'])
                if status == 'terminated':
                    factory.coupled_state = 0
                    path_data.append((factory.left_fork.pos, factory.right_fork.pos))
                    coupled_states_data.append(0)
                    break
                if crossed_barrier and np.random.rand() < fork.attrs['decoupled_p']:
                    factory.coupled_state = 0
                    path_data.append((factory.left_fork.pos, factory.right_fork.pos))
                    coupled_states_data.append(0)
                    break
            if factory.coupled_state == 0:
                break
            factory.update_speed(k=self.args['k'], sigma_c=self.args['sigma_c'], add_noise=self.args['add_noise'])
            factory.update_coupled_state(alpha=self.args['alpha'], p_fixed=self.args['p_fixed'], time=time_)
            time_ += 1

        return {"trajectory_path": np.array(path_data), "coupled_states": np.array(coupled_states_data)}

    def run_simulations(self, num_simulations: int, output_file: str) -> None:
        for sim_id in range(num_simulations):
            sim_data = self.simulate_one_factory(sim_id)
            self.trajectories_data.append(sim_data)
        self.save_to_hdf5(output_file)

    def save_to_hdf5(self, output_file: str) -> None:
        trajectory_lengths = [len(sim['trajectory_path']) for sim in self.trajectories_data]
        coupled_states_data = [sim['coupled_states'] for sim in self.trajectories_data]
        with h5py.File(output_file, 'w') as myfile:
            total_length = np.nansum(trajectory_lengths)
            dset = myfile.create_dataset("positions",
                                         shape=(total_length, 1, 2),
                                         dtype=np.int32,
                                         compression="gzip")
            start_idx = 0
            for sim_idx, sim in enumerate(self.trajectories_data):
                cur_positions = sim['trajectory_path']
                length = len(cur_positions)
                cur_positions = cur_positions.reshape((length, 1, 2))
                dset[start_idx:start_idx + length, :, :] = cur_positions
                start_idx += length
            myfile.attrs["total_length"] = total_length
            myfile.attrs["FactoryNum"] = 1
            myfile.attrs["total_simulations"] = len(self.trajectories_data)
            myfile.attrs["segments"] = trajectory_lengths
            myfile.attrs['N'] = self.args['N']
            coupled_states_str = [json.dumps(coupled.tolist()) for coupled in coupled_states_data]
            myfile.create_dataset("coupled_states", data=np.array(coupled_states_str, dtype='S'))
        print(f"Simulation results saved to {output_file}")

def run_1d(args, n_sims, output_file):
    simulator = SingleMoleculeSimulator(args)
    simulator.run_simulations(n_sims, output_file)
    return output_file

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
    run_folder = "./test_1d"
    os.makedirs(run_folder, exist_ok=True)
    file_1d = os.path.join(run_folder, "01_simulations.h5")
    run_1d(args, n_sims=10, output_file=file_1d)
