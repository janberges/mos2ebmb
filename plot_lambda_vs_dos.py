#!/usr/bin/env python3

import elphmod
import matplotlib.pyplot as plt
import numpy as np
import os

tot_charge = []
lamda = []
dosef = []
dosav = []

kT = 0.0005 * elphmod.misc.Ry

for ne in np.arange(0.0, 0.3, 0.005):
    directory = 'data/dop_%s' % ('%g' % ne).replace('.', '')
    a2F_file = '%s/800K_a2f_lam_FA.txt' % directory

    if not os.path.exists(a2F_file):
        continue

    DOS_file = '%s/dos.dat' % directory

    tot_charge.append(ne)

    a2F = np.loadtxt(a2F_file)
    DOS = np.loadtxt(DOS_file)

    delta = elphmod.occupations.fermi_dirac_delta(DOS[:, 0] / kT) / kT

    lamda.append(a2F[-1, -1])
    dosef.append(DOS[np.argmin(abs(DOS[:, 0])), 1])
    dosav.append(np.sum(delta * DOS[:, 1]) / delta.sum())

lamda = np.array(lamda)
dosef = np.array(dosef)
dosav = np.array(dosav)

plt.plot(tot_charge, lamda, 'o-', label=r'$\lambda$')
plt.plot(tot_charge, dosef, 'D-', label='exact $N(0)$ (1/eV)')
plt.plot(tot_charge, dosav, 's-', label='smeared $N(0)$ (1/eV)')

plt.xlabel('Total charge ($-e$)')
plt.legend()

plt.savefig('lambda_vs_dos.pdf')
plt.show()
