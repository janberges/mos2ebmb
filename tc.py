#!/usr/bin/env python3

import ebmb
import elphmod
import matplotlib.pyplot as plt
import numpy as np
import os

muStar = 0.0

tot_charge = []
Tc_Eliashberg = []
Tc_Einstein = []
Tc_McMillan = []
Tc_AllenDynes = []

a2F_tmp = '/dev/shm/a2d.tmp'

for n in np.arange(0.0, 0.3, 0.005):
    a2F_file = 'data/dop_%s/800K_a2f_lam_FA.txt' % ('%g' % n).replace('.', '')

    if not os.path.exists(a2F_file):
        continue

    print('tot_charge: %g' % n)

    tot_charge.append(n)

    a2F = np.loadtxt(a2F_file)
    a2F[:, 0] *= 1e-3
    np.savetxt(a2F_tmp, a2F)

    info = ebmb.get(
       tell=False,
       a2F=a2F_tmp,
       )

    print('lambda: %g (%g)' % (info['lambda'], a2F[-1, -1]))
    print('omegaLog: %g eV' % info['omegaLog'])
    print('omega2nd: %g eV' % info['omega2nd'])

    Tc_Eliashberg.append(ebmb.get(
       program='critical',
       a2F=a2F_tmp,
       muStar=muStar,
       tell=False,
       ))

    Tc_Einstein.append(ebmb.get(
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

plt.plot(tot_charge, Tc_Eliashberg, 's-', label='Eliashberg')
plt.plot(tot_charge, Tc_Einstein, 'o-', label='Einstein')
plt.plot(tot_charge, Tc_McMillan, 'v-', label='McMillan')
plt.plot(tot_charge, Tc_AllenDynes, '^-', label='Allen-Dynes')

plt.title(r'$\mu^* = %g$' % muStar)
plt.xlabel('Total charge ($-e$)')
plt.ylabel('Critical temperature (K)')
plt.legend()

plt.savefig(('tc_%g' % muStar).replace('.', '') + '.pdf')
plt.show()
