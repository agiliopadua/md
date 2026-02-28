# WATER

MD simulation of water (the most important liquid!) using OpenMM.

## Objective

Run a simulation of liquid water and calculate structural, thermodynamic and transport properties.


## Three-site water models

The simplest realistic models of water consist of three sites corresponding to the O and H atoms. They are usually labelled Ow and Hw to distinguish them from O and H atoms on other compounds. In 3-site water models, the Ow atom has a LJ site and a negative partial charge, with the Hw atoms having just positive partial charges (no LJ sites on hydrogens: the Hw are embedded in the van der Waals radius of the the Ow, which accounts for the repulsive and van der Waals interactions of the entire water molecule).

The SPCE model is one of the popular 3-site water models [[1](#spce),[2](#opc3)]. It is a rigid model, but some variants can have a flexible HOH angle [[3](#flex)] (a flexible OH bond is less relevant).


## Contents

* `spce.zmat`: fftool input file for SPCE water molecule (z-matrix file)
* `spce.xml`: fftool input file with force field parameters of SPCE water
* `omm.py`: OpenMM script to run a simple simulation
* `openmm.ipynb`: Jupyter notebook for an OpenMM simulation


## Tools and codes

The **fftool** and **packmol** utilities can build initial configuration and force field files for OpenMM. Use **VMD** for visualization of the trajectories.

Activate the conda environment with OpenMM:

    conda activate openmm


## Carry out the simulations

### 1. Build system with 500 water molecules

Build a box with 1000 water molecules, with a density somewhat below the experimental value at 300 K (which is about 55 mol L<sup>-1</sup>):

    fftool 1000 spce.zmat --rho 40

this produces an input file for packmol, which packs the water molecules into a cubic box (look at the contents of `pack.inp`):

    packmol < pack.inp

visualize the box created:

    vmd simbox.xyz

Then run fftool again to read the coordinates from `simbox.xyz` and generate input files for OpenMM:

    fftool 1000 spce.zmat --rho 40 --xml --mix a

this creates two input files:

    field.xml
    config.pdb

Familiarize yourself with their formats and content.


### 2. Run an equilibration of 200 ps

We want to start from the initial configuration at 40 mol L<sup>-1</sup> and let it reach a state representative of thermodynamic equilibrium. We will then use the last configuration from the equilibration to start a production trajectory, from which averages of quantities  will be meaningful.

Edit the `omm.py` (or better a copy named `omm-eq.py`) script or open the `openmm.ipynb` Jupyter notebook to perform the equilibration run. Adapt the `Reporters` to:

* write a resonable number of times to the screnn
* write a reasonable number of configurations to the trajectory file (about 500 configurations)

Check that the GPU in your machine is available

    nvidia-smi

The output of the script can be sent to a file:

    ./omm-eq.py > omm-eq.out &

The `&` sends the job to background. If you need to cancel it use `ps` and then `kill PID`. You can follow the contents of the output file with (exit with <Ctrl>-C):

    tail -f omm-eq.out

(Ctrl-C to exit the `tail` command)

Follow the evolution of the different properties (density, energies) and the the speed in ns/day.

Visualize the equilibration trajectory

    vmd -e ../utils/pbc.vmd config.pdb traj.dcd


### 3. Run a production trajectory of 500 ps

Make a copy of the OpenMM input script `omm-run.py` to:
* read the configuration from the saved state in `state-eq.xml` (the necessary code in `omm.py` needs to be commented out)
* modify the `Reporters` to save a reasonable number of configurations to the trajectory (1000 snapshots)

    ./omm-run.py > omm-run.out &
    tail -f omm-run.out


### 4. Compute physical quantities (and compare with experimental values):

* density (trivial)
* enthalpy of vaporization (the intermolecular potential energy plus RT)
* self-diffusion coefficient from the mean-squared displacement, using `mdtraj` (Jupyter notebook provided)
* radial distribution functions using `mdtraj` (Jupyter notebook provided)
* static permittivity (dielectric constant)


## References

1. <a id="spce" /> Berendsen, H. J. C.; Grigera, J. R.; Straatsma, T. P. The Missing Term in Effective Pair Potentials. *J. Phys. Chem.* 1987, 91 (24), 6269–6271. DOI: [10.1021/j100308a038](https://doi.org/10.1021/j100308a038)
2. <a id="opc3" /> Izadi, S.; Onufriev, A. V. Accuracy Limit of Rigid 3-Point Water Models. *J. Chem. Phys.* 2016, 145 (7), 074501. DOI: [10.1063/1.4960175](https://doi.org/10.1063/1.4960175)
3. <a id="flex" /> Wu, Y.; Tepper, H. L.; Voth, G. A. Flexible Simple Point-Charge Water Model with Improved Liquid-State Properties. The Journal of Chemical Physics 2006, 124 (2), 24503–24503. DOI: [10.1063/1.2136877]](https://doi.org/10.1063/1.2136877)
