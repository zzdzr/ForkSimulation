# ForkSimulation

**ForkSimulation** is a coarse-grained molecular dynamics framework to investigate how replication forks propagate and interact with chromatin architecture under replication stress.

---

## Table of Contents
- [Simulation of Fork Dynamics](#simulation-of-fork-dynamics)
- [Simulation of Two Replication Forks](#simulation-of-two-replication-forks)
- [Algorithm Implementation](#algorithm-implementation)
- [Algorithm Flowcharts](#algorithm-flowcharts)

---

## Simulation of Fork Dynamics
<div style="ddisplay: flex; justify-content: center; gap: 20px">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/simulations3.gif" width="400" align="left"/>
  <!-- <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/alg.png" width="400"/> -->
</div>

<p align="center">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/simulations2.png" width="90%" align="center" />
</p>

---

## Algorithm Implementation
<div style="display: flex; justify-content: center; gap: 20px;">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/alg.png" width="800" align="center" />
</div>

> [!NOTE]  
> This diagram illustrates the algorithm used in ForkSimulation.  
> It connects Monte Carlo sampling with fork propagation rules.

---

## Simulation of Two Replication Forks
<p align="center">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/simulations5.png" alt="Two forks" width="400" align="left" />
  This animation demonstrates the dynamics of two replication forks:

- **Left panel**: progressive fork movement over time  
- **Right panel**: representative frame snapshot  
- More details are available in the `docs/` folder  

<br clear="left"/>
</p>

<!-- 保持你原有注释掉的div不动 -->
<!-- <div style="display: flex; justify-content: space-between; align-items: flex-start;">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/simulations5.png" width="400" align="left"/>
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/alg2.png" width="400"/>
</div> -->

<div style="display: flex; justify-content: center; gap: 20px;">
  <!-- <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/alg2.png" width="400"/> -->
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/simulations_two_ori.svg" width="800" align="center" />
</div>

> [!WARNING]  
> Fork collisions and stalling events may occur under replication stress,  
> which can be further investigated in extended simulations.

---

## Algorithm Flowcharts
<div style="display: flex; justify-content: center; gap: 20px;">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/alg2.png" width="800"/>
</div>
