# LJMOLS

Simple MD code for 2-site Lennard-Jones molecules.

## Objective

The aim of this study case is to write a very simple molecular dynamics code for the simplest molecules. Most of the code, including its general organisation, is quite similar to the one for LJ atoms of the first study case. Here the complexity arises from handling bonded forces, which in this example represent covalent bonds in diatomic molecules.


## Handling bonded and non-bonded forces

The force field is composed of bonded and non-bonded terms (or, in other words, intra- and intermolecular potentials), in this example harmonic bond stretching and Lennard-Jones potential between atomic sites.

Atoms belonging to the same molecule interact through a harmonic bond potential and do not interact through the LJ potential. Therefore, exclusion lists that identify which atoms are bonded to each one have to be setup.


## Contents

### Minimal MD code and input files

* `mdmol_stu.py` -- MD code to complete
* `air.pdb` -- sample system with molecules of O2, Ar, N2
* `ffnonbond.json` -- LJ parameters for N2, O2, Ar
* `ffbond.json` -- harmonic bond parameters for diatomic molecules
* `sim.json` -- simulation conditions
* `pack.inp` -- make box with air (`packmol < pack.inp`)
* `pbc.vmd` -- show box and wrap coordinates (`vmd -e pbc.vmd file.pdb`)


## Suggested runs

* Take the `air.pdb` system and run a few steps (200) with a timestep of 1 fs, to check if molecules behave as expected (bond vibrations, rotation). Test with different initial velocities (temperatures).
* Create a box of air with 100 molecules (30 Å cube): 79 N2 molecules, 20 O2 molecules and 1 Ar; run 2000 steps and compare the properties with those from [CoolProp](http://ibell.pythonanywhere.com).
