#qmp.potential.potential
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

from qmp.tools.utilities import *
import numpy as np

class Potential(object):
    """
    Defines Potential and all operations on it. Functions for the 
    potential energy, the first and second derivative, and for possible 
    excited states and scalar and vectorial derivative couplings must 
    be passed explicitly.
    """

    def __init__(self, domain=None, f=None, firstd=None, secondd=None, \
            n=1, d1=None, d2=None ,name=None):
        """
        Initializes potential
        Input
            domain: domain given as list of two values
            f:    function that defines potential
            firstd: first derivative, if not given is calculated numerically
            secondd: second derivative, if not given is calculated numerically
            n: number of states, default is 1. if n>1, f,d1,d2,firstd, secondd are lists of functions
            d1: first order couplings
            d2: second order couplings
        """

        self.ndim = 1
        if domain is None:
            domain = [[0.,1.]]
        self.domain = domain
        if n is None:
            self.n = 1
        else:
            self.n = n
        if isinstance(f,list):
            self.f = f
        else:
            self.f = [f]
        if isinstance(firstd,list):
            self.firstd = firstd
        else:
            self.firstd = [firstd]
        if isinstance(secondd,list):
            self.secondd = secondd
        else:
            self.secondd = [secondd]
        if isinstance(d1,list):
            self.d1 = d1
        else:
            self.d1 = [d1]
        if isinstance(d2,list):
            self.d2 = d2
        else:
            self.d2 = [d2]
        self.data = None

        if name is None:
            self.name = 'Potential'
        else:
            self.name = name

    def __call__(self,x,n=0):
        """
        calculate potential at point x or list of points x
        """
        f = self.f[n]
        if f is None:
            return np.zeros_like(x)
        else:
            return f(x)
   
    def __repr__(self):
        return self.name

    def deriv(self,x,n=0):
        """
        calculate 1st derivative at point x or list of points x
        """
        firstd = self.firstd[n]
        if firstd is None:
            return num_deriv(self.f,x)
        else:
            return firstd(x)

    def hess(self,x,n=0):
        """
        calculate 2nd derivative at point x or list of points x
        """
        secondd = self.secondd[n]
        if secondd is None:
            return num_deriv2(self.f,x)
        else:
            return secondd(x)

    #### coupling is different for different PES pairs
    def coupling_d1(self,x,n=0, m=1):
        """
        calculate nonadiabatic vectorial 1st order coupling
        """
        d1 = self.d1[n]
        if d1 is None:
            return np.zeros_like(x)
        else:
            return d1(x)
    
    def coupling_d2(self,x,n=0, m=1):
        """
        calculate nonadiabatic vectorial 1st order coupling
        """
        d2 = self.d2[n,m]
        if d2 is None:
            return np.zeros_like(x)
        else:
            return d2(x)


    def plot_pot(self,start=0.0, end=1.0, pts=50):
        """
        plot potential with matplotlib
        """
        try:
            from matplotlib import pyplot as plt
        except:
            raise ImportError('cannot import matplotlib')

        L = np.linspace(start, end, pts)
        y = np.zeros_like(L)
        for i,x in enumerate(L):
            y[i]=self.f(x)

        plt.plot(L, y)


