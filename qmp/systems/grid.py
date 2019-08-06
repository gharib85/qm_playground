import numpy as np
import scipy.sparse as sparse
from qmp.tools.utilities import hbar


class Grid1D:

    def __init__(self, mass=1, start=0.0, end=1.0, N=100, psi0=None):

        self.x, self.dx = np.linspace(start, end, N, retstep=True)
        self.mass = mass
        self.N = N
        self.ndim = 1
        self.solved = False

        # Initial wavefunction all zeros
        if psi0 is None:
            self.psi = np.zeros_like(self.x)
        else:
            self.psi = psi0

        self.L = self.define_laplacian()

    def define_laplacian(self):
        L = sparse.lil_matrix(-2*np.diag(np.ones(self.N), 0)
                              + np.diag(np.ones(self.N-1), 1)
                              + np.diag(np.ones(self.N-1), -1))

        L[0, -1] = 1
        L[-1, 0] = 1
        return sparse.lil_matrix(L / (self.dx*self.dx))

    def construct_T_matrix(self):
        return - (hbar**2) * self.L / (2 * self.mass)

    def construct_V_matrix(self, potential):
        return np.diag(potential(self.x))

    def compute_potential_flat(self, potential):
        return potential(self.x)

    def set_initial_wvfn(self, psi):
        self.psi = psi


class Grid2D:

    def __init__(self, mass=1, start=[0.0, 0], end=[1, 1], N=100, psi0=None):

        self.x, self.dx = np.linspace(start[0], end[0], N, retstep=True)
        self.y, self.dy = np.linspace(start[0], end[0], N, retstep=True)
        self.xgrid, self.ygrid = np.meshgrid(self.x, self.y)

        self.mass = mass
        self.N = N
        self.ndim = 1
        self.solved = False

        # Initial wavefunction all zeros
        if psi0 is None:
            self.psi = np.zeros_like(self.xgrid)
        else:
            self.psi = psi0

        self.L = self.define_laplacian()

    def define_laplacian(self):
        A, b = -2.*np.eye(self.N), np.ones(self.N-1)
        L1 = sparse.lil_matrix(A+np.diagflat(b, -1)+np.diagflat(b, 1))

        L = (sparse.kron(L1, np.eye(self.N))
             + sparse.kron(np.eye(self.N), L1)).tolil()

        L[0, -1] = 1.
        L[-1, 0] = 1.
        return sparse.lil_matrix(L/(self.dx**2*self.dy**2))

    def construct_T_matrix(self):
        return - hbar ** 2 * self.L / (2 * self.mass)

    def construct_V_matrix(self, potential):
        Vflat = potential(self.xgrid, self.ygrid).flatten()
        return sparse.diags(Vflat, 0, (self.N*self.N, self.N*self.N))

    def compute_potential_flat(self, potential):
        return potential(self.xgrid, self.ygrid).flatten()

    def set_initial_wvfn(self, psi):
        self.psi = psi