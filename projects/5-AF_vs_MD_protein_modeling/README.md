# AlphaFold vs Molecular Dynamics: Exploring Protein Structure and Flexibility

## Overview

This tutorial introduces you to the relationship between **protein structure prediction** and **molecular dynamics (MD) simulations**.  

Modern tools such as **AlphaFold** can predict highly accurate protein structures from sequence. However, proteins are **dynamic molecules**, and their behavior in solution may differ from a single predicted structure.

In this tutorial you will:

1. Predict protein structures using **AlphaFold**
2. Use the predicted structures as starting points for **molecular dynamics simulations in GROMACS**
3. Analyze the resulting trajectories using **Python tools**

Two systems are studied and compared:

- **HP36** – a small, well-folded protein
- **p53 TAD** – an intrinsically disordered protein domain

By comparing these systems, you will explore how **protein flexibility and disorder appear in MD simulations** and how this relates to **confidence scores from AlphaFold**.

---

# Repository Structure

The repository is organized into several folders that contain input data, simulation parameters, analysis scripts, and workflow instructions.

```
.
├── analysis
│   └── analysis_mdtraj.py
│
├── hp36
│   ├── hp36.fasta
│   └── fold_hp36_model_0.pdb
│
├── p53_TAD
│   ├── p53_TAD.fasta
│   └── fold_p53_TAD_model_0.pdb
│
├── mdp
│   ├── ions.mdp
│   ├── minim.mdp
│   ├── nvt.mdp
│   ├── npt.mdp
│   └── md.mdp
│
├── setup
│   ├── GROMACS_MD.sh
│   ├── README_AF.md
│   ├── README_MD.md
│   └── charmm36-jul2022.ff
```

---

# Folder Description

## `analysis/`

Contains the **Python analysis scripts** used to analyze MD trajectories.

The analysis uses:

- **MDTraj** for trajectory analysis
- **Seaborn** and **Matplotlib** for visualization

The script computes and plots several structural properties such as:

- RMSD (structural deviation)
- RMSF (residue flexibility)
- Radius of gyration
- Secondary structure content
- AlphaFold confidence scores (pLDDT)

---

## `hp36/`

Contains input files for the **HP36 protein system**.

Files included:

```
hp36.fasta
```

Protein sequence used as input for AlphaFold.

```
fold_hp36_model_0.pdb
```

Best AlphaFold predicted structure used as the **starting configuration for MD simulations**.

---

## `p53_TAD/`

Contains input files for the **p53 transactivation domain (TAD)** system.

Files included:

```
p53_TAD.fasta
```

Protein sequence used for AlphaFold prediction.

```
fold_p53_TAD_model_0.pdb
```

Best AlphaFold model used as the starting structure for the MD simulation.

This protein is expected to behave as an **intrinsically disordered protein**.

---

## `mdp/`

This folder contains **GROMACS parameter files** that control the different stages of the simulation.

```
ions.mdp
```

Parameters used to prepare the system before adding ions.

```
minim.mdp
```

Energy minimization settings.

```
nvt.mdp
```

Constant volume equilibration to stabilize temperature.

```
npt.mdp
```

Constant pressure equilibration to stabilize system density.

```
md.mdp
```

Production molecular dynamics simulation parameters.

All simulations use the **CHARMM36 force field** with typical cutoffs:

- `rcoulomb = 1.2 nm`
- `rvdw = 1.2 nm`
- `rvdw-switch = 1.0 nm`
- `vdw-modifier = Force-switch`

---

## `setup/`

This folder contains files needed to **set up and run the simulation workflow**.

### `GROMACS_MD.sh`

Bash script that automates the MD workflow in **GROMACS**.  
It performs the following steps:

1. Structure preparation
2. Box creation
3. Solvation
4. Ion addition
5. Energy minimization
6. NVT equilibration
7. NPT equilibration
8. Production MD simulation

---

### `README_AF.md`

Instructions describing how to:

- run **AlphaFold predictions**
- download predicted structures
- convert structures into **PDB format for GROMACS**

---

### `README_MD.md`

Instructions explaining how to:

- prepare the simulation system
- run molecular dynamics simulations using GROMACS
- organize simulation outputs

---

### `charmm36-jul2022.ff`

The **CHARMM36 force field** used for the simulations.

This folder contains all force field parameters required by **GROMACS** to perform the simulations.

---

# Tutorial Workflow

The overall workflow of the tutorial is:

```
Protein sequence
        ↓
AlphaFold structure prediction
        ↓
Convert structure to PDB
        ↓
Prepare system in GROMACS
        ↓
Run molecular dynamics simulation
        ↓
Analyze trajectories with Python
```

---

# Learning Objectives

By completing this tutorial you will learn:

- how to generate protein structures using **AlphaFold**
- how to run **molecular dynamics simulations with GROMACS**
- how to analyze trajectories using **Python**
- how to compare **predicted protein structures with dynamic behavior**

---

# Software Used

This tutorial uses the following tools:

- **AlphaFold Server** – protein structure prediction
- **GROMACS** – molecular dynamics simulations
- **MDTraj** – trajectory analysis
- **Seaborn / Matplotlib** – visualization
- **Python** – data analysis