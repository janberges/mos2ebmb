#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys

muStar = float(sys.argv[1]) if len(sys.argv) > 1 else 0.13

filename = 'tc_%s.dat' % ('%4.2f' % muStar).replace('.', '')

(SOC, doping, Tc_McMillan, Tc_AllenDynes, Tc_Eliashberg_CDOS_Einstein,
    Tc_Eliashberg_CDOS_a2F, Tc_Eliashberg_DOS_Einstein, Tc_Eliashberg_DOS_a2F,
    Tc_Eliashberg_intervalley) = np.loadtxt(filename, skiprows=1).T

SOC = SOC.astype(bool)

plt.plot(doping[~SOC], Tc_Eliashberg_intervalley[~SOC], 'C0o-',
    label=r'Eliashberg: $N_i(\epsilon), \alpha^2 F_{i j}(\omega)$')

plt.plot(doping[~SOC], Tc_Eliashberg_DOS_a2F[~SOC], 'C1v-',
    label=r'Eliashberg: $N(\epsilon), \alpha^2 F(\omega)$')

plt.plot(doping[~SOC], Tc_Eliashberg_DOS_Einstein[~SOC], 'C2^-',
    label=r'Eliashberg: $N(\epsilon), '
        r'\lambda \omega_{\log} \delta(\omega - \omega_{\log}) / 2$')

plt.plot(doping[~SOC], Tc_Eliashberg_CDOS_a2F[~SOC], 'C3>-',
    label=r'Eliashberg: $N(0), \alpha^2 F(\omega)$')

plt.plot(doping[~SOC], Tc_Eliashberg_CDOS_Einstein[~SOC], 'C4<-',
    label=r'Eliashberg: $N(0), '
        r'\lambda \omega_{\log} \delta(\omega - \omega_{\log}) / 2$')

plt.plot(doping[~SOC], Tc_AllenDynes[~SOC], 'C5D-',
    label='Allen-Dynes')

plt.plot(doping[~SOC], Tc_McMillan[~SOC], 'C6s-',
    label='McMillan')

plt.plot(doping[SOC], Tc_Eliashberg_intervalley[SOC], 'C0o-')
plt.plot(doping[SOC], Tc_Eliashberg_DOS_a2F[SOC], 'C1v-')
plt.plot(doping[SOC], Tc_Eliashberg_DOS_Einstein[SOC], 'C2^-')
plt.plot(doping[SOC], Tc_Eliashberg_CDOS_a2F[SOC], 'C3>-')
plt.plot(doping[SOC], Tc_Eliashberg_CDOS_Einstein[SOC], 'C4<-')
plt.plot(doping[SOC], Tc_AllenDynes[SOC], 'C5D-')
plt.plot(doping[SOC], Tc_McMillan[SOC], 'C6s-')

plt.title(r'$\mu^* = %g$' % muStar)
plt.ylabel('Critical temperature (K)')
plt.xlabel('Doping electrons per cell')
plt.legend()
plt.show()
