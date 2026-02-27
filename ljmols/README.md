# LJMOLS

Simple MD code for 2-site Lennard-Jones molecules.

## Objective

The aim of this study case is to write a minimal molecular dynamics code for the simplest molecules. Most of the code, including its general organization, is quite similar to the one for LJ atoms of the first study case.

Here the complexity arises from handling bonded forces, in this example the covalent bonds in diatomic molecules. These are represented by a harmonic bond-stretching potential.

As in the first study case, working on code written by someone else develops important skills, so take time to study it and try to understand its structure.

## Handling bonded and non-bonded forces

The force field is composed of bonded and non-bonded terms (or, in other words, intra- and intermolecular potentials), in this example harmonic bond-stretching and Lennard-Jones potentials between atomic sites.

Atoms belonging to the same molecule interact through the bonded potential, which accounts for their total interaction. Therefore, bonded atoms do not interact through the LJ potential. This leads to setup exclusion lists that identify which atoms are covalently bonded, and therefore excluded from the computation of the non-bonded forces.

## Contents

### Minimal MD code and input files

* `mdmol_gaps.py` -- MD code with gaps to complete
* `air.pdb` -- sample system with a few molecules of O<sub>2</sub>, Ar and N<sub>2</sub>
* `ffnonbond.json` -- LJ parameters for N<sub>2</sub>, O<sub>2</sub>, Ar
* `ffbond.json` -- harmonic bond parameters for diatomic molecules
* `sim.json` -- simulation conditions
* `pack.inp` -- to make a box with air using packmol (`packmol < pack.inp`)
* `pbc.vmd` -- to show box and wrap coordinates in VMD (`vmd -e pbc.vmd file.pdb`)


## Suggested runs

* Take the `air.pdb` system and run a few steps (200) with a time step of 1 fs, to check if molecules behave as expected (bond vibrations, rotations). Test with different initial velocities (temperatures).
* Create a box of air with 100 molecules (30 Å cube): 79 N<sub>2</sub> molecules, 20 O<sub>2</sub> molecules and 1 Ar; run 2000 steps and compare the properties with those from [CoolProp](http://ibell.pythonanywhere.com) for air (it is easier to provide T and p and calculate density, but you can also calculate the mass density of the simulated air).
