#!/usr/bin/env python
# Umbrella sampling for PMF calculation with WHAM

import sys
import datetime
import numpy as np

import openmm
from openmm import app
from openmm import unit
from openmmplumed import PlumedForce

field = 'field.xml'
config = 'config.pdb'
statefile = 'state-eq.xml'

temperature = 300.0*unit.kelvin
pressure = 1*unit.bar

# biasing force
k = 50.0*unit.kilojoule_per_mole/(unit.angstrom)**2
r0 = 4.0*unit.angstrom

print('#', datetime.datetime.now())
print()

print('#', field, config)
forcefield = app.ForceField(field)
pdb = app.PDBFile(config)

modeller = app.Modeller(pdb.topology, pdb.positions)
#print('#   adding extra particles')
#modeller.addExtraParticles(forcefield)

print('#  ', modeller.topology.getNumResidues(), 'molecules',
    modeller.topology.getNumAtoms(), 'atoms',
    modeller.topology.getNumBonds(), 'bonds')

lx = modeller.topology.getUnitCellDimensions().x
ly = modeller.topology.getUnitCellDimensions().y
lz = modeller.topology.getUnitCellDimensions().z
print('#   box', lx, ly, lz, 'nm')

system = forcefield.createSystem(modeller.topology, nonbondedMethod=app.PME,
    nonbondedCutoff=12.0*unit.angstrom, constraints=app.HBonds,
    ewaldErrorTolerance=1.0e-5)

print('# Nose-Hoover integrator', temperature)
integrator = openmm.NoseHooverIntegrator(temperature, 5/unit.picosecond, 1*unit.femtosecond)
#print('# Langevin integrator', temperature)
#integrator = openmm.LangevinIntegrator(temperature, 5/unit.picosecond, 1*unit.femtosecond)

print('#   barostat', pressure)
barostat = openmm.MonteCarloBarostat(pressure, temperature)
system.addForce(barostat)

bias = openmm.CustomBondForce("0.5*k*(r-r0)^2")
bias.addGlobalParameter("k", k)
bias.addGlobalParameter("r0", r0)
bias.addBond(1, 24)
system.addForce(bias)

platform = openmm.Platform.getPlatformByName('CUDA')
#platform = openmm.Platform.getPlatformByName('OpenCL')
#platform.setPropertyDefaultValue('Precision', 'mixed')
properties = {'Precision': 'single'}

# force settings before creating Simulation
for i, f in enumerate(system.getForces()):
    f.setForceGroup(i)

sim = app.Simulation(modeller.topology, system, integrator, platform, properties)

#sim.context.setPositions(modeller.positions)
#sim.context.setVelocitiesToTemperature(temperature)
print('# coordinates and velocities from', statefile)
sim.loadState(statefile)
sim.context.setTime(0)

#print('# coordinates and velocities from restart.chk')
#sim.loadCheckpoint('restart.chk')

state = sim.context.getState()
sim.topology.setPeriodicBoxVectors(state.getPeriodicBoxVectors())

platform = sim.context.getPlatform()
print('# platform', platform.getName())
for prop in platform.getPropertyNames():
    print('#  ', prop, platform.getPropertyValue(sim.context, prop))

state = sim.context.getState(getEnergy=True)
print('# PotentielEnergy', state.getPotentialEnergy())

for i, f in enumerate(system.getForces()):
    state = sim.context.getState(getEnergy=True, groups={i})
    print('#  ', f.getName(), state.getPotentialEnergy())

sim.reporters = []
sim.reporters.append(app.StateDataReporter(sys.stdout, 10000, step=True,
    speed=True, temperature=True, separator='\t',
    totalEnergy=True, potentialEnergy=True, density=True))
#sim.reporters.append(app.PDBReporter('traj.pdb', 10000))
#sim.reporters.append(app.DCDReporter('traj.dcd', 1000))
#sim.reporters.append(app.CheckpointReporter('restart.chk', 10000))

def dist(i, j, coords):
    return(np.sqrt(np.sum(np.power(coords[1] - coords[24], 2))))

distances = np.arange(2.5, 10.1, 0.5)*unit.angstrom

wham = open("wham.meta", "w")
wham.write("# metadata for PMF calculation with wham\n")

kval = k.value_in_unit(unit.kilocalorie_per_mole/(unit.angstrom)**2)

for r0 in distances:
    r0val = r0.value_in_unit(unit.angstrom)
    fts = open(f"tseries_{r0val}.dat", "w")
    fts.write(f"# tseries k {k}\n")
    fts.write(f"# step d\n")

    sim.context.setParameter("r0", r0)

    print(f"# equilibrating at r0: {r0}")
    state = sim.context.getState(getPositions=True, getEnergy=True, groups={8})
    coords = state.getPositions()
    d = dist(1, 24, coords).in_units_of(unit.angstrom)
    epot = state.getPotentialEnergy()
    print(f"# before: {d} {epot}")

    sim.step(50000)

    state = sim.context.getState(getPositions=True, getEnergy=True, groups={8})
    coords = state.getPositions()
    d = dist(1, 24, coords).in_units_of(unit.angstrom)
    epot = state.getPotentialEnergy()
    print(f"# after: {d} {epot}")

    print(f"# sampling at r0: {r0}")
    for i in range(15000):
        sim.step(50)
        state = sim.context.getState(getPositions=True)
        coords = state.getPositions()
        t = sim.context.getStepCount()
        d = dist(1, 24, coords).value_in_unit(unit.angstrom)
        fts.write(f"{t} {d}\n")

    fts.close()
    wham.write(f"tseries_{r0val}.dat {r0val} {kval}\n")

wham.close()

state = sim.context.getState(getPositions=True, getVelocities=True)
coords = state.getPositions()
sim.topology.setPeriodicBoxVectors(state.getPeriodicBoxVectors())
app.PDBFile.writeFile(sim.topology, coords, open('equil.pdb', 'w'))

sim.saveState('state.xml')

print()
print('#', datetime.datetime.now())
