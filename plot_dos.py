#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

w, DOS = np.loadtxt('dos.dat', skiprows=1).T
w, DOS1, DOS2 = np.loadtxt('dos2.dat', skiprows=1).T

plt.plot(w, DOS, label='total')
plt.plot(w, DOS1, label='$d_{z^2}$')
plt.plot(w, DOS2, label='$d_{x^2 - y^2, x y}$')
plt.plot(w, DOS1 + DOS2, 'k--', label='sum')

plt.xlabel('Energy (eV)')
plt.ylabel('Density of states (1/eV)')
plt.legend()

plt.show()
