#!/usr/bin/env python

import sys
import datetime
import numpy as np

import openmm
from openmm import app
from openmm import unit

field = 'field.xml'
config = 'config.pdb'
#statefile = 'state-eq.xml'

temperature = 300.0*unit.kelvin
pressure = 1*unit.bar

print('#', datetime.datetime.now())
print()

print('#', field, config)
forcefield = app.ForceField(field)
pdb = app.PDBFile(config)

modeller = app.Modeller(pdb.topology, pdb.positions)

print('#  ', modeller.topology.getNumResidues(), 'molecules',
    modeller.topology.getNumAtoms(), 'atoms',
    modeller.topology.getNumBonds(), 'bonds')

box = modeller.topology.getUnitCellDimensions()
print('#   box', box.x, box.y, box.z, 'nm')

system = forcefield.createSystem(modeller.topology, nonbondedMethod=app.PME,
    nonbondedCutoff=12.0*unit.angstrom, constraints=app.HBonds,
    ewaldErrorTolerance=1.0e-5)

#print('# Nose-Hoover integrator', temperature)
#integrator = openmm.NoseHooverIntegrator(temperature, 5/unit.picosecond,
#    1*unit.femtosecond)
print('# Langevin integrator', temperature)
integrator = openmm.LangevinIntegrator(temperature, 5/unit.picosecond,
    1*unit.femtosecond)

print('#   barostat', pressure)
barostat = openmm.MonteCarloBarostat(pressure, temperature)
system.addForce(barostat)

platform = openmm.Platform.getPlatformByName('CUDA')
#platform = openmm.Platform.getPlatformByName('OpenCL')
#properties = {'DeviceIndex': '1', 'Precision': 'mixed'}
properties = {'Precision': 'single'}

# force settings before creating Simulation
for i, f in enumerate(system.getForces()):
    f.setForceGroup(i)

sim = app.Simulation(modeller.topology, system, integrator, platform, properties)

sim.context.setPositions(modeller.positions)
# starting with velocities 0 is often more robust
sim.context.setVelocitiesToTemperature(temperature)

#print('# coordinates and velocities from', statefile)
#sim.loadState(statefile)

#print('# coordinates and velocities from restart.chk')
#sim.loadCheckpoint('restart.chk')

#state = sim.context.getState()
#sim.topology.setPeriodicBoxVectors(state.getPeriodicBoxVectors())

platform = sim.context.getPlatform()
print('# platform', platform.getName())
for prop in platform.getPropertyNames():
    print('#  ', prop, platform.getPropertyValue(sim.context, prop))

state = sim.context.getState(getEnergy=True)
print('# PotentielEnergy', state.getPotentialEnergy())

for i, f in enumerate(system.getForces()):
    state = sim.context.getState(getEnergy=True, groups={i})
    print('#  ', f.getName(), state.getPotentialEnergy())

print("# Minimizing energy...")
sim.minimizeEnergy()

state = sim.context.getState(getEnergy=True)
print('# PotentielEnergy', state.getPotentialEnergy())

for i, f in enumerate(system.getForces()):
    state = sim.context.getState(getEnergy=True, groups={i})
    print('#  ', f.getName(), state.getPotentialEnergy())

sim.reporters = []
sim.reporters.append(app.StateDataReporter(sys.stdout, 1000, step=True,
    speed=True, temperature=True, separator='\t',
    totalEnergy=True, potentialEnergy=True, density=True))

sim.reporters.append(app.DCDReporter('traj.dcd', 1000, enforcePeriodicBox=False))

#sim.reporters.append(app.CheckpointReporter('restart.chk', 10000))

sim.step(200000)

for i, f in enumerate(system.getForces()):
    state = sim.context.getState(getEnergy=True, groups={i})
    print('#  ', f.getName(), state.getPotentialEnergy())

state = sim.context.getState(getPositions=True, getVelocities=True, getIntegratorParameters=False)
coords = state.getPositions()
sim.topology.setPeriodicBoxVectors(state.getPeriodicBoxVectors())
app.PDBFile.writeFile(sim.topology, coords, open('equil.pdb', 'w'))

sim.context.setTime(0)
sim.context.setStepCount(0)
sim.saveState('state-eq.xml')
print('# state saved to state-eq.xml')

print()
print('#', datetime.datetime.now())
