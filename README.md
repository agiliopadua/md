# MD

Course on molecular dynamics, 1st yr masters in Physical Sciences - Sciences de la Matière, ENS de Lyon.

## Working environment and codes

The case studies below make use of Python libraries and simulation codes installed in the machines of the CBP.

### Python environment

In order to activate the **conda** installation in `/projects/DepartementChimie/miniconda3`, append the contents of the `conda.rc` file to your `.bashrc`.

### Codes

* LAMMPS: /projects/DepartementChimie/lammps/bin/lmp
* packmol: /usr/bin/packmol (in the PATH)
* VMD: /usr/local/bin/vmd (in the PATH)
* Avogadro: /usr/bin/avogadro (in the PATH)
* Open Babel: /usr/bin/obabel
* Gromacs: /usr/bin/gmx (in the PATH)
* OpenMM, mdtraj: `conda activate omm`


## Study cases

* `ljatoms` -- simple MD code for Lennard-Jones atoms
* `ljmols` -- simple MD code for 2-site Lennard-Jones molecules
* `water` -- simulation of water using LAMMPS
