# LJATOMS

Simple MD code for Lennard-Jones atoms (rare gases).

The aim of this study case is to write a very simple molecular dynamics code for the simulation of a monatomic substance (ex. a rare gas) whose interactions are described by the Lennard-Jones potential. 

The configurations of the system are stored in the PDB format, one of the most widely used to store atomic coordinates. The PDB standard is described in [cgl.ucsf.edu](https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/tutorials/pdbintro.html) and [wwpdb.org](https://www.wwpdb.org/documentation/file-format-content/format33/v3.3.html)

A very basic MD code contains the following routines/elements:

- read an initial configuration (PDB file)
- read interaction parameters (JSON file)
- input simulation conditions (temperature, time step, number of timesteps, delay between saving trajectory snapshots, cutoff distance)
- compute the energy (potential and kinetic)
- compute forces
- integrate the equations of motion
- write configurations at selected time steps

Some remarks:
- Force and energy calculations need to account for the periodic boundary conditions.
- Interactions need to be considered explicitly only up to a cutoff distance of around $3\sigma \approx 12$ Å.
- Attention must be paid to the **units** in the calculation of energies and forces, and in the integrator.

Routines to read and write PDB files are supplied, as well as the LJ potential parameters of the rare gases.


## Contents

- `raregas.json` - LJ parameters of the rare gases
- `raregas.xml` - force field database for the rare gases
- `md_pdb.py` - functions to read and write PDB files
