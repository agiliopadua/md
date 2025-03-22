# PMF

MD simulation to calculate the PMF of Na Cl in water using umbrella sampling


## Objective

Through the principles of umbrella sampling, create a bias for different windows of NaCl distances and plot histograms of the biased displacements. Use the WHAM code to retrieve the PMF curve.

## Tools

WHAM implementation form [Grossfield Lab](http://membrane.urmc.rochester.edu/?page_id=126)

Download the source code and untarr it in your `~/src` directory

    tar -xvf ~/src/ wham-release-2.1.0.tgz

than build the wham code using make 

    cd wham/wham
    make clean
    make

move the newly created file `wham` in your bin

    mv wham ~/bin/.
    
try if it working

    wham -h

gnuplot for visualization

## Do the simulations

Use the final configuration obtained in [solvation](../solvation) to run the umbrella simulation.

Modify the `in-pmf.lmp` reading [LAMMPS documentation](https://docs.lammps.org/Manual.html) to run the umbrella simulation.

plot the histograms using gnuplot:
    
    gnuplot> load "hist.gp"

What do you notice? How would it change applying a weaker force constant, or a stronger one? 
You can try to change the force constant and/or use different force constants for every window by iterating over the k variable.

WHAM the using histograms, using the same parameters as set in the simulation

    wham start stop bins 1e-10 temperature 0 wham.meta PMF.dat

plot the obtained PMF stored in the `PMF.dat` file and compare it to PMF curves present in the literature.

