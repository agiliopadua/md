# LJATOMS

Simple MD code for Lennard-Jones atoms (rare gases).

The aim is to write a very simple molecular dynamics code for the simulation of a monatomic substance (ex. a rare gas) whose interactions are described by the Lennard-Jones potential. 

The configurations of the system are stored in the PDB format, which one of the most used to store atomic coordinates. The PDB standard is described in [cgl.ucsf.edu](https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/tutorials/pdbintro.html) and [wwpdb.org](https://www.wwpdb.org/documentation/file-format-content/format33/v3.3.html)


## Contents

- `raregas.json` - LJ parameters of the rare gases
- `raregas.xml` - force field database for the rare gases
- `md_pdb.py` - functions to read and write PDB files
