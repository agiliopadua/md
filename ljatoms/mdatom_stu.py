#!/usr/bin/env python
# Molecular dynamics of LJ atoms

import sys
import argparse
import json
import time
import random
import numpy as np
import scipy.constants as cst

# -------------------------------------

def readpdb(pdbfile):
    """Read PDB file

    Args:
        pdbfile (string): PDB file

    Returns:
        box (ndarray): Lx, Ly, Lz box lengths
        atnames (list): N atom names
        r (ndarray): [N, 3] coordinates
    """

    cell = '0.0 0.0 0.0'
    atoms = []
    for line in open(pdbfile, 'r'):
        if 'CRYST1' in line:
            cell = line[6:].strip().split()
        if 'ATOM' in line or 'HETATM' in line:
            atom = {}
            atom['name'] = line[76:78].strip()
            atom['x'] = float(line[30:38])
            atom['y'] = float(line[38:46])
            atom['z'] = float(line[46:54])
            atoms.append(atom)

    box = np.array([float(cell[0]), float(cell[1]), float(cell[2])])
    atnames = [atom['name'] for atom in atoms]
    r = np.array([[atom['x'], atom['y'], atom['z']] for atom in atoms])
    return box, atnames, r


def writepdb(pdbfile, step, box, atnames, r, mode='a'):
    """Write or append PDB file

    Args:
        pdbfile (string): PDB file name
        step (int): time step
        box (ndarray): Lx, Ly, Lz box lengths
        atnames (list): N atom names
        r (ndarray): [N, 3] coordinates
        mode (str, optional): 'w' write, 'a' append. Defaults to 'a'
    """

    if mode not in ('a', 'w'):
        print('wrong file access mode in writepdb()')
        sys.exit(1)
    with open(pdbfile, mode) as pdb:
        pdb.write('TITLE     LJ atoms\n')
        pdb.write(f'REMARK    timestep {step}\n')
        pdb.write(f'CRYST1 {box[0]:8.3f} {box[1]:8.3f} {box[2]:8.3f}'\
                '  90.00  90.00  90.00 P1          1\n')
        for i in range(len(atnames)):
            pdb.write('HETATM{0:5d} {1:4s} {2:3s}  {3:4d}    '\
                      '{4:8.3f}{5:8.3f}{6:8.3f}  1.00  0.00          {7:>2s}\n'.format(
                        i+1, atnames[i], 'UNL', i+1, r[i, 0], r[i, 1], r[i, 2], atnames[i]))
        pdb.write('END\n')

# -------------------------------------

# Units:
#   mass [g/mol]
#   length [A]
#   time [fs]
#   temperature [K]
#   energy [kJ/mol]
#   force [(kJ/mol)/A]


def ljparams(atnames, forcefield):
    """Set non-bonded LJ parameters

    Args:
        atnames (array): N atom names
        forcefield (dict): nested dict {m, sig, eps} for each element

    Returns:
        m (ndarray): column array with M atomic masses
        sig (ndarray): N LJ sigma
        eps (ndarray): N LJ epsilon
    """

    natom = len(atnames)
    m   = np.zeros(natom)
    sig = np.zeros(natom)
    eps = np.zeros(natom)
    for i in range(natom):
        m[i]   = forcefield[atnames[i]]['m']
        sig[i] = forcefield[atnames[i]]['sig']
        eps[i] = forcefield[atnames[i]]['eps']
    m = m[:, np.newaxis]
    return m, sig, eps


def initvel(m, temp):
    """Set initial velocities

    Args:
        m (ndarray): column array with N atomic masses
        temp (float): temperature

    Returns:
        v (ndarray): [N, 3] velocities
    """

    random.seed(1234)
    natom = len(m)
    v = np.zeros((natom, 3))
    for i in range(natom):
        fact = 0.0                      # TODO replace by expression
        v[i, 0] = fact * random.gauss()
        v[i, 1] = fact * random.gauss()
        v[i, 2] = fact * random.gauss()
    return v

# -------------------------------------

def ekinetic(m, v):
    """Compute kinetic energy

    Args:
        m (ndarray): column array with N atomic masses
        v (ndarray): [N, 3] velocities

    Returns:
        kinetic energy (float)
        temperature (float)
    """

    ekin = 0.0                          # TODO replace by expression
    temp = 0.0                          # TODO replace by expression
    return ekin, temp


def epotential(r, sig, eps, box, rcut):
    """Compute potential energy

    Args:
        r (ndarray): positions
        sig (ndarray): sigma LJ parameters
        eps (ndarray): epsilon LJ parameters
        box (ndarray): box lengths
        rcut (float): cutoff radius

    Returns:
        epot (float): potential energy
    """

    natom = len(r)
    rcut2 = rcut*rcut
    epot = 0.0
    for i in range(natom - 1):
        for j in range(i + 1, natom):
            rij = r[j] - r[i]           # [rij_x, rij_y, rij_z]
#           ...
            epot += 0.0                 # TODO replace by expression
    return epot


def forces(r, sig, eps, box, rcut):
    """Compute forces (LJ potential)

    Args:
        r (ndarray): [N, 3] positions
        sig (ndarray): N LJ sigma
        eps (ndarray): N LJ epsilon
        box (ndarray): box lengths
        rcut (float): cutoff radius

    Returns:
        f (ndarray): [N, 3] forces
    """

    natom = len(r)
    f = np.zeros((natom, 3))
    rcut2 = rcut*rcut
    for i in range(natom - 1):
        for j in range(i + 1, natom):
            rij = r[j] - r[i]           # [rij_x, rij_y, rij_z]
#           ...
            fij = [0.0, 0.0, 0.0]       # TODO replace by expression
#           ...
    return f


def pressure(r, f, temp, box):
    """Compute pressure from virial

    Args:
        r (ndarray): [N, 3] coordinates
        f (ndarray): [N, 3] forces
        temp (float): temperature
        box (ndarray): 3 box lengths

    Returns:
        pressure [bar]
    """

    n = len(r)
    vol = np.prod(box) * 1e-30  # [m3]
    virial = np.sum(f * r) / 2
    p = (n * cst.k * temp / vol \
      + virial * 1e3 / (3 * vol * cst.Avogadro)) * 1e-5 # [bar]
    return p


# -------------------------------------

def main():

    parser = argparse.ArgumentParser(description='Molecular dynamics of LJ atoms')
    parser.add_argument('--ini', help='PDB file with initial configuration')
    parser.add_argument('--last', default='last.pdb', help='final configuration (default: last.pdb)')
    parser.add_argument('--ff', default='ff.json', help='force field parameters (default: ff.json)')
    parser.add_argument('--sim', default='sim.json', help='simulation conditions (default: sim.json)')
    parser.add_argument('--traj', default='traj.pdb', help='trajectory (default: traj.pdb)')
    args = parser.parse_args()

    if not args.ini:
        parser.print_help()
        print('\nError: supply initial configuration file')
        sys.exit(1)

    box, atnames, r = readpdb(args.ini)
  
    with open(args.ff) as f:
        forcefield = json.load(f)
    m, sig, eps = ljparams(atnames, forcefield)
  
    with open(args.sim) as f:
        sim = json.load(f)
    tstep = sim['tstep']
    rcut = sim['rcut']

    step = 0
    v = initvel(m, sim['temp'])

    print('# Step      Etotal        Ekin          Epot        Temp     Press')
    epot = epotential(r, sig, eps, box, rcut)
    ekin, temp = ekinetic(m, v)
    etot = ekin + epot
    f = forces(r, sig, eps, box, rcut)
    press = pressure(r, f, temp, box)
    print(f'{0:6d} {etot:13.6f} {ekin:13.6f} {epot:13.6f} {temp:8.1f} {press:8.1f}')
    sys.stdout.flush()
    writepdb(args.traj, step, box, atnames, r, 'w')

    tstart = time.perf_counter_ns()
    for step in range(1, sim['steps']+1):

#       ...                             # TODO integrator

        if step % sim['save'] == 0:
            epot = epotential(r, sig, eps, box, rcut)
            ekin, temp = ekinetic(m, v)
            etot = ekin + epot
            press = pressure(r, f, temp, box)
            print(f'{step:6d} {etot:13.6f} {ekin:13.6f} {epot:13.6f} {temp:8.1f} {press:8.1f}')
            sys.stdout.flush()
            writepdb(args.traj, step, box, atnames, r, 'a')

    tend = time.perf_counter_ns()
    nsday = sim['steps']*tstep*1e-6 / ((tend - tstart)*1e-9/86400)
    print(f'# {nsday:.1f} ns/day')

    writepdb(args.last, step, box, atnames, r, 'w')

if __name__ == '__main__':
    main()
