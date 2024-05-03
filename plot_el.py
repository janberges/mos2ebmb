#!/usr/bin/env python3

import elphmod
import matplotlib.pyplot as plt
import numpy as np

comm = elphmod.MPI.comm

colors = ['red'] + 2 * ['blue'] + 2 * ['red'] + 6 * ['yellow']

el = elphmod.el.Model('mos2')
mu = elphmod.el.read_Fermi_level('sc.out')

path = 'GMKG'
k, x, corners = elphmod.bravais.path(path, ibrav=4, N=150)

e, U, order = elphmod.dispersion.dispersion(el.H, k,
    vectors=True, order=True)

e -= mu

plt.ylabel('Electron energy (eV)')
plt.xlabel('Wave vector')

plt.xticks(x[corners], path)

for n in range(el.size):
    fatbands = elphmod.plot.compline(x, e[:, n],
        0.1 * (U[:, :, n] * U[:, :, n].conj()).real)

    for fatband, color in zip(fatbands, colors):
        plt.fill(*fatband, color=color, linewidth=0.0)

plt.show()
