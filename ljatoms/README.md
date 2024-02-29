# LJATOMS

Simple MD code for Lennard-Jones atoms (rare gases).


## Objective

The aim of this study case is to write a very simple molecular dynamics code for the simulation of a monatomic substance (ex. a rare gas) whose interactions are described by the Lennard-Jones potential. 


## How-to

The configurations of the system are stored in the PDB format, one of the most widely used to store atomic coordinates. The PDB standard is described in [cgl.ucsf.edu](https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/tutorials/pdbintro.html) and [wwpdb.org](https://www.wwpdb.org/documentation/file-format-content/format33/v3.3.html)

A very basic MD code contains the following routines/elements:

1. Read an initial configuration (PDB file).
2. Read interaction parameters (JSON file).
3. Input simulation conditions, such as temperature, time step, number of timesteps, delay between saving trajectory snapshots, cutoff distance, etc. (JSON file)
4. Compute forces.
5. Integrate the equations of motion.
6. Compute energies (kinetic and potential).
7. Compute temperature and pressure.
8. Write configurations at selected time steps.

Some remarks:
* Force and energy calculations need to account for the periodic boundary conditions.
* Interactions need to be considered explicitly only up to a cutoff distance slightly above $3\sigma$, usually 12 Å.
* Attention must be paid to the **units** in the calculation of energies and forces, as well as in the integrator.
* **Avogadro** is a handy tool to create an initial PDB file with some atoms (add the box with \<Crystallography>\<Add Unit Cell>, 30 Å side for example).
* **Packmol** can be used to pack a simulation box with a number of molecules (one has to provide a PDB file with one atom/molecule).


## Contents

### To write a minimal MD code
* `mdatom_stu.py` -- MD code to complete
* `raregas.json` -- LJ parameters of rare gases
* `sim.json` -- simulation parameters
* `pack.inp` -- fill box with many atoms (`packmol < pack.inp`)
* `pbc.vmd` -- show box and wrap coordinates (`vmd -e pbc.vmd file.pdb`)
