# Gromacs tutorial

Simulation of a protein using Gromacs, following the [lysozyme in water](http://www.mdtutorials.com/gmx/lysozyme/) tutorial by J. Lemkul.

## Calling Gromacs

On the CBPSMN the Gromacs binary is `/usr/bin/gmx` and should be directly accessible:

    gmx

## Obtaining the protein structure

PDB files of proteins can be obtained from the [RCSB Protein Data Bank](www.rcsb.org). We will download the structure of the immunoglobulin binding domain of streptococcal protein G, 2GB1, which has 56 residues (aminoacids):

    wget http://www.rcsb.org/pdb/files/2GB1.pdb.gz
    gunzip 2GB1.pdb.gz

You can visualize it using VMD (drawing method: NewRibbons; coloring method: ResType).

This structure was obtain from NMR.


## Choosing a force field and preparing the box

Gromacs is in fact a set of tools. We first use `pdb2gmx`. Each tool may have many options

    gmx pdb2gmx -h

Let us create a `.gro` file from the pdb choosing a water model (SPC/E):

    gmx pdb2gmx -f 2GB1.pdb -o protein.gro -water spce

You will be prompted to choose a force field. Pick `15: OPLS-AA/L`, for example.

You will get an error:

    Fatal error:
    Atom HB3 in residue MET 1 was not found in rtp entry MET with 19 atoms
    while sorting atoms.

This is common in structures obtained from NMR orbecause of different protonation states. In other cases there may be some hydration water molecules that need to be removed. Processing steps are often necessary. Let's ignore hydrogens from the initial structure and Gromacs will add them back:

    gmx pdb2gmx -f 2GB1.pdb -o protein.gro -water spce -ignh

This should run successfully. The output to the terminal told us that the total charge is -4 e. This net charge needs to be compensated by counterions later.

You can visualize the `.gro` file with VMD anc check that H atoms are there.

As a result of this step a topology file `topol.top` was created, which includes force field parameters, connectivity, system composition, etc. Sections are labeled `[ atoms ]', '[ bonds ]`, and so on.

Another file `posre.itp` was also created. This file specifies position restrains on the protein atoms (for alter use). 

Let us define a cubic box for the system:

    gmx editconf -f protein.gro -o protein_newbox.gro -c -d 1.0 -bt cubic

This centers the box around the protein `-c` and leaves 1 nm from the edges `-d 1.0`. You can see the box size in the output to the terminal and in VMD you can use `pbc box` at the prompt to show the box.


## Solvating the protein

    gmx solvate -cp protein_newbox.gro -cs spc216.gro -o protein_solv.gro -p topol.top

This fills the box with water molecules, using a pre-equilibrated configuration of liquid water (with the SPC model, which is fine). Display the output `.gro` with VMD.

Now is the time to add the counterions. For that a file named `ions.mdp` is required as input, to create another file called `ions.tpr`:

    gmx grompp -f ions.mdp -c protein_solv.gro -p topol.top -o ions.tpr

and now the ions can be generated into the system:

    gmx genion -s ions.tpr -o protein_solv_ions.gro -p topol.top -pname NA -nname CL -neutral

Choose group `13 (   SOL)` for the continuous group of solvent molecules. Four water molecules will be replaced by sodium cations.


## Energy minimization

The `minim.mdp` file has instructions for the initial energy minimization of the system. The `.mdp` files specify the simulation conditions, so study them, since they are the main Gromacs input files that users modify to suit their needs.

    gmx grompp -f minim.mdp -c protein_solv_ions.gro -p topol.top -o em.tpr
    gmx mdrun -nt 8 -v -deffnm em

This uses 8 threads for parallel execution (check with `lscpu` how many cores your machine has).
Energy minimization steps will run until the maximum force is below 1000 kJ mol<sup>-1</sup> nm<sup>-1</sup>. A few hundred steps are usually needed.

Use the `energy` command to retrieve the potential energy along the minimization:

    gmx energy -f em.edr -o potential.xvg

Choose `10` (then enter to exit). The file can be plotted using the Grace program (not installed on the CBP machines apparently) or by some other means.

The minimized structure should be good to start an equilibration run.


## Equilibration run

First let us perform an equilibration run at constant NVT. Study the `nvt.mdp` file, which is more detailed than the equilibration input file. Position restraints are read from the `posres.itp` file (``behind the curtains'') and are used to prevent the protein from changing conformation during the equilibration, when the solvation environment is not representative.

    gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr

Run 50 000 steps with timestep 2 fs (use a max of CPU cores):

    gmx mdrun -nt 16 -v -deffnm nvt

The performance in ns/day and other information are printed to the screen.

Use the `energy` command to retrieve the temperature along the equilibration:

    gmx energy -f nvt.edr -o temperature.xvg

Choose `16` (enter to exit) and plot.

Now we can run a final equilibration at constant pressure, NpT, for the system to reach its density. Study the `npt.mdp` file to see the differences (`continuation = yes` to start from the last configuration; pressure coupling).

    gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
    gmx mdrun -nt 16 -v -deffnm npt

Retrieve pressure and density (choose `18` and `24`):

    gmx energy -f npt.edr -o p_rho.xvg

Observe the averages and fluctuations.

VMD can read the trajectory `.xtc` files:

    vmd npt.gro npt.xtc

For a nice view you can create different representations for selections `protein`, `water`, `ions`; the first in `NewRibbons` (colouring by `ResType`), the second in `lines` or `points` and the ions in `VDW`.


## Production run

The production run uses essentially the same settings as the NPT equilibration, except that the position restraints are not applied (and bulky `.trr` trajectory files are not written). An example of a 500 ps run is given in the file `md.mdp`.

    gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md.tpr

Because this run will take some time, we send it to background

    nohup gmx mdrun -nt 16 -v -deffnm md > run.out &

we can check progress with (Ctrl-C to exit)

    tail -f run.out

Look at the trajectory using VMD:

    vmd md.gro md.xtc

Create different representations for selections `protein`, `water`, `ions`; the first in `NewRibbons` (colouring by `ResType`), the second in `lines` or `points` and the ions in `VDW`.


## Trajectory analysis

To center the protein in the box during the trajectory and to unwrap coordinates:

    gmx trjconv -s md.tpr -f md.xtc -o md_noPBC.xtc -pbc mol -center

Select `1` (Protein) as the group to be centered and `0` (System) for output.

To calculate the RMSD of the protein:

    gmx rms -s md.tpr -f md_noPBC.xtc -o rmsd.xvg -tu ps

Choose `4` (Backbone) for both the least-squares fit and the group for RMSD calculation.

Calculate the radius of gyration of the protein along the trajectory:

    gmx gyrate -s md.tpr -f md_noPBC.xtc -o gyrate.xvg

## END
