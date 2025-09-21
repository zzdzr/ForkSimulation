# ForkSimulation

**ForkSimulation** is a coarse-grained molecular dynamics framework to investigate the spatial organizations of coupled replication forks.  

> [!NOTE]  
> The code of this project is continuously updating.

---

## Table of Contents
- [:movie_camera: Simulation of Fork Dynamics](#movie_camera-simulation-of-fork-dynamics)
- [:movie_camera: Simulation of Two Replication Forks](#movie_camera-simulation-of-two-replication-forks)
- [:gear: Algorithm1 Implementation](#gear-algorithm1-implementation)
- [:gear: Algorithm2 Flowcharts](#gear-algorithm2-flowcharts)

---

## :movie_camera: Simulation of Fork Dynamics

<div style="display: flex; align-items: center; gap: 20px;">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/simulations3.gif" width="400" align="left"/>
  <p>
    <b>Perform 100 independent simulations</b>, each corresponding to a single-molecule dynamics trajectory.<br><br>
    This demonstrates the stochastic behavior of replication forks under identical initial conditions.
  </p>
</div>

<p align="center">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/simulations2.png" width="90%" />
</p>

For each frame in time, the states of all 100 simulations were averaged  
to obtain the <b>ensemble behavior</b>, representing the collective trend of fork dynamics  
rather than individual stochastic fluctuations.

---

## :movie_camera: Simulation of Two Replication Forks

<div style="display: flex; align-items: center; gap: 20px;">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/simulations5.png" alt="Two forks" width="400" align="left"/>
  <p>
    This animation demonstrates the dynamics of two replication forks:<br><br>
    • <b>Left panel</b>: progressive fork movement over time <br>
    • <b>Right panel</b>: representative frame snapshot <br>
    • More details are available in the <code>docs/</code> folder
  </p>
</div>

---

## :gear: Algorithm1 Implementation

<p align="center">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/alg.png" width="800" />
</p>

> [!NOTE]  
> This diagram illustrates the first algorithm implemented in ForkSimulation.  
> The code is continuously being updated.

---

## :gear: Algorithm2 Flowcharts

<p align="center">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/alg2.png" width="800"/>
</p>

> [!TIP]  
> This diagram shows the second algorithmic workflow for fork dynamics simulation.
