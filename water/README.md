# WATER

MD simulation of water, the most important liquid!

## Three-site water models

The simplest realistic models of water consist of three sites corresponding to the O and H atoms. They are usually labelled Ow and Hw to distinguish them from oxygen and hydrogen sites on other compounds. In 3-site water models, the Ow atom has a LJ site and a negative partial charge, and the Hw atoms have just positive partial charges (no LJ sites: the Hw are embedded in the van der Waals radius of the site placed on the Ow, which accounts for the entire water molecule).

The SPCE model is one of the popular 3-site water models [[1](#spce),[2](#opc3)]. It is a rigid model, but some variants can have a flexible HOH angle [[3](#flex)] (a flexible OH bond is less relevant).

## Objective

Run a simulation of liquid water and calculate structural, thermodynamic and transport properties.

1. Prepare a system with 500 water molecules and a density 20% below the experimental density at 300 K.
2. Equilibrate the system at constant NpT for 200 ps, with a time step of 1 fs. Check that energy and density have converged.
3. Run a production trajectory of 200 ps, saving 1000 snapshots.
4. Compute the following quantities (and compare to experiemntal values):
    - density
    - radial distribution functions
    - self-diffusion coefficient from the mean-squared displacement
    - enthalpy of vaporization
    - static permitivity (dielectric constant)

## Tools and codes

Use the **fftool** and **packmol** utilities to build an initial configuration and force field fir use with the **LAMMPS** code. Instructions are given in the [fftool GitHub](https://github.com/paduagroup/fftool). 

Visualize your system using **VMD**. 


## Contents

- `spce.zmat`: SPCE water molecule (z-matrix file)
- `spce.xml`: force field parameters of SPCE water


## References

1. <a id="spce" /> Berendsen, H. J. C.; Grigera, J. R.; Straatsma, T. P. The Missing Term in Effective Pair Potentials. *J. Phys. Chem.* 1987, 91 (24), 6269–6271. DOI: [10.1021/j100308a038](https://doi.org/10.1021/j100308a038)
2. <a id="opc3" /> Izadi, S.; Onufriev, A. V. Accuracy Limit of Rigid 3-Point Water Models. *J. Chem. Phys.* 2016, 145 (7), 074501. DOI: [10.1063/1.4960175](https://doi.org/10.1063/1.4960175)
3. <a id="flex" /> Wu, Y.; Tepper, H. L.; Voth, G. A. Flexible Simple Point-Charge Water Model with Improved Liquid-State Properties. The Journal of Chemical Physics 2006, 124 (2), 24503–24503. DOI: [10.1063/1.2136877]](https://doi.org/10.1063/1.2136877)

