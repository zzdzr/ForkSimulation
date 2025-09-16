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

**Input:** Polymer length `N`, fork loading region `[loadStart, loadEnd]`,  
initial speeds `(v_l, v_r)`, termination distribution, barrier distribution,  
coupling parameters `(k, σ_c, α, p_fixed)`, decoupling probability, noise flag  

**Output:** Fork trajectories and coupled states (HDF5)

---

1. **Initialization**  
   - Sample termination sites and barrier site from Gaussian distributions  
   - Place replication origin between `[loadStart, loadEnd]`  
   - Initialize left/right forks with speeds `(v_l, v_r)`  
   - Set `coupled_state = 1`  

2. **While `coupled_state = 1`:**  
   a. Record fork positions  
   b. For each fork:  
      - Move one step according to speed & direction  
      - If termination reached → terminate  
      - If barrier crossed → decouple with probability `p_decouple`  
   c. Update fork speeds by coupling rule:  
      $v \gets v - k(v_l - v_r) + \sigma_c \xi$  
   d. Update coupled state with transition probability:  
      $P(1 \to 0) = f(\alpha, p_{fixed}, t)$  
   e. Increment time  

3. **Finalize**  
   - Save trajectory path and coupled states for each simulation  
   - Aggregate all simulations and export to HDF5
