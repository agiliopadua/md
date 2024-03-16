# MD

Course on molecular dynamics, 1st yr masters in Physical Sciences - Sciences de la Matière, ENS de Lyon.

## Working environment and codes

The case studies below make use of Python libraries and simulation codes installed in the machines of the CBP.

### Python environment

A **conda** installation with the simulation codes and tools is installed in `/projects/DepartementChimie/miniconda3`. To activate it append the contents of the `conda.rc` file (in this repository) to your `.bashrc` and then login again. The `base` environment contains jupyter, numpy, matplolib, etc.

### Paths to codes on the CBP

* **LAMMPS**: /projects/DepartementChimie/lammps/bin/lmp

    Include in your `.bashrc` (and then restart a terminal shell):

        DEPT=/projects/DepartementChimie
        export LD_LIBRARY_PATH=$DEPT/plumed/lib
        export PATH=$DEPT/lammps/bin:$PATH

* packmol: /usr/bin/packmol (in the PATH)
* VMD: /usr/local/bin/vmd (in the PATH)
* Avogadro: /usr/bin/avogadro (in the PATH)
* Open Babel: /usr/bin/obabel (in the PATH)
* Gromacs: /usr/bin/gmx (in the PATH)
* **OpenMM, mdtraj**: in the `omm` conda environment

        conda activate omm


## Study cases

* `ljatoms` -- simple MD code for Lennard-Jones atoms
* `ljmols` -- simple MD code for 2-site Lennard-Jones molecules
* `water` -- simulation of water using LAMMPS
* `solvation` -- simulation of solvation of NaCl and ethelene glycol in water using LAMMPS
