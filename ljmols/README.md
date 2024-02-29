# LJMOLS

Simple MD code for 2-site Lennard-Jones molecules.

Compared to the first study case, here the complexity arises from handling bonded forces, which in this example represent covalent bonds in diatomic molecules. The force field is composed of bonded and non-bonded terms (or, in other words, intra- and intermolecular potentials).

Atoms belonging to the same molecule interact through a harmonic bond potential and do not interact through the LJ potential. Therefore, exclusion lists that identify which atoms are bonded to each one have to be setup.

Most of the code, including its general organisation, is quite similar to the one for LJ atoms.


## Contents

### Minimal MD code
* `mdmol_stu.py` -- MD code to complete
* `air.pdb` -- sample system with molecules of O2, Ar, N2
* `ffnonbond.json` -- LJ parameters for N2, O2, Ar
* `ffbond.json` -- harmonic bond parameters for diatomic molecules
* `sim.json` -- simulation conditions
* `pbc.vmd` -- show box and wrap coordinates (`vmd -e pbc.vmd file.pdb`)
