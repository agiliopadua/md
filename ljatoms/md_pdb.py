#!/usr/bin/env python
# Molecular dynamics of LJ atoms

import sys
import numpy as np


def readpdb(pdbfile):
    """Read PDB file

    Args:
        pdbfile (string): PDB file

    Returns:
        box (ndarray): Lx, Ly, Lz box lengths
        atnames (list): array with N atom names
        r (ndarray): [N,3] array with coordinates
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
    natom = len(atoms)

    box = np.array([float(cell[0]), float(cell[1]), float(cell[2])])
    atnames = [atom['name'] for atom in atoms]
    r = np.array([[atom['x'], atom['y'], atom['z']] for atom in atoms])
    return box, atnames, r


def writepdb(pdbfile, step, box, atnames, r, mode='a'):
    """Write PDB file

    Args:
        pdbfile (string): PDB file name
        step (int): time step
        box (ndarray): Lx, Ly, Lz box lengths
        atnames (list): array with atom names
        r (ndarray): [N,3] array with N coordinates
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

def main():

    if len(sys.argv) == 1:
        print(sys.argv[0] + ' pdbfile' + ' outfile' + ' [a|w]')
        exit()

    infile = sys.argv[1]
    outfile = sys.argv[2]
    if len(sys.argv) == 4:
        mode = sys.argv[3]
    else:
        mode = 'a'

    box, atnames, r = readpdb(infile)
    writepdb(outfile, box, atnames, r, mode)

if __name__ == '__main__':
    main()
