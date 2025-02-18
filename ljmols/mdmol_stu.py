#!/usr/bin/env python
# Molecular dynamics of 2-site LJ molecules

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
        bonds (array): dicts {i, j} with bonded atom indices
    """

    cell = '0.0 0.0 0.0'
    atoms = []
    bonds = []
    for line in open(pdbfile, 'r'):
        if 'CRYST1' in line:
            cell = line[6:].strip().split()
        elif 'ATOM' in line or 'HETATM' in line:
            atom = {}
            atom['name'] = line[76:78].strip()
            atom['x'] = float(line[30:38])
            atom['y'] = float(line[38:46])
            atom['z'] = float(line[46:54])
            atoms.append(atom)
        elif 'CONECT' in line:
            bond = {'i': -1, 'j': -1}
            i = int(line[6:11]) - 1
            j = int(line[12:17]) - 1
            if i < j:
                bond['i'] = i
                bond['j'] = j
            else:
                bond['i'] = j
                bond['j'] = i
            found = False
            for bd in bonds:
                if bd == bond:
                    found = True
            if not found:
                bonds.append(bond)

    box = np.array([float(cell[0]), float(cell[1]), float(cell[2])])
    atnames = [atom['name'] for atom in atoms]
    r = np.array([[atom['x'], atom['y'], atom['z']] for atom in atoms])
    return box, atnames, r, bonds


def writepdb(pdbfile, step, box, atnames, r, bonds, mode='a'):
    """Write or append PDB file

    Args:
        pdbfile (string): PDB file name
        step (int): time step
        box (ndarray): Lx, Ly, Lz box lengths
        atnames (list): N atom names
        r (ndarray): [N, 3] coordinates
        bonds (array): dicts {i, j} with bonded atom indices
        mode (str, optional): 'w' write, 'a' append. Defaults to 'a'
    """

    if mode not in ('a', 'w'):
        print('wrong file access mode in writepdb()')
        sys.exit(1)
    with open(pdbfile, mode) as pdb:
        pdb.write('TITLE     LJ molecules\n')
        pdb.write(f'REMARK    timestep {step}\n')
        pdb.write(f'CRYST1 {box[0]:8.3f} {box[1]:8.3f} {box[2]:8.3f}'\
                '  90.00  90.00  90.00 P1          1\n')
        for i in range(len(atnames)):
            pdb.write('HETATM{0:5d} {1:4s} {2:3s}  {3:4d}    '\
                      '{4:8.3f}{5:8.3f}{6:8.3f}  1.00  0.00          {7:>2s}\n'.format(
                        i+1, atnames[i], 'UNL', i+1, r[i, 0], r[i, 1], r[i, 2], atnames[i]))
        for bd in bonds:
            pdb.write('CONECT{0:5d}{1:5d}\n'.format(bd['i'] + 1, bd['j'] + 1))
        pdb.write('END\n')

# -------------------------------------

# Units:
#   mass [g/mol]
#   length [A]
#   time [fs]
#   temperature [K]
#   energy [kJ/mol]
#   force [(kJ/mol)/A]


def ljparams(atnames, ffnonbond):
    """Set non-bonded LJ parameters 

    Args:
        atnames (array): N atom names
        ffnonbond (dict): nested dict {m, sig, eps} for each atom type

    Returns:
        m (ndarray): column array with N atomic masses
        sig (ndarray): N LJ sigma
        eps (ndarray): N LJ epsilon
    """

    natom = len(atnames)
    m   = np.zeros(natom)
    sig = np.zeros(natom)
    eps = np.zeros(natom)
    for i in range(natom):
        m[i]   = ffnonbond[atnames[i]]['m']
        sig[i] = ffnonbond[atnames[i]]['sig']
        eps[i] = ffnonbond[atnames[i]]['eps']
    m = m[:, np.newaxis]
    return m, sig, eps


def topology(atnames, bonds, ffbond):
    """Set bonds between atoms in molecules and exclusion lists

    Args:
        atnames (array): N atom names
        bonds (array): dicts {i, j} with bonded atom indices
        ffbond (dict): nested dict with {'X-Y', r0, kr} for each bond type

    Returns:
        bonds (array): dicts {i, j, r0, kr} for all bonds
        excl (array): [N, i] exclusion list of bonded atom indices for each atom
    """

    for bd in bonds:
        i = bd['i']
        j = bd['j']
        bdname = f'{atnames[i]}-{atnames[j]}'
        if bdname in ffbond.keys():
            bd['r0'] = ffbond[bdname]['r0']
            bd['kr'] = ffbond[bdname]['kr']

    excl = []
    for i in range(len(atnames)):
        excl.append([])
        for bd in bonds:
#           ...                         # TODO build exclusion lists!

    return bonds, excl


def initvel(m, temp):
    """Set initial velocities

    Args:
        m (array): atom masses
        temp (float): temperature (K)

    Returns:
        v (ndarray): [N, 3] velocities
    """

    random.seed(1234)
    natom = len(m)
    v = np.zeros((natom, 3))
    for i in range(natom):
        fact = (cst.R * temp / (m[i][0] * 1e-3))**0.5 * 1e-5 # m [kg/mol], v [A/fs]
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


def epot_pair(r, sig, eps, excl, box, rcut):
    """Compute non-bonded potential energy

    Args:
        r (ndarray): [N, 3] positions
        sig (ndarray): N LJ sigma
        eps (ndarray): N LJ epsilon
        excl (array): exclusion lists
        box (ndarray): box lengths
        rcut (float): cutoff radius

    Returns:
        epot (float): non-bonded potential energy
    """

    natom = len(r)
    rcut2 = rcut*rcut
    epot = 0.0
    for i in range(natom - 1):
        for j in range(i + 1, natom):
            if j in excl[i]:
                continue
            rij = r[i] - r[j]
            rij -= np.rint(rij/box) * box
            rsq = np.sum(rij*rij)
            if rsq > rcut2:
                continue
            sigij = (sig[i] + sig[j])/2
            epsij = (eps[i] * eps[j])**0.5
            sr2 = sigij * sigij / rsq
            sr6 = sr2 * sr2 * sr2
            sr12 = sr6 * sr6
            epot += 4 * epsij * (sr12 - sr6)
    return epot


def forces_pair(r, sig, eps, box, rcut, excl):
    """Compute non-bonded forces (LJ potential)

    Args:
        r (ndarray): [N, 3] positions
        sig (ndarray): N LJ sigma
        eps (ndarray): N LJ epsilon
        box (ndarray): box lengths
        rcut (float): cutoff radius
        excl (array): exclusion list of bonded atoms for each atom

    Returns:
        f (ndarray): [N, 3] non-bonded forces
        vir (float): the virial
    """

    natom = len(r)
    f = np.zeros((natom, 3))
    vir = 0.0
    rcut2 = rcut*rcut
    for i in range(natom - 1):
        for j in range(i + 1, natom):
#           ...
            fij = np.array([0.0, 0.0, 0.0])     # TODO replace by expression
            f[i] += fij
            f[j] -= fij
            vir += np.sum(rij * fij)
    return f, vir


def epot_bond(r, bonds, box):
    """Compute bonded potential energy

    Args:
        r (ndarray): [N, 3] positions
        bonds (array): {i, j, r0, kr} for all bonds
        excl (array): exclusion list

    Returns:
        epot (float): bonded potential energy
    """    

    epot = 0.0
    for bd in bonds:
        rij = r[bd['i']] - r[bd['j']]   # [rij_x, rij_y, rij_z]
        rij -= np.rint(rij/box) * box
        rbd = np.sqrt(np.sum(rij*rij))
        epot += 0.5 * bd['kr'] * (rbd - bd['r0'])**2
    return epot


def forces_bond(r, bonds, box):
    """Compute bonded forces (harmonic bonds)

    Args:
        r (ndarray): [N, 3] positions
        bonds (array): {i, j, r0, kr} for all bonds
        box (ndarray): box lengths

    Returns:
        f (ndarray): [N, 3] bonded forces
    """

    natom = len(r)
    f = np.zeros((natom, 3))
    for bd in bonds:
        rij = r[bd['i']] - r[bd['j']]   # [rij_x, rij_y, rij_z]
#       ...
        fij = np.array([0.0, 0.0, 0.0])     # TODO replace by expression
        f[bd['i']] += fij
        f[bd['j']] -= fij
    return f


def pressure(natom, vir, temp, box):
    """Compute pressure from virial

    Args:
        natom (int): number of atoms in system
        vir (float): virial
        temp (float): temperature
        box (ndarray): 3 box lengths

    Returns:
        pressure [bar]
    """

    vol = np.prod(box) * 1e-30  # [m3]
    p = (natom * cst.k * temp / vol \
        + vir * 1e3 / (3 * vol * cst.Avogadro)) * 1e-5 # [bar]
    return p

# -------------------------------------

def main():

    parser = argparse.ArgumentParser(description='Molecular dynamics of 2-site LJ molecules')
    parser.add_argument('--ini', help='PDB file with initial configuration')
    parser.add_argument('--last', default='last.pdb', help='final configuration (default: last.pdb)')
    parser.add_argument('--ffbond', default='ffbond.json', help='force field bonded parameters (default: ffbond.json)')
    parser.add_argument('--ffnonbond', default='ffnonbond.json', help='force field non-bonded parameters (default: ffnonbond.json)')
    parser.add_argument('--sim', default='sim.json', help='simulation conditions (default: sim.json)')
    parser.add_argument('--traj', default='traj.pdb', help='trajectory (default: traj.pdb)')
    args = parser.parse_args()

    if not args.ini:
        parser.print_help()
        print('\nError: supply initial configuration file')
        sys.exit(1)

    box, atnames, r, bonds = readpdb(args.ini)
    nmol = len(atnames) - len(bonds)

    with open(args.ffnonbond) as f:
        forcefield = json.load(f)
    m, sig, eps = ljparams(atnames, forcefield)
  
    with open(args.ffbond) as f:
        ffbond = json.load(f)
    bonds, excl = topology(atnames, bonds, ffbond)

    with open(args.sim) as f:
        sim = json.load(f)
    tstep = sim['tstep']
    rcut = sim['rcut']

    step = 0
    v = initvel(m, sim['temp'])

    print('# Step          Etot          Ekin          Epot         Ebond         Epair     Temp    Press')
    ebond = epot_bond(r, bonds, box)
    epair = epot_pair(r, sig, eps, excl, box, rcut)
    ekin, temp = ekinetic(m, v)
    epot = epair + ebond
    etot = ekin + epot
    fbond = forces_bond(r, bonds, box)
    fpair, vir = forces_pair(r, sig, eps, box, rcut, excl)
    f = fbond + fpair
    press = pressure(nmol, vir, temp, box)

    print(f'{0:6d} {etot:13.5f} {ekin:13.5f} {epot:13.5f} {ebond:13.5f} {epair:13.5f} {temp:8.1f} {press:8.1f}')
    sys.stdout.flush()
    writepdb(args.traj, step, box, atnames, r, bonds, 'w')

    tstart = time.perf_counter_ns()
    for step in range(1, sim['steps']+1):

#       ...                             # TODO integrator
        
        if step % sim['save'] == 0:
            ebond = epot_bond(r, bonds, box)
            epair = epot_pair(r, sig, eps, excl, box, rcut)
            ekin, temp = ekinetic(m, v)
            epot = epair + ebond
            etot = ekin + epot
            press = pressure(nmol, vir, temp, box)
                    
            print(f'{step:6d} {etot:13.5f} {ekin:13.5f} {epot:13.5f} {ebond:13.5f} {epair:13.5f} {temp:8.1f} {press:8.1f}')
            sys.stdout.flush()
            writepdb(args.traj, step, box, atnames, r, bonds, 'a')

    tend = time.perf_counter_ns()
    nsday = sim['steps']*tstep*1e-6 / ((tend - tstart)*1e-9/86400)
    print(f'# {nsday:.1f} ns/day')

    writepdb(args.last, step, box, atnames, r, bonds, 'w')

if __name__ == '__main__':
    main()
