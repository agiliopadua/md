# LJATOMS

Simple MD code for Lennard-Jones atoms (rare gases).


## Objective

This very simple code should allow you to become familiar with the different components of a molecular dynamics code, and for that we start with the simulation of a monatomic substance (ex. a rare gas) whose interactions are described by the Lennard-Jones potential. 

An example of a minimal MD code is supplied, in which some parts that calculate energies, forces, etc. have been removed. The aim of the study case is to complete gaps in the code and perform some short runs.

Working on code written by others is always challenging, but is the norm when contributing to a collaborative computational project. Here we attempt to showcase this at a very small scale.


## Contents

### Minimal MD code and input files
* `mdatom_gaps.py` -- MD code with gaps to complete
* `raregas.json` -- LJ parameters of rare gases
* `sim.json` -- example simulation parameters
* `pack.inp` -- fill box with many atoms using packmol (`packmol < pack.inp`)
* `pbc.vmd` -- display box and wrap coordinates in VMD (`vmd -e pbc.vmd file.pdb`)


## Minimal MD code

A very basic MD code contains the following procedures:

1. Read an initial configuration of the system (PDB file). The configurations of the system are stored in the PDB format, one of the most widely used to store atomic coordinates. The PDB standard is described in [cgl.ucsf.edu](https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/tutorials/pdbintro.html) and [wwpdb.org](https://www.wwpdb.org/documentation/file-format-content/format33/v3.3.html).
2. Read interaction parameters (JSON file).
3. Input the simulation conditions, such as temperature, time step, number of timesteps, delay between saving trajectory snapshots, cutoff distance, etc. (JSON file)
4. Calculate forces.
5. Integrate the equations of motion.
6. Calculate energies (kinetic and potential).
7. Calculate temperature and pressure.
8. Write configurations at selected time steps.

Allow yourself some time to read the `mdatom_gaps.py` script in detail, aiming to understand its organization and data structures. Also look at the input files.

Some important points when completing the gaps in the code:

* Force and energy calculations need to account for the periodic boundary conditions.
* Force calculations should be as efficient as possible, since this is where the code spends most time.
* Interactions need to be considered explicitly only up to a cutoff distance slightly above $3\sigma$, usually 12 Å.
* Attention must be paid to the **units** in the calculation of energies and forces, as well as in the integrator.


## Suggested runs

* Create a PDB file with 2 Ar atoms at a chosen distance in a box of 30 Å using Avogadro, to test energy and force calculations. Avogadro is a handy tool to create an initial PDB file with some atoms (add the box with \<Crystallography>\<Add Unit Cell>).
* Build a system with more atoms (10–12) using Avogadro and run a short trajectory (20 000 steps of 5 fs, saving every 100 steps):
    * Visualize the trajectory using VMD.
    * Test with different initial velocities (temperatures of 0, 100 and 200 K for example).
* Build a system with 100 atoms using `packmol` and run a trajectory of 20 000 steps starting with initial velocities of zero (T = 0 K):
    * Redirect the output to a file (adding `> md.out &` at the end of the command line) in order to plot properties later.
    * Check the conservation of energy.
    * Compare the pVT properties from simulation with those of argon in the same conditions of temperature and density (or pressure) using [CoolProp](http://ibell.pythonanywhere.com), which implements very accurate equations of state for fluids.
