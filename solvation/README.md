# SOLVATION

MD simulations to study the solvation of NaCl and of ethelene glycol in water, then study the solvation environments through structural and transport properties.

## Solvation of NaCl

### System setup and equilibration

Build a system with 1 ion pair and 500 water molecules at a density slightly lower than that of pure water at 300 K

    fftool 1 Na.xyz 1 Cl.xyz 500 spce.zmat --rho 40

Use packmol to pack the molecules

    packmol < pack.inp

Visualize the simulation box

    vmd simbox.xyz

Use fftool to generate the OpenMM input files.

    fftool 1 Na.xyz 1 Cl.xyz 500 spce.zmat --rho 40 --xml --mix a

Adapt the `omm.py` scripts from the water example to the present system (often very few modifications are necessary). Run a 200 ps equilibration.

Check that energy and density have converged by plotting the respective columns from the output file.

### Production run

Prepare the input script for a 500 ps run starting from the saved equilibrated state. Set the reporter to write 1000 configurations to the trajectory file.

### Trajectory analysis

Perform the following analysis using `MDTraj` as explained in the [analysis](analysis.ipynb) file:

* RDF and coordination number of Cl - O
* RDF and coordination number of Na - O
* Combined angular-radial distribution function O - H - Cl
* MSD of water

 
## Ehylene glycol + water

Simulate a mixture of ethylene glycol and water with the typical composition of cooling fluid.

### System setup and simulations

Build a system with 200 EG molecule and 800 water molecules at a density of 25 mol L<sup>-1</sup>

    fftool 200 EG.zmat 800 spce.zmat --rho 25 
    packmol < pack.inp

If this step takes too long, the initial density may be too high. Reduce a bit and retry.

    vmd simbox.xyz

Check that the box looks ok, then create the OpenMM input files

    fftool 200 EG.zmat 800 spce.zmat --rho 25 --xml --mix a

Run equilibration and a production runs.


### Trajectory anaysis

Perform the following analysis using `MDTraj`  as explained in the [analysis](analysis.ipynb) file:

* RDF and coordination number of C - Ow
* RDF and coordination number of OHG - Ow
* RDF of HOG - Ow 
* RDF of Hw - OHG
* Combined angular-radial distribution 
function OHG - HOG - Ow
* Combined angular-radial distribution 
function Ow - Hw - OHG
* Combined angular-radial distribution 
function OHG - HOG - OHG
* Dihedral distribution of the O - C - C - O dihedral in EG

