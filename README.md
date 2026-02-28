# MD

Course on molecular dynamics, 1st yr masters in Physical Sciences - Sciences de la Matière, ENS de Lyon.

## Working environment and codes

The case studies below make use of Python libraries and simulation codes installed on the machines of the Centre Blaise Pascal, CBP.

### Python environment

A **conda** installation with the simulation codes and tools is installed in `/projects/DepartementChimie/miniforge3`. To activate it append the contents of the `conda.rc` file (in the `utils` folder) to your `.bashrc` and then login again. The `base` environment contains jupyter, numpy, matplolib, etc.

### Paths to codes on the CBP

* **OpenMM, mdtraj**: available in the `openmm` conda environment

        source /projects/DepartementChimie/conda.rc

(you can add the contents of this file to your `.bashrc`)
        
        conda activate openmm

* fftool: /projects/DepartementChimie/fftool

        export PATH=/projects/DepartementChimie/fftool:$PATH

(you can add this line to your `.bashrc`)

* packmol: /usr/bin/packmol (in the default PATH)
* VMD: /usr/local/bin/vmd (in the default PATH)
* Avogadro: /usr/bin/avogadro (in the default PATH)
* Open Babel: /usr/bin/obabel (in the default PATH)


### GPU

To check your machine's GPU configuration and monitor its usage:

        nvidia-smi

You can select and see the state of the CBP machines on the [Cloud@CBP](https://www.cbp.ens-lyon.fr/python/forms/CloudCBP) web page.


## Study cases

* `ljatoms` -- simple MD code for Lennard-Jones atoms
* `ljmols` -- simple MD code for 2-site Lennard-Jones molecules
* `openmm_basic` -- basic simulation using OpenMM (water)
* `solvation` -- solvation of simple ions and molecules


## Utilities

Utilities to improve visualization using VMD.
