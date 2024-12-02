#!/usr/bin/env python3

import elphmod
import numpy as np
import re
import storylines

x = float('0.' + re.search('dop_0(\d*)', __file__).group(1))

nk = 313
dw = 0.001

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
U202 = np.sum(abs(U[:, :, d02, -4 * nspin:]) ** 2, axis=2)
U2z2 = np.sum(abs(U[:, :, dz2, -4 * nspin:]) ** 2, axis=2)

e = np.empty((nk, nk, 2 * nspin))
weight = np.empty((nk, nk, 2 * nspin))

for k1 in range(nk):
    for k2 in range(nk):
        indices = sorted(np.argsort(U202[k1, k2])[-2 * nspin:])
        e[k1, k2, :] = E[k1, k2, indices]
        weight[k1, k2, :] = U2z2[k1, k2, indices] / U202[k1, k2, indices]

e -= elphmod.occupations.find_Fermi_level(x * nspin, e, 0.005 * elphmod.misc.Ry,
    elphmod.occupations.fermi_dirac)

w = np.array(list(storylines.multiples(e.min() - dw, e.max() + dw, dw)))

DOS = 0
DOSz2 = 0

for n in range(2 * nspin):
    DOS = DOS + elphmod.dos.hexDOS(e[:, :, n])(w)
    DOSz2 = DOSz2 + elphmod.dos.hexa2F(e[:, :, n], weight[:, :, n])(w)

DOS /= nspin
DOSz2 /= nspin

if elphmod.MPI.comm.rank == 0:
    with open('dos.dat', 'w') as data:
        for iw in range(len(w)):
            data.write('%6.3f %9.6f\n' % (w[iw], DOS[iw]))

    with open('dos2.dat', 'w') as data:
        for iw in range(len(w)):
            data.write('%6.3f %9.6f %9.6f\n'
                % (w[iw], DOSz2[iw], DOS[iw] - DOSz2[iw]))
