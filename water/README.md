# WATER

MD simulation of water, the most important liquid!

## Three-site water models

The simplest realistic models of water consist of three sites corresponding to the O and H atoms. They are usually labelled Ow and Hw to distinguish them from O and H atoms on other compounds. In 3-site water models, the Ow atom has a LJ site and a negative partial charge, with the Hw atoms having just positive partial charges (no LJ sites: the Hw are embedded in the van der Waals radius of the the Ow, which accounts for the entire water molecule).

The SPCE model is one of the popular 3-site water models [[1](#spce),[2](#opc3)]. It is a rigid model, but some variants can have a flexible HOH angle [[3](#flex)] (a flexible OH bond is less relevant).

## Objective

Run a simulation of liquid water and calculate structural, thermodynamic and transport properties.

## Tools and codes

With the **fftool** and **packmol** utilities build initial configuration and force field files for use with the LAMMPS code.

Download **fftool** from the [fftool GitHub](https://github.com/paduagroup/fftool).

Instructions on how to use are provided there. Test that it works with

    fftool -h

Use **VMD** for visualization.


## Carry out the simulations

### 1 - Build system 

Build a box with 500 water molecules, with a density somewhat below the experimental value at 300 K (about 55 mol L<sup>-1</sup>):

    fftool 500 spce.zmat -r 40

this produces an input file for packmol, which packs the water molecules into a cubic box:

    packmol < pack.inp

visualize the box created:

    vmd simbox.xyz

run fftool again to read the coordinates from `simbox.xyz` and generate input files for LAMMPS:

    fftool 500 spce.zmat -r 40 -l

this creates two files, one is a script with LAMMPS commands and the other a data file with the force field parameters, atomic coordinates and molecular topologies:

    in.lmp
    data.lmp

study their content.

### 2 - Run an equilibration of 50 ps

Make a copy of `in.lmp` for editing

    cp in.lmp in-eq.lmp

edit `in-eq.lmp` to run 50 000 steps at constant NpT.

Check how many processor cores your machine has

    lscpu

 Physical cores are (sockets) * (cores per socket). This is half the number of CPUs printed, which is actually the number of threads.

LAMMPS uses MPI for parallel execution. To launch NP parallel processes:

    mpirun -np NP <command> <arguments> > <output_file> &

The `&` sends the job to background. If you need to cancel it use `ps` and then `kill PID`

Run the equilibration (8 processes here)

    mpirun -np 8 lmp -in in-eq.lmp > out.lmp &

This should take 5 minutes or so, depending on the machine; check progress (Ctrl-C to exit the `tail` command):

    tail -f out.lmp

Look at the table at the end of the file with the performance: find the speed in ns/day and where LAMMPS spends time (pair interactions, electrostatics, communication, etc.)

Check that energy and density have converged by plotting the respective columns from the `log.lammps` file.

Visualize the trajectory

    vmd -e pbc.vmd dump.lammpstrj


### 3. Run a production trajectory of 100 ps

Prepare a new input script for LAMMPS

    cp in-eq.lmp in-run.lmp

Edit the `in-run.lmp` file to:
* read the configuration from `data.eq.lmp` (the last one saved from the equilibration)
* **do not create new velocities!** (comment out the command)
* calculate mean-squared displacements (and add to `thermo_style` for printing)

        compute MSD all msd
        ...
        thermo_style custom ... c_MSD[4]

    study the man page of the `compute msd` on the LAMMPS site

* compute radial distribution functions Hw-Hw, Ow-Ow and Hw-Ow and average over the trajectory

        compute RDF all rdf 120 1 1 2 2 1 2
        fix RDF all ave/time 50 2000 100000 c_RDF[*] mode vector file rdf.lmp

    study the man page of `compute rdf` and `fix ave/time` on the LAMMPS site

* save a snapshot to `dump.lammpstrj` every 100 steps

* run 100 000 steps


### 4 - Compute quantities (and compare with experimental values):
- density
- enthalpy of vaporization (the intermolecular potential energy plus RT)
- radial distribution functions 
- self-diffusion coefficient from the mean-squared displacement
- static permitivity (dielectric constant) calculated from the configurations stored in the trajectory using the `rerun` command (`in-rerun.lmp`).


## Contents

- `spce.zmat`: SPCE water molecule (z-matrix file)
- `spce.xml`: force field parameters of SPCE water
- `in-rerun.lmp`: calculation of static permitivity from fluctuations of the dipole moment


## References

1. <a id="spce" /> Berendsen, H. J. C.; Grigera, J. R.; Straatsma, T. P. The Missing Term in Effective Pair Potentials. *J. Phys. Chem.* 1987, 91 (24), 6269–6271. DOI: [10.1021/j100308a038](https://doi.org/10.1021/j100308a038)
2. <a id="opc3" /> Izadi, S.; Onufriev, A. V. Accuracy Limit of Rigid 3-Point Water Models. *J. Chem. Phys.* 2016, 145 (7), 074501. DOI: [10.1063/1.4960175](https://doi.org/10.1063/1.4960175)
3. <a id="flex" /> Wu, Y.; Tepper, H. L.; Voth, G. A. Flexible Simple Point-Charge Water Model with Improved Liquid-State Properties. The Journal of Chemical Physics 2006, 124 (2), 24503–24503. DOI: [10.1063/1.2136877]](https://doi.org/10.1063/1.2136877)

