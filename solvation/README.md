# SOLVATION

MD simulations to study the solvation of NaCl and glycerol in water.

## Objective

Run simulations to study the solvation environment through structural and transport properties.

## Tools and codes

The **fftool** and **packmol** utilities are needed to set up the systems. To perform analysis the python library `MDTraj` will be used. To access all the python libraries activate the `omm` conda environment

    conda activate omm

use **VMD** for visualization

## Simulations

## 1 - Solvation of NaCl
### 1.0 - Equilibration
Build a system with 1 ion pair and 500 water molecules at a density slightly lower than that of pure water at 300 K

    fftool 1 na.xyz 1 cl.xyz 500 spce.zmat -r 40

use packmol to pack the nely generated system

    packmol < pack.inp

and visualize the obtained simulation box

    vmd simbox.xyz

use fftool to generate the lammps input files.

    fftool 1 na.xyz 1 cl.xyz 500 spce.zmat -r 40 -l

As for the example in water we will run a 100 ps equilibration followed by a 100 ps production trajectory.
    
Copy the `in.lmp` file to create `in-eq.lmp`

    cp in.lmp in-eq.lmp

and modify it following the instruction in the [water](../water/) directory.

Run the equilibration using LAMMPS

    mpirun -np 8 lmp -in in-eq.lmp > eq.lmp &

Check that energy and density have converged by plotting the respective columns from the `log.lammps` file.

### 1.1 - Production run

Prepare the input script for LAMMPS

    cp in-eq.lmp in-run.lmp

and modify it as for the [water](../water/) case.

Since we are now simulating more than one component, we have to define groups of atoms for which we want to calculate the **MSD**

    group Na type 1
    group Cl type 2
    group H2O type 3 4

and the MSD will be now defined by 

    compute MSDNa Na msd
    compute MSDCl Cl msd
    compute MSDW H2O msd
    ...
    thermo_style ... c_MSDNa[4] c_MSDCl[4] c_MSDW[4]

While for the **RDF** calculation the pairs of interest change. To study the solvation shell of the solvents we calculate the RDF between Na - Ow (`1 4`) and Cl - Ow (`2 4`). Hydrogen bonding between chloride and water can be studied via the RDF between Cl - Hw  (`2 3`).

    compute RDF all rdf 120 1 4 2 4 2 3
    fix RDF all ave/time 50 2000 100000 c_RDF[*] mode vector file rdf.lmp

dump the trajectory every 100 steps.

### 1.2 - Analysis

Perform the following analysis using `MDTraj` as explained in the [analysis.ipynb](../water/) file:

* RDF and coordination number of Cl - O
* RDF and coordination number of Na - O
* Combined angular-radial distribution function O - H - Cl
* MSD of water

compare the results with LAMMPS when possible.

## 2 Solvation of ethelene glycol

### 2.0 - Equilibration

Build a system with 1 EG molecule and 500 water 
molecules at a density slightly lower than that of 
pure water at 300 K

    fftool 1 eg.xyz 500 spce.zmat -r 40

Pack the system using `packmol` and generate the LAMMPS input files using `fftool` as done in the previous case. 

Copy the `in.lmp` file to create `in-eq.lmp`

    cp in.lmp in-eq.lmp

and modify it following the instruction in the 
[water](../water/) directory.

Run the equilibration using LAMMPS

    mpirun -np 8 lmp -in in-eq.lmp > eq.lmp &

Check that energy and density have converged by 
plotting the respective columns from the `log.
lammps` file.

### 2.1 - Production run

Prepare the input script for LAMMPS

    cp in-eq.lmp in-run.lmp

and modify it as for the [water](../water/) case.

While for the **RDF** calculation the pairs of 
interest change. To study the solvation shell of the 
solvents we calculate the RDF between C* - Ow (`1 
4`) and Cl - Ow (`2 4`). Hydrogen bonding between 
chloride and water can be studied via the RDF 
between Cl - Hw  (`2 3`).

    compute RDF all rdf 120 1 4 2 4 2 3
    fix RDF all ave/time 50 2000 100000 c_RDF[*] 
mode vector file rdf.lmp

dump the trajectory every 100 steps.