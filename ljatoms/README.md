# LJATOMS

Simple MD code for Lennard-Jones atoms (rare gases).


## Objective

The aim of this study case is to write a very simple molecular dynamics code for the simulation of a monatomic substance (ex. a rare gas) whose interactions are described by the Lennard-Jones potential. 

An example minimal MD code is supplied, in which the parts that calculate energies, forces, etc. have been removed. The aim of the study case is to complete the code.

Spend some time studying the code to understand its organization and data structures.

Working on code written by other people is the norm when contributing to a collaborative project. This study case tries to showcase this at a very small scale!


## Minimal MD code

A very basic MD code contains the following routines/elements:

1. Read an initial configuration (PDB file).
2. Read interaction parameters (JSON file).
3. Input simulation conditions, such as temperature, time step, number of timesteps, delay between saving trajectory snapshots, cutoff distance, etc. (JSON file)
4. Compute forces.
5. Integrate the equations of motion.
6. Compute energies (kinetic and potential).
7. Compute temperature and pressure.
8. Write configurations at selected time steps.

Some important points when completing the code:

* Force and energy calculations need to account for the periodic boundary conditions.
* Force calculations should be as efficient as possible, since this is where the code spends most time.
* Interactions need to be considered explicitly only up to a cutoff distance slightly above $3\sigma$, usually 12 Å.
* Attention must be paid to the **units** in the calculation of energies and forces, as well as in the integrator.
* The configurations of the system are stored in the PDB format, one of the most widely used to store atomic coordinates. The PDB standard is described in [cgl.ucsf.edu](https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/tutorials/pdbintro.html) and [wwpdb.org](https://www.wwpdb.org/documentation/file-format-content/format33/v3.3.html).
* Avogadro is a handy tool to create an initial PDB file with some atoms (add the box with \<Crystallography>\<Add Unit Cell>).
* Packmol can be used to pack a simulation box with a number of molecules; it is controlled by a simple input file (one has to provide a PDB file with one molecule).


## Contents

### Minimal MD code and input files
* `mdatom_stu.py` -- MD code for students to complete
* `raregas.json` -- LJ parameters of rare gases
* `sim.json` -- simulation parameters
* `pack.inp` -- to fill box with many atoms using packmol (`packmol < pack.inp`)
* `pbc.vmd` -- to show box and wrap coordinates in VMD (`vmd -e pbc.vmd file.pdb`)


## Sujested runs

* Create a PDB file with 2 Ar atoms at a chosen distance in a box of 30 Å using Avogadro to test energy and force calculations.
* Build a system with more atoms (10 -- 12) using Avogadro and run a short trajectory (20 000 steps of 5 fs, saving every 100):
    * Visualize the trajectory using VMD.
    * Test with different initial velocities (temperatures of 0, 100 and 200 K for example).
* Build a system with 100 atoms using packmol and run a trajectory of 20 000 steps starting with initial velocities of zero (T = 0 K):
    * Redirect the output to a file (`> md.out &` at the end of the command line) in order to plot properties later.
    * Check the conservation of energy.
    * Compare the pVT properties from simulation with those of argon in the same conditions of temperature and density (or pressure) using [CoolProp](http://ibell.pythonanywhere.com), which implemenbts very accurate equations of state for fluids.
