## Simulation of Fork Dynamics
<img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/simulations3.gif" alt="ForkSimulation" width="400" align="left"/>

This animation demonstrates the dynamics of replication forks under stress:

- **Left panel**: progressive fork movement over time  
- **Right panel**: representative frame snapshot  
- More details are available in the `docs/` folder  

<br clear="left"/>

<!-- --- -->

<p align="center">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/simulations2.png" width="90%" />
</p>


## Simulation of two replication forks
<p align="center">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/simulations5.png" alt="Two forks" width="400" align="left" />
  This animation demonstrates the dynamics of two replication forks:

- **Left panel**: progressive fork movement over time  
- **Right panel**: representative frame snapshot  
- More details are available in the `docs/` folder  

<br clear="left"/>
</p>

<p align="center">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/simulations_two_ori.png" width="90%" align="center" />
</p>

---
## Algorithm Overview (Pseudocode)

```pseudo
Algorithm: Single-Molecule Replication Simulation
Input: Parameters {N, loadStart, loadEnd, speed_left, speed_right, 
                   termCenters, termStd, barrier_centers, barrier_std, 
                   k, sigma_c, alpha, p_fixed, decoupled_p, add_noise}
Output: HDF5 file with fork trajectories and coupled states

1. Initialize BarrierTerminationManager with termination sites & barrier sites

2. For each simulation (sim_id = 1 … num_simulations):
      a. Initialize replication origin at random position near loadStart/loadEnd
      b. Create left fork (upstream) and right fork (downstream)
      c. Assign initial speeds (speed_left, speed_right)
      d. Initialize replication factory (coupled_state = 1)

   3. While coupled_state = 1:
        i.   Record current fork positions
        ii.  For each fork:
                 - Move one step according to speed & direction
                 - If fork hits termination site → terminate
                 - If fork crosses barrier → decouple with probability p
        iii. Update fork speeds by coupling dynamics:
                 v ← v - k * (v_left - v_right) + noise (if add_noise)
        iv.  Update coupled_state by stochastic transition rule:
                 P(coupled → decoupled) = f(alpha, p_fixed, time)
        v.   Increment time

   4. Save trajectory_path and coupled_states for this simulation

5. Aggregate all trajectories and save to HDF5:
      - positions[time, fork_id, pos]
      - coupled_states[time]
      - metadata: total_length, number_of_factories, segments

6. Optionally: Run 3D polymer simulation and dynamic visualization scripts
