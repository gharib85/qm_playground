#    qmp.potential.potential
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
class potential
"""

from qmp.tools import derivatives
import numpy as np


class Potential:
    """
    Defines Potential and all operations on it. Functions for the
    potential energy, the first and second derivative, and for possible
    excited states and scalar and vectorial derivative couplings must
    be passed explicitly.
    """

    def __init__(self, cell=[[0., 1.]], f=lambda a: 0, firstd=None, n=1,
                 secondd=None, d1=None, d2=None):
        """
        Initializes potential
        Input
            cell: domain given as list of two values
            f:    function that defines potential
            firstd: first derivative, if not given is calculated numerically
            secondd: second derivative, if not given is calculated numerically
            n: number of states, default is 1. if n>1, f,d1,d2,firstd, secondd are lists of functions
            d1: first order couplings
            d2: second order couplings
        """

        self.cell = cell
        self.dimension = len(self.cell)
        self.states = n

        try:
            self.f = np.array(f).reshape((self.states, self.states))
        except ValueError:
            print('The list of functions given to the potential is not of '
                  + 'the correct size to match the number of states.'
                  + ' You must provide n**2 elements.')
            raise

        if not isinstance(firstd, (list, np.ndarray)):
            firstd = [firstd]
        self.firstd = firstd

        if not isinstance(secondd, list):
            secondd = [secondd]
        self.secondd = secondd

        if not isinstance(d1, list):
            d1 = [d1]
        self.d1 = d1

        if not isinstance(d2, list):
            d2 = [d2]
        self.d2 = d2

    def __call__(self, *points, i=0, j=0):
        """
        calculate potential at point x or list of points x
        """
        f = self.f[i, j]
        return f(*points)

    def deriv(self, points, n=0):
        """
        calculate 1st derivative at point x or list of points x
        """
        # Need to make these functions n-dimensional, very ugly right now
        firstd = self.firstd[n]
        if firstd is None:
            if self.dimension == 1:
                return derivatives.num_deriv(self, points)
            elif self.dimension == 2:
                d = np.empty_like(points)
                for i, point in enumerate(points):
                    d[i] = derivatives.num_deriv_2D(self, point[0], point[1])
                return d
        else:
            if self.dimension == 1:
                return firstd(points)
            elif self.dimension == 2:
                d = np.empty_like(points)
                for i, point in enumerate(points):
                    d[i] = firstd(point[0], point[1])
                return d

    def hess(self, points, i=0, j=0):
        """
        calculate 2nd derivative at point x or list of points x
        """
        secondd = self.secondd[i]
        if secondd is None:
            if self.dimension == 1:
                return derivatives.num_deriv2(self, points)
            elif self.dimension == 2:
                return derivatives.num_deriv2_2D(self, points[:, 0], points[:, 1])
        else:
            return secondd(*points)

    #### coupling is different for different PES pairs
    #def coupling_d1(self,x,n=0, m=1):
        #"""
        #calculate nonadiabatic vectorial 1st order coupling
        #"""
        #d1 = self.d1[n]
        #if d1 is None:
            #return np.zeros_like(x)
        #else:
            #return d1(x)

    #def coupling_d2(self,x,n=0, m=1):
        #"""
        #calculate nonadiabatic vectorial 1st order coupling
        #"""
        #d2 = self.d2[n,m]
        #if d2 is None:
            #return np.zeros_like(x)
        #else:
            #return d2(x)

    def compute_cell_potential(self, density=100):

        if self.dimension == 1:
            x = np.linspace(self.cell[0][0], self.cell[0][1], density)
            out = self(x)

        elif self.dimension == 2:
            x = np.linspace(self.cell[0][0], self.cell[0][1], density)
            y = np.linspace(self.cell[1][0], self.cell[1][1], density)
            xx, yy = np.meshgrid(x, y)
            out = self(xx, yy)

        else:
            raise ValueError(self.dimension+', the dimension, must be 1 or 2.')

        return out
