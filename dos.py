#!/usr/bin/env python3

import elphmod
import numpy as np
import storylines

comm = elphmod.MPI.comm

nk = 313
dw = 0.001

plot_3d = False
plot_dos = True

el = elphmod.el.Model('mos2')
mu = elphmod.el.read_Fermi_level('sc.out')

E, U = elphmod.dispersion.dispersion_full(el.H, nk, vectors=True)

E = E[:, :, -4:]
U2 = (abs(U) ** 2)[:, :, [0, 3, 4], -4:].sum(axis=2)
U2z2 = (abs(U) ** 2)[:, :, 0, -4:]

e = np.empty((nk, nk, 2))
weight = np.empty((nk, nk, 2))

for k1 in range(nk):
    for k2 in range(nk):
        indices = sorted(np.argsort(U2[k1, k2])[-2:])
        e[k1, k2, :] = E[k1, k2, indices]
        weight[k1, k2, :] = U2z2[k1, k2, indices] / U2[k1, k2, indices]

e -= mu

w = np.array(list(storylines.multiples(e.min() - dw, e.max() + dw, dw)))

DOS = 0
DOSz2 = 0

for n in range(2):
    DOS = DOS + elphmod.dos.hexDOS(e[:, :, n])(w)
    DOSz2 = DOSz2 + elphmod.dos.hexa2F(e[:, :, n], weight[:, :, n])(w)

if comm.rank == 0:
    with open('dos.dat', 'w') as data:
        for iw in range(len(w)):
            data.write('%6.3f %9.6f\n' % (w[iw], DOS[iw]))

    with open('dos2.dat', 'w') as data:
        for iw in range(len(w)):
            data.write('%6.3f %9.6f %9.6f\n'
                % (w[iw], DOSz2[iw], DOS[iw] - DOSz2[iw]))

    if plot_3d or plot_dos:
        import matplotlib.pyplot as plt

    if plot_3d:
        from matplotlib import cm

        ax = plt.axes(projection='3d')

        k = np.arange(nk)
        kx, ky = np.meshgrid(k, k)

        ax.plot_surface(kx, ky, e[:, :, 0], cmap=cm.coolwarm, linewidth=0,
            antialiased=False)

        plt.show()

    if plot_dos:
        plt.plot(w, DOS)
        plt.plot(w, DOSz2)
        plt.show()
