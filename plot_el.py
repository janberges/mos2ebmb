#!/usr/bin/env python3

import elphmod
import matplotlib.patches as pat
import matplotlib.pyplot as plt

el = elphmod.el.Model('mos2')

path = 'GMKG'
k, x, corners = elphmod.bravais.path(path, ibrav=4, N=150)

e, U, order = elphmod.dispersion.dispersion(el.H, k,
    vectors=True, order=True)

if elphmod.MPI.comm.rank != 0:
    raise SystemExit

colors = ['chocolate'] + 2 * ['royalblue'] + 2 * ['gold'] + 6 * ['lightblue']

for n in range(el.size):
    fatbands = elphmod.plot.compline(x, e[:, n], 0.1 * abs(U[:, :, n]) ** 2)

    for fatband, color in zip(fatbands, colors):
        plt.fill(*fatband, color=color, linewidth=0.0)

plt.ylabel('Electron energy (eV)')
plt.xlabel('Wave vector')
plt.xticks(x[corners], path)

plt.legend(handles=[
    pat.Patch(color=colors[0], label='Mo-$d_{z^2}$'),
    pat.Patch(color=colors[3], label='Mo-$d_{x^2 - y^2, x y}$'),
    pat.Patch(color=colors[1], label='Mo-$d_{x z, y z}$'),
    pat.Patch(color=colors[5], label='S-$p$'),
    ])

plt.show()
