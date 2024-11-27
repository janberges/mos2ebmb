#!/usr/bin/env python3

import elphmod
import numpy as np
import storylines
import sys

comm = elphmod.MPI.comm

x = float(sys.argv[1]) if len(sys.argv) > 1 else 0.1

nk = 313
dw = 0.001

plot_3d = False

el = elphmod.el.Model('mos2')

SOC = el.size == 22

E, U = elphmod.dispersion.dispersion_full(el.H, nk, vectors=True)

if SOC:
    d02 = [0, 1, 6, 7, 8, 9]
    dz2 = [0, 1]
    nspin = 2
else:
    d02 = [0, 3, 4]
    dz2 = [0]
    nspin = 1

E = E[:, :, -4 * nspin:]
U2 = (abs(U) ** 2)[:, :, d02, -4 * nspin:].sum(axis=2)
U2z2 = (abs(U) ** 2)[:, :, dz2, -4 * nspin:].sum(axis=2)

e = np.empty((nk, nk, 2 * nspin))
weight = np.empty((nk, nk, 2 * nspin))

for k1 in range(nk):
    for k2 in range(nk):
        indices = sorted(np.argsort(U2[k1, k2])[-2 * nspin:])
        e[k1, k2, :] = E[k1, k2, indices]
        weight[k1, k2, :] = U2z2[k1, k2, indices] / U2[k1, k2, indices]

mu = elphmod.occupations.find_Fermi_level(x * nspin, e, 0.005 * elphmod.misc.Ry,
        elphmod.occupations.fermi_dirac)

e -= mu

w = np.array(list(storylines.multiples(e.min() - dw, e.max() + dw, dw)))

DOS = 0
DOSz2 = 0

for n in range(2 * nspin):
    DOS = DOS + elphmod.dos.hexDOS(e[:, :, n])(w)
    DOSz2 = DOSz2 + elphmod.dos.hexa2F(e[:, :, n], weight[:, :, n])(w)

DOS /= nspin
DOSz2 /= nspin

if comm.rank == 0:
    with open('dos.dat', 'w') as data:
        for iw in range(len(w)):
            data.write('%6.3f %9.6f\n' % (w[iw], DOS[iw]))

    with open('dos2.dat', 'w') as data:
        for iw in range(len(w)):
            data.write('%6.3f %9.6f %9.6f\n'
                % (w[iw], DOSz2[iw], DOS[iw] - DOSz2[iw]))

    if plot_3d:
        import matplotlib.pyplot as plt
        from matplotlib import cm

        ax = plt.axes(projection='3d')

        k = np.arange(nk)
        kx, ky = np.meshgrid(k, k)

        ax.plot_surface(kx, ky, e[:, :, 0], cmap=cm.coolwarm, linewidth=0,
            antialiased=False)

        plt.show()
