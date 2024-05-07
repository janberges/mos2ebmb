#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

for muStar in 0.0, 0.05, 0.1, 0.15, 0.2:
    label = ('tc_%g' % muStar).replace('.', '')

    (tot_charge, Tc_McMillan, Tc_AllenDynes, Tc_Eliashberg_CDOS_Einstein,
        Tc_Eliashberg_CDOS_a2F, Tc_Eliashberg_DOS_a2F,
        Tc_Eliashberg_intervalley) = np.loadtxt(label + '.dat', skiprows=1).T

    plt.plot(tot_charge, Tc_Eliashberg_intervalley, 'D-',
        label=r'Eliashberg: $N_i(\epsilon), \alpha^2 F_{i j}(\omega)$')

    plt.plot(tot_charge, Tc_Eliashberg_DOS_a2F, '*-',
        label=r'Eliashberg: $N(\epsilon), \alpha^2 F(\omega)$')

    plt.plot(tot_charge, Tc_Eliashberg_CDOS_a2F, 's-',
        label=r'Eliashberg: $N(\epsilon) = N(0), \alpha^2 F(\omega)$')

    plt.plot(tot_charge, Tc_Eliashberg_CDOS_Einstein, 'o-',
        label=r'Eliashberg: $N(\epsilon) = N(0), \alpha^2 F(\omega) = \lambda'
            r'\omega_{\log} \delta(\omega - \omega_{\log}) / 2$')

    plt.plot(tot_charge, Tc_AllenDynes, '^-', label='Allen-Dynes')
    plt.plot(tot_charge, Tc_McMillan, 'v-', label='McMillan')

    plt.title(r'$\mu^* = %g$' % muStar)
    plt.xlabel('Total charge ($-e$)')
    plt.ylabel('Critical temperature (K)')
    plt.legend()

    plt.savefig(label + '.pdf')
    plt.show()
