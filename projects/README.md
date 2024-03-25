# Exam Project
For the final examination you have to complete **one project** between:

* 1 -  Write a molecular MD code to perform NVT and NPT simulations.

* 2 - Study of solvation properties 

* 3 - Study of solid-liquid interface 
 

## 1 - NVT-NPT MD code

The aim of this project is to implement a thermostat and a barostat in the molecular code [ljmols](../ljmols/).

### 1.1 - Molecular NVE code

Complete the assignement contained in [ljmols](../ljmols/), namely:
* Add bonded contribution to the atomic code 
* Implement an exclusion list

Verify that the code works properly with the suggested runs and compare the results with LAMMPS

### 1.2 - Molecular NVT code

Choose to implement one thermostat from the following:

* [Berendsen Thermostat](https://doi.org/10.1063/1.448118)

* [Langevin Thermostat]([https://levich.ccny.cuny.edu/koplik/molecular_simulation/AT2.pdf])


Compare the results obtained by simulating air with LAMMPS and comment on the pros and the cons of the chosen thermostat.

### 1.3 - Molecular NPT code

Choose to implement one barostat from the 
following:

* [Berendsen Barostat](https://doi.org/10.1063/1.448118)

* [Langevin Piston Barostat](https://doi.org/10.1063/1.470648)


Compare the results obtained by simulating air with LAMMPS and comment on the pros and the cons of the chosen barostat.

## 2 - Solvation

The aim of this project is to study the solvation properties of the chosen solvent-solute system.

### 2.1 - Structure and dynamics of pure solvent

Use LAMMPS to run the MD simulations of one of the following solvents:

* methanol
* ethanol
* dmso
* toluene

Study the structural and dynamic properties of the system using LAMMPS and MDTraj and compare your findings with existing data in the literature.

### 2.2 - Structure and dynamics in the presence of the solute

Add in the solvent one of the following solutes:

* SO2
* Paracetamol
* Sodium acetate

Study the solvation environment of the soulte by calculating the structural and dynamic properties of the system using MDTraj and compare with the literature when possible. 

## 3 - Solid-Liquid Interface

The aim of this project is to calculate the contact angle between the liquid and the solid  surface to study its wetting properties.

### 3.1 - Build the solid-liquid interface

Use [packmol](https://m3g.github.io/packmol/userguide.shtml) and [fftool](https://github.com/paduagroup/fftool) to build the solid-liquid interface between one of:

* Graphite
* MoS2

and 

* water 
* ethanol

### 3.2 - Run Simulation using LAMMPS

Use LAMMPS to equilibrate the systems and run production trajectory

### 3.3 - Analyze the trajectory

Use MDTraj to write your own analysis tool to derive the contact angle between solid and liquid and compare with the literature.

