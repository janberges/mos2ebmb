#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys

dat = sys.argv[1] if len(sys.argv) > 1 else 'tc_0.dat'

(SOC, tot_charge, Tc_McMillan, Tc_AllenDynes, Tc_Eliashberg_CDOS_Einstein,
    Tc_Eliashberg_CDOS_a2F, Tc_Eliashberg_DOS_a2F,
    Tc_Eliashberg_intervalley) = np.loadtxt(dat, skiprows=1).T

SOC = SOC.astype(bool)

plt.plot(tot_charge[~SOC], Tc_Eliashberg_intervalley[~SOC], 'C0D-',
    label=r'Eliashberg: $N_i(\epsilon), \alpha^2 F_{i j}(\omega)$')

plt.plot(tot_charge[~SOC], Tc_Eliashberg_DOS_a2F[~SOC], 'C1*-',
    label=r'Eliashberg: $N(\epsilon), \alpha^2 F(\omega)$')

plt.plot(tot_charge[~SOC], Tc_Eliashberg_CDOS_a2F[~SOC], 'C2s-',
    label=r'Eliashberg: $N(\epsilon) = N(0), \alpha^2 F(\omega)$')

plt.plot(tot_charge[~SOC], Tc_Eliashberg_CDOS_Einstein[~SOC], 'C3o-',
    label=r'Eliashberg: $N(\epsilon) = N(0), \alpha^2 F(\omega) = \lambda'
        r'\omega_{\log} \delta(\omega - \omega_{\log}) / 2$')

plt.plot(tot_charge[~SOC], Tc_AllenDynes[~SOC], 'C4^-',
    label='Allen-Dynes')

plt.plot(tot_charge[~SOC], Tc_McMillan[~SOC], 'C5v-',
    label='McMillan')

plt.plot(tot_charge[SOC], Tc_Eliashberg_intervalley[SOC], 'C0D-')
plt.plot(tot_charge[SOC], Tc_Eliashberg_DOS_a2F[SOC], 'C1*-')
plt.plot(tot_charge[SOC], Tc_Eliashberg_CDOS_a2F[SOC], 'C2s-')
plt.plot(tot_charge[SOC], Tc_Eliashberg_CDOS_Einstein[SOC], 'C3o-')
plt.plot(tot_charge[SOC], Tc_AllenDynes[SOC], 'C4^-')
plt.plot(tot_charge[SOC], Tc_McMillan[SOC], 'C5v-')

plt.xlabel('Doping electrons per cell')
plt.ylabel('Critical temperature (K)')
plt.legend()

plt.savefig(dat.replace('.dat', '.pdf'))
plt.show()
