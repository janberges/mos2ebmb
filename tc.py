#!/usr/bin/env python3

import ebmb
import elphmod
import matplotlib.pyplot as plt
import numpy as np
import os

muStar = 0.0

tot_charge = []
Tc_Eliashberg_DOS_a2F = []
Tc_Eliashberg_cDOS_a2F = []
Tc_Eliashberg_cDOS_Einstein = []
Tc_McMillan = []
Tc_AllenDynes = []

a2F_tmp = '/dev/shm/a2d.tmp'

for ne in np.arange(0.0, 0.3, 0.005):
    directory = 'data/dop_%s' % ('%g' % ne).replace('.', '')
    a2F_file = '%s/800K_a2f_lam_FA.txt' % directory

    if not os.path.exists(a2F_file):
        continue

    DOS_file = '%s/dos.dat' % directory

    print('tot_charge: %g' % ne)

    tot_charge.append(ne)

    n = 0.5 * ne # for n = 2 all bands are filled, our DOS can hold 4 electrons

    a2F = np.loadtxt(a2F_file)
    a2F[:, 0] *= 1e-3
    np.savetxt(a2F_tmp, a2F)

    info = ebmb.get(
       tell=False,
       n=n,
       dos=DOS_file,
       a2F=a2F_tmp,
       )

    print('lambda: %g (%g)' % (info['lambda'], a2F[-1, -1]))
    print('omegaLog: %g eV' % info['omegaLog'])
    print('omega2nd: %g eV' % info['omega2nd'])
    print('mu0: %g eV' % info['mu0'])
    print('mu: %g eV' % info['mu'])

    Tc_Eliashberg_DOS_a2F.append(ebmb.get(
       program='critical',
       n=n,
       dos=DOS_file,
       a2F=a2F_tmp,
       muStar=muStar,
       tell=False,
       ))

    Tc_Eliashberg_cDOS_a2F.append(ebmb.get(
       program='critical',
       a2F=a2F_tmp,
       muStar=muStar,
       tell=False,
       ))

    Tc_Eliashberg_cDOS_Einstein.append(ebmb.get(
       program='critical',
       lamda=info['lambda'],
       omegaE=info['omegaLog'],
       muStar=muStar,
       tell=False,
       ))

    Tc_McMillan.append(elphmod.eliashberg.Tc(info['lambda'], info['omegaLog'],
        muStar))

    Tc_AllenDynes.append(elphmod.eliashberg.Tc(info['lambda'], info['omegaLog'],
        muStar, info['omega2nd'], correct=True))

plt.plot(tot_charge, Tc_Eliashberg_DOS_a2F, '*-',
    label=r'Eliashberg: $N(\epsilon), \alpha^2 F(\omega)$')

plt.plot(tot_charge, Tc_Eliashberg_cDOS_a2F, 's-',
    label=r'Eliashberg: $N(\epsilon) = N(0), \alpha^2 F(\omega)$')

plt.plot(tot_charge, Tc_Eliashberg_cDOS_Einstein, 'o-',
    label=r'Eliashberg: $N(\epsilon) = N(0), \alpha^2 F(\omega) = \lambda'
        r'\omega_{\mathrm{log}} \delta(\omega - \omega_{\mathrm{log}}) / 2$')

plt.plot(tot_charge, Tc_AllenDynes, '^-', label='Allen-Dynes')
plt.plot(tot_charge, Tc_McMillan, 'v-', label='McMillan')

plt.title(r'$\mu^* = %g$' % muStar)
plt.xlabel('Total charge ($-e$)')
plt.ylabel('Critical temperature (K)')
plt.legend()

plt.savefig(('tc_%g' % muStar).replace('.', '') + '.pdf')
plt.show()
