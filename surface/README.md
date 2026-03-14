# Simulation of water at the interface with graphene

## Objectives

The following example uses molecular dynamics (MD) simulations to study the interface between a liquid and a material. The level of description is all-atom, fully flexible interaction potentials.

Thes examples of application should allow you to develop skills in modelling heterogeneous systems at the atomistic level and in computing some of their properties, for example the structure of the interfacial layers (easy) or the contact angle (more challenging).

Detailed guidelines are given on how to build periodic systems containing a slab of a material and a film or a droplet of liquid. The aim is to learn how to build such systems from scratch, equilibrate them, run a trajectory, and finally compute some properties in post-treatment.

You are encouraged to go beyond the examples provided and test new things (different system sizes, other compounds) or compute different quantities (lifetimes in the interfacial layers).

Input files for nanocarbon materials are supplied.

----

## Requirements

- [OpenMM](https://openmm.org), molecular dynamics code that is mostly used through its Python interface
- [Packmol](https://m3g.github.io/packmol/), packs molecules in a box
- [VMD](https://www.ks.uiuc.edu/Research/vmd/), trajectory visualizer
- [VESTA](https://jp-minerals.org/vesta/en/), visualizer and editor of crystallographic files
- [fftool](https://github.com/paduagroup/fftool), builds an initial configuration and the force field for a system


----

## Simple system with a film of water on graphite

In this section we build and simulate a system consisting of graphene planes with a film of water. There will be several interfaces, namely between the material and the liquid, and the free surface of the liquid.

Although the unit cell of graphite corresponds to an hexagonal lattice, we will work with an orthorhombic (all angles 90°) simulation box.


### Create graphene planes from crystal structure

Download a CIF file for graphite from the [Crystallography Open Database](https://www.crystallography.net/): 9011577.cif


Using VESTA, under \<Edit\>\<Bonds\> choose each bond type on the table (there is just one type for graphite) and tick \<Do not search atoms beyond the boundary\>, then \<Apply\>.

Click \<Boundary...\> and set ranges of fractional coordinates: x(max) = 26.4, y(max) = 19.9, z(max) = 1. \<Apply\>

Add cutoff planes:

- (2 -1 0), distance from origin 33 x d
- (-2 1 0), distance from origin 0.1 x d

\<Apply\>. Verify that the edges of the graphene planes are matching, with no duplicate atoms (only the bonds across box boundaries should be missing).

Q. Count the number of unit cells along each perpendicular direction.

Check that you have 680 atoms per plane. You can choose z(max) to control the number of planes. For the following work we will use 4 planes, so set z(max) accordingly.

Then \<Export Data...\> to XYZ format (answer **No** to Save hidden atoms).

### Simulation box with periodic graphene planes

In the definition of the atom types within the force field (`nanocarbon.xml`), graphite C atoms are labelled type CG.

Copy the `.xyz` file with the coordinates of the graphene planes and replace all `C` atom names with `CG`:

    sed 's/C /CG/' < graph4.xyz > graph.xyz

Edit the `graph.xyz` file and add the force field file to the second line, after the name of the molecule:

    2720
    graphite nanocarbon.xml
    CG   0.000000    0.000000    1.677750
    [...]

Build the input files for OpenMM with the graphene planes of dimensions 41.888 x 42.678 Å (Q. Find the origin of these lengths); specify periodic bonds on the x and y directions:

    fftool 1 graph.xyz --box 41.888,42.678,50 --pbc xy

The `gr_pack.inp` file instructs Packmol to place the structure fixed at the origin:

    packmol < gr_pack.inp

Now create the input files for OpenMM:

    fftool 1 graph.xyz --box 41.888,42.678,50 --pbc xy --xml --mix a

With the planes stitched across box boundaries we expect 1.5 * 2720 = 4080 bonds.

Test a short run with just the graphene planes:

Graphite atoms have no electrostatic charge, therefore copy a usual `omm.py` file and edit it to replace the `createSystem()` line with just:

    system = forcefield.createSystem(modeller.topology, nonbondedCutoff=12.0*unit.angstrom)

We also want an anisotropic barostat in order to keep the length of the box along z fixed:

    pressure = (1.0, 1.0, 0.0)*unit.bar
    barostat = openmm.MonteCarloAnisotropicBarostat(pressure, temperature, True, True, False, 20)

Make sure that bond, angle and dihedral potentials use periodic boundary conditions (too "stich" the planes across box boudaries):

    # force settings before creating Simulation
    for i, f in enumerate(system.getForces()):
        f.setForceGroup(i)
        if f.getName() == 'HarmonicBondForce':
            f.setUsesPeriodicBoundaryConditions(True)
        if f.getName() == 'HarmonicAngleForce':
            f.setUsesPeriodicBoundaryConditions(True)
        if f.getName() == 'RBTorsionForce':
            f.setUsesPeriodicBoundaryConditions(True)

Also, start with zero velocities, which is more robust, by commenting out the line:

    # starting with velocities 0 is often more robust
    #sim.context.setVelocitiesToTemperature(temperature)

And, finally, comment out the energy minimization step, which is not necessary for the initial configuration, which is not too dense.

Then run

    ./omm-gr.py

Check energies and density to see if the box size adapts.

    vmd -e graph.vmd config.pdb traj.dcd


### Add a film of water

Place 1000 water molecules above the graphene planes:

    fftool 1 graph.xyz 1000 spce.zmat --box 41.888,42.678,80
    packmol < gr_water_pack.inp
    vmd simbox.xyz

    fftool 1 graph.xyz 1000 spce.zmat --box 41.888,42.678,80 --pbc xy --xml --mix a

Put back the settings concernimg electrostatic interactions and H-bonds in the `createSystem()` line.

Run a short test trajectory to make sure the system is ok:

    ./omm-gr.py &> omm.out &

Visualize:

    vmd -e graph.vmd config.pdb traj.dcd

Then run an equilibration of 500 ps at 300 K; visualize it using vmd;
check values of energy to see if the system is well equilibrated; run a trajectory from its last configuration for 1 ns saving a snapshot every 500 steps (2000 configurations).

----


## Droplet on a surface

Build a system with a graphite slab and a droplet of liquid, to measure the contact angle. An example input file for Packmol to arrange water molecules in a droplet is provided: `gr_drop_pack.inp`.

This system has not been tested for the stability of the drop after equilibration. It may require a larger graphite surface to avoid interactions of water with the periodic images. The number of water molecules and the size of the drop may also require adjustment.

