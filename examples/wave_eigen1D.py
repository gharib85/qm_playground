"""
time independent 
solutions to the 1D Particle in different 
potentials
"""

import numpy as np
import sys
sys.path.append('..')
from qmp import *
from qmp.basis.gridbasis import onedgrid
from qmp.potential.pot_tools import create_potential
from qmp.tools.visualizations import wave_slideshow1D


### SIMULATION CELL ### 
cell = [[0., 120.0]]

### POTENTIAL ### 
pot = Potential( cell, f=create_potential(cell,
                                          name='double_well',
					  double_well_barrier=.008,
					  double_well_asymmetry=0.,
					  double_well_width=19.,
                                          ) )

### INITIALIZE MDOEL ###
## number of lowest eigenstates to be solved for
states = 30

tik1d = Model(
        ndim=1,
        mass=1.0,
        mode='wave',
        basis='onedgrid',
        solver='scipy',
        states=states,
        )

### SET POTENTIAL ### 
tik1d.set_potential(pot)

### BASIS ###
## spatial discretization
N = 512
b = onedgrid(cell[0][0], cell[0][1],N)
tik1d.set_basis(b)
print tik1d

tik1d.solve()

psi = tik1d.data.wvfn.psi
print tik1d.data.wvfn.E[:3]

### VISUALIZATION ###
wave_slideshow1D(tik1d.basis.x, psi, tik1d.pot(tik1d.basis.x))
