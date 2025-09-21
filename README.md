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

## Table of Contents
- [Simulation of fork dynamics](#simulation-of-fork-dynamics)
- [Simulation of two replication forks](#simulation-of-two-replication-forks)
- [Algorithm flowcharts](#algorithm-flowcharts)
- [Citation](#citation)

---

## Simulation of Fork Dynamics
<p align="center">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/simulations3.gif" width="400"/>
</p>

<p align="center">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/simulations2.png" width="90%"/>
</p>

<div style="display: flex; justify-content: center; gap: 20px;">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/alg.png" width="800" align="center" />
</div>

> [!NOTE]  
> The **rescaled analysis** highlights fork dynamics across different chromatin contexts.  
> The green rectangles represent coverage regions in rescaled fountains.

---

## Simulation of Two Replication Forks
<p align="center">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/simulations5.png" alt="Two forks" width="400" align="left" />
</p>

This animation demonstrates the dynamics of two replication forks:

- **Left panel**: progressive fork movement over time  
- **Right panel**: representative frame snapshot  

<br clear="left"/>

<p align="center">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/simulations_two_ori.svg" width="800" align="center" />
</p>

> [!WARNING]  
> Fork collisions or stalling events may emerge under replication stress,  
> which can be further explored in extended simulations.

---

## Algorithm Flowcharts
<p align="center">
  <img src="https://github.com/zzdzr/ForkSimulation/blob/main/img/alg2.png" width="800"/>
</p>

---

## Citation
If you are using this code, please cite:

```bibtex
@article{forksimulation2025,
  title={Simulation of replication fork dynamics under chromatin constraints},
  author={Your Name and Collaborators},
  journal={Preprint},
  year={2025}
}
