#!/usr/bin/env python3

import ebmb
import elphmod
import numpy as np
import os
import sys

muStar = float(sys.argv[1]) if len(sys.argv) > 1 else 0.13

cutoff = 20.0

label = ('tc_%4.2f' % muStar).replace('.', '')

SOC = []
tot_charge = []
Tc_Eliashberg_intervalley = []
Tc_Eliashberg_DOS_a2F = []
Tc_Eliashberg_CDOS_a2F = []
Tc_Eliashberg_CDOS_Einstein = []
Tc_McMillan = []
Tc_AllenDynes = []

a2F_tmp = '/dev/shm/a2f.tmp'
a2F2_tmp = '/dev/shm/a2f2.tmp'

for directory in sorted(os.listdir('data')):
    a2F_file = 'data/%s/800K_a2f_lam_FA.txt' % directory

    if not os.path.exists(a2F_file):
        continue

    n = ''.join(a for a in directory if a in '0123456789')
    n = float(n[0] + '.' + n[1:])

    DOS_file = 'data/%s/dos.dat' % directory
    DOS2_file = 'data/%s/dos2.dat' % directory

    a2F = np.loadtxt(a2F_file)
    a2F[:, 0] *= 1e-3
    np.savetxt(a2F_tmp, a2F)

    a2F2 = np.zeros((len(a2F), 5))
    a2F2[:, 0] = a2F[:, 0]
    a2F2[:, 2] = a2F[:, 1]
    a2F2[:, 3] = a2F[:, 1]
    np.savetxt(a2F2_tmp, a2F2)

    info = ebmb.get(
       n=n,
       dos=DOS_file,
       a2F=a2F_tmp,
       cutoff=cutoff,
       tell=False,
       )

    print('directory: %s' % directory)
    print('tot_charge: %g' % n)
    print('lambda: %g (%g)' % (info['lambda'], a2F[-1, -1]))
    print('omegaLog: %g eV' % info['omegaLog'])
    print('omega2nd: %g eV' % info['omega2nd'])
    print('mu0: %g eV' % info['mu0'])
    print('mu: %g eV' % info['mu'])

    Tc = elphmod.eliashberg.Tc(info['lambda'], info['omegaLog'],
        muStar, info['omega2nd'], correct=True)

    if Tc < 1:
        continue

    SOC.append('soc' in directory.lower())

    tot_charge.append(n)

    Tc_McMillan.append(elphmod.eliashberg.Tc(info['lambda'], info['omegaLog'],
        muStar))

    Tc_AllenDynes.append(Tc)

    Tc_Eliashberg_intervalley.append(ebmb.get(
       T=Tc,
       program='critical',
       bands=2,
       n=n,
       dos=DOS2_file,
       a2F=a2F2_tmp,
       muStar=[[0, muStar], [muStar, 0]],
       cutoff=cutoff,
       tell=False,
       ))

    Tc_Eliashberg_DOS_a2F.append(ebmb.get(
       T=Tc,
       program='critical',
       n=n,
       dos=DOS_file,
       a2F=a2F_tmp,
       muStar=muStar,
       cutoff=cutoff,
       tell=False,
       ))

    Tc_Eliashberg_CDOS_a2F.append(ebmb.get(
       T=Tc,
       program='critical',
       a2F=a2F_tmp,
       muStar=muStar,
       cutoff=cutoff,
       tell=False,
       ))

    Tc_Eliashberg_CDOS_Einstein.append(ebmb.get(
       T=Tc,
       program='critical',
       lamda=info['lambda'],
       omegaE=info['omegaLog'],
       muStar=muStar,
       cutoff=cutoff,
       tell=False,
       ))

with open(label + '.dat', 'w') as data:
    data.write(('%2s' + ' %6s' * 7 + '\n')
        % ('SO', 'NE', 'MM', 'AD', 'CE', 'CA', 'DA', 'OD'))

    for i in range(len(tot_charge)):
        data.write(('%2d' + ' %6.3f' * 7 + '\n') % (SOC[i], tot_charge[i],
            Tc_McMillan[i], Tc_AllenDynes[i], Tc_Eliashberg_CDOS_Einstein[i],
            Tc_Eliashberg_CDOS_a2F[i], Tc_Eliashberg_DOS_a2F[i],
            Tc_Eliashberg_intervalley[i]))
