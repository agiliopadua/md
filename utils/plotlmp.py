#!/usr//bin/env python
# Plot quantities from log.lammps

import sys
import subprocess
import numpy as np
import matplotlib.pyplot as plt

# Read header and line numbers of start and end of thermo data
cmd = "grep -n -m1 Step log.lammps"
output = subprocess.run(cmd.split(), capture_output=True)
header = output.stdout.decode()
nskip = int(header.split(':')[0])

cmd = "grep -n -m1 Loop log.lammps"
output = subprocess.run(cmd.split(), capture_output=True)
foot = output.stdout.decode()
nread = int(foot.split(':')[0]) - nskip - 1

header = header.split()
header = header[1:]

if len(sys.argv) < 3:
    print('Plot thermo data from log.lammps')
    print('usage: plotlmp.py xcol ycol')
    print('columns are (start at 1):')
    print(header)
    sys.exit(1)

xcol = int(sys.argv[1]) - 1
ycol = int(sys.argv[2]) - 1

thermo = np.loadtxt("log.lammps", skiprows=nskip, max_rows=nread)
thermo = thermo.T        # we need to transpose

fix, ax = plt.subplots()

ax.plot(thermo[xcol], thermo[ycol])
ax.set_xlabel(header[xcol])
ax.set_ylabel(header[ycol])
plt.show()



