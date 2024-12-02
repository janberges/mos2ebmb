#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys

muStar = float(sys.argv[1]) if len(sys.argv) > 1 else 0.13

filename = 'tc_%s.dat' % ('%4.2f' % muStar).replace('.', '')

(SOC, tot_charge, Tc_McMillan, Tc_AllenDynes, Tc_Eliashberg_CDOS_Einstein,
    Tc_Eliashberg_CDOS_a2F, Tc_Eliashberg_DOS_Einstein, Tc_Eliashberg_DOS_a2F,
    Tc_Eliashberg_intervalley) = np.loadtxt(filename, skiprows=1).T

SOC = SOC.astype(bool)

plt.plot(tot_charge[~SOC], Tc_Eliashberg_intervalley[~SOC], 'C0D-',
    label=r'Eliashberg: $N_i(\epsilon), \alpha^2 F_{i j}(\omega)$')

plt.plot(tot_charge[~SOC], Tc_Eliashberg_DOS_a2F[~SOC], 'C1*-',
    label=r'Eliashberg: $N(\epsilon), \alpha^2 F(\omega)$')

plt.plot(tot_charge[~SOC], Tc_Eliashberg_DOS_Einstein[~SOC], 'C2*-',
    label=r'Eliashberg: $N(\epsilon), '
        r'\lambda \omega_{\log} \delta(\omega - \omega_{\log}) / 2$')

plt.plot(tot_charge[~SOC], Tc_Eliashberg_CDOS_a2F[~SOC], 'C3s-',
    label=r'Eliashberg: $N(0), \alpha^2 F(\omega)$')

plt.plot(tot_charge[~SOC], Tc_Eliashberg_CDOS_Einstein[~SOC], 'C4o-',
    label=r'Eliashberg: $N(0), '
        r'\lambda \omega_{\log} \delta(\omega - \omega_{\log}) / 2$')

plt.plot(tot_charge[~SOC], Tc_AllenDynes[~SOC], 'C5^-',
    label='Allen-Dynes')

plt.plot(tot_charge[~SOC], Tc_McMillan[~SOC], 'C6v-',
    label='McMillan')

plt.plot(tot_charge[SOC], Tc_Eliashberg_intervalley[SOC], 'C0D-')
plt.plot(tot_charge[SOC], Tc_Eliashberg_DOS_a2F[SOC], 'C1*-')
plt.plot(tot_charge[SOC], Tc_Eliashberg_DOS_Einstein[SOC], 'C2*-')
plt.plot(tot_charge[SOC], Tc_Eliashberg_CDOS_a2F[SOC], 'C3s-')
plt.plot(tot_charge[SOC], Tc_Eliashberg_CDOS_Einstein[SOC], 'C4o-')
plt.plot(tot_charge[SOC], Tc_AllenDynes[SOC], 'C5^-')
plt.plot(tot_charge[SOC], Tc_McMillan[SOC], 'C6v-')

plt.title(r'$\mu^* = %g$' % muStar)
plt.xlabel('Doping electrons per cell')
plt.ylabel('Critical temperature (K)')
plt.legend()
plt.show()
