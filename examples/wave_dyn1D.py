import numpy as np
from qmp.potential import Potential
from qmp.integrator.dyn_tools import create_gaussian
from qmp.potential import preset_potentials
from qmp.tools.visualizations import *
from qmp.integrator.waveintegrators import PrimitivePropagator
from qmp.integrator.waveintegrators import EigenPropagator
from qmp.integrator.waveintegrators import SOFT_Propagator
from qmp.systems.grid import Grid1D
from qmp import Model


# SIMULATION CELL
cell = [[-10., 20.0]]
N = 256
mass = 1800
dt = 25


# POTENTIAL
wall = preset_potentials.Wall(1, position=[5.],
                              width=np.array([2]), height=[0.001])
pot = Potential(cell, f=wall())
# integrator = SOFT_Propagator(dt)
integrator = SOFT_Propagator(dt)
# integrator = PrimitivePropagator(dt)
integrator = EigenPropagator(dt)
system = Grid1D(mass, cell[0][0], cell[0][1], N)

# initial wave functions
sigma = 1./2.
psi_0 = create_gaussian(system.x, x0=0., p0=2.0, sigma=sigma)
psi_0 /= np.sqrt(np.conjugate(psi_0).dot(psi_0))

system.set_initial_wvfn(psi_0)

# NUMBER OF BASIS STATES
# for propagation in eigenbasis
states = 128

# INITIALIZE MODEL
tik1d = Model(
        system=system,
        potential=pot,
        integrator=integrator,
        mode='wave',
        states=200
        )

print(tik1d)
print('Grid points:', N, '\n')

# INITIAL WAVE FUNCTION AND DYNAMICS PARAMETERS
# time step, number of steps
steps = 3E2

# EVOLVE SYSTEM
tik1d.run(steps, output_freq=10)

# GATHER INFO
# info time evolution
psi_t = tik1d.data.psi_t
E_t = tik1d.data.E_t
# E_kin_t = tik1d.data.E_kin_t
# E_pot_t = tik1d.data.E_pot_t
rho_t = tik1d.data.rho_t
# rho_mean = tik1d.data.rho_mean

norm_t = np.sum(rho_t, 1)

V_x = tik1d.potential(tik1d.system.x)

## view animation
# print(E_t[:, 0])
wave_movie1D(tik1d.system.x, rho_t[:, :N], V_x, dt=dt, E_arr=E_t,
        rho_tot_arr=norm_t)
            # E_kin_arr=E_kin_t, E_pot_arr=E_pot_t)
             #rho_tot_arr=norm_t)#, E_kin_arr=E_kin_t, E_pot_arr=E_pot_t)
