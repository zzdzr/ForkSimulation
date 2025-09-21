<h1>
<p align="center">
    <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/simulations3.gif" alt="ForkSimulation logo" width="300"/>
</p>
</h1>

<p align="center">
  <a href="https://doi.org/10.1101/2025.01.01.000000">
    <img src="https://zenodo.org/badge/DOI/10.1101/2025.01.01.000000.svg" alt="DOI"/>
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white" alt="Python 3.10+"/>
  </a>
  <a href="https://github.com/zzdzr/ForkSimulation/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/zzdzr/ForkSimulation" alt="License"/>
  </a>
  <a href="https://github.com/zzdzr/ForkSimulation/releases">
    <img src="https://img.shields.io/github/v/release/zzdzr/ForkSimulation?color=green&label=release" alt="GitHub release"/>
  </a>
</p>

# ForkSimulation

**ForkSimulation** is a coarse-grained molecular dynamics framework to investigate how replication forks propagate and interact with chromatin architecture under replication stress.

---

## Simulation of Fork Dynamics
<div style="ddisplay: flex; justify-content: center; gap: 20px">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/simulations3.gif" width="400" align="left"/>
  <!-- <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/alg.png" width="400"/> -->
</div>

<p align="center">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/simulations2.png" width="90%" align="center" />
</p>

<div style="display: flex; justify-content: center; gap: 20px;">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/alg.png" width="800" align="center" />
</div>

> [!NOTE]  
> The green rectangles indicate rescaled type-II fountain coverage regions.  
> Replication timing is represented by the S50 profile (NT, HU, APH).

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

---

