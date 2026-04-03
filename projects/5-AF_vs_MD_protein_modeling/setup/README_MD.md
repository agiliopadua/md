# Running the Molecular Dynamics Pipeline

This script automates the full molecular dynamics workflow using **GROMACS**, starting from an AlphaFold structure and ending with a production MD simulation.

The workflow performs the following steps:

1. Structure preparation  
2. Simulation box creation  
3. Solvation  
4. Ion addition  
5. Energy minimization  
6. NVT equilibration  
7. NPT equilibration  
8. Production MD simulation  

---

# Script: `GROMACS_MD.sh`

```bash
#!/bin/bash

# upload GROMACS
source /DAMM/software/gromacs_teaching_room/trixie/AVX_256/gromacs-2025.3/bin/GMXRC

folder_name=$1
# step 0: in each simulation folder place the FF folder: charmm36-jul2022.ff
# Process the AF configuration file
# Here, choose the FF (option 1, placed in the current folder), water model - TIP3P (option 1); NH3+ and COO- as terminal residues 
gmx pdb2gmx -f fold_${folder_name}_model_0.pdb  -o processed.gro -ignh -ter

# Define the simulation box & solvate
gmx editconf -f processed.gro -o boxed.gro -c -d 1.0 -bt dodecahedron
gmx solvate -cp boxed.gro -cs spc216.gro -o solvated.gro -p topol.top

# Add ions by replacing solvent (SOL) by ions 
gmx grompp -f ../mdp/ions.mdp -c solvated.gro -p topol.top -o ions.tpr -maxwarn 1
gmx genion -s ions.tpr -o ionized.gro -p topol.top -neutral

# Energy minimization
gmx grompp -f ../mdp/minim.mdp -c ionized.gro -p topol.top -o em.tpr
gmx mdrun -deffnm em -v

# NVT equilibration
gmx grompp -f ../mdp/nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
gmx mdrun -deffnm nvt -v

# NPT equilibration
gmx grompp -f ../mdp/npt.mdp -c nvt.gro -r nvt.gro -p topol.top -o npt.tpr
gmx mdrun -deffnm npt -v

# Production
gmx grompp -f ../mdp/md.mdp -c npt.gro -p topol.top -o md.tpr
gmx mdrun -deffnm md -v

# Create a trajectory for the analysis
gmx trjconv -s md.tpr -f md.xtc -o md_peptide_no_pbc_center.xtc -center -pbc mol
gmx trjconv -s md.tpr -f md.xtc -o md_peptide_no_pbc_center.pdb -center -pbc mol -dump 0

```
# How to Run the Script:

```bash
bash run_md.sh hp36
```
The script expects the AlphaFold structure to be named: 
```bash
fold_<folder_name>_model_0.pdb
```