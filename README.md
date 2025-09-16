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
## Algorithm 1. Single-Molecule Replication Simulation

**Input:**  
- Polymer length `N`  
- Fork loading region `[loadStart, loadEnd]`  
- Initial fork speeds `(speed_left, speed_right)`  
- Termination distribution `(termCenters, termStd)`  
- Barrier distribution `(barrier_centers, barrier_std)`  
- Coupling parameters `(k, sigma_c, alpha, p_fixed)`  
- Decoupling probability `decoupled_p`  
- Noise flag `add_noise`  

**Output:**  
- Fork trajectories and coupled states stored in HDF5  

---

1. **Initialization**  
   1.1 Sample termination sites from Gaussian(`termCenters`, `termStd`)  
   1.2 Sample a barrier site from Gaussian(`barrier_centers`, `barrier_std`)  
   1.3 Place origin near `(loadStart, loadEnd)`  
   1.4 Initialize left fork (upstream) and right fork (downstream)  
   1.5 Set replication factory with coupled_state = 1  

2. **Simulation loop (while coupled_state = 1):**  
   2.1 Record current fork positions  
   2.2 For each fork:  
   &nbsp;&nbsp;&nbsp;&nbsp;a) Move one step based on speed & direction  
   &nbsp;&nbsp;&nbsp;&nbsp;b) If fork reaches termination → set terminated  
   &nbsp;&nbsp;&nbsp;&nbsp;c) If fork crosses barrier → decouple with probability `decoupled_p`  
   2.3 Update fork speeds by coupling rule:  
   &nbsp;&nbsp;&nbsp;&nbsp;`v ← v - k (v_left - v_right) + noise`  
   2.4 Update coupled_state via Markov transition:  
   &nbsp;&nbsp;&nbsp;&nbsp;`P(coupled → decoupled) = f(alpha, p_fixed, time)`  
   2.5 Increment simulation time  

3. **Output**  
   3.1 Store trajectory path and coupled states for this simulation  
   3.2 Append results to global list  

4. **Finalization**  
   4.1 Write all results into HDF5 with attributes:  
   - `positions[time, fork_id, pos]`  
   - `coupled_states[time]`  
   - Metadata: total_length, number_of_simulations, trajectory_segments  

5. **Optional Post-processing**  
   - Run 3D polymer simulations  
   - Generate dynamic visualizations  
