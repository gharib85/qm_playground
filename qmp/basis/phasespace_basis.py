#qmp.basis.phasespace_basis
#
#    qm_playground - python package for dynamics simulations
#    Copyright (C) 2016  Reinhard J. Maurer 
#
#    This file is part of qm_playground.
#    
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>#
"""
initialization arrays for classical dynamics
"""


from qmp.basis.basis import basis
from qmp.tools.utilities import *
import numpy as np


class phasespace(basis):
    """
    initialization array in phase space
    """

    def __init__(self, coordinates, velocities, masses):
        """
        
        """

        basis.__init__(self)
        
        self.r = np.array(coordinates)
        self.npar = self.r.shape[0]
        if self.r.size == self.npar:
            self.ndim = 1
        else:
            self.ndim = self.r.shape[1]
        self.v = np.array(velocities)
        self.masses = np.array(masses)
        
        if self.masses.size != self.masses.shape[0]:
            raise ValueError('Masses must be given as List of integers')
        elif (self.masses.size != self.npar) or \
             (self.r.shape != self.v.shape):
            raise ValueError('Please provide consistent masses, coordinates, and velocities')
        elif self.ndim > 2:
            raise NotImplementedError('Only 1D and 2D implemented yet')
        

    def __eval__(self):
        return self.r, self.v

    def get_kinetic_energy(self, mass, v):
        return mass*np.sum(v*v)/2.

    def get_potential_energy(self, r, pot):
        if self.ndim == 1:
            return pot(r)
        elif self.ndim == 2:
            return pot(r[0],r[1])
            
    
    def get_forces(self, r, pot):
        if self.ndim == 1:
            return -1.*num_deriv(pot, r)
        elif self.ndim == 2:
            return -1.*num_deriv_2D(pot, *r)
    
