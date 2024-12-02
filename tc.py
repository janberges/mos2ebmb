#!/usr/bin/env python3

import ebmb
import elphmod
import numpy as np
import os
import re
import sys

muStar = float(sys.argv[1]) if len(sys.argv) > 1 else 0.13

filename = 'tc_%s.dat' % ('%4.2f' % muStar).replace('.', '')

SOC = []
doping = []
Tc_McMillan = []
Tc_AllenDynes = []
Tc_Eliashberg_CDOS_Einstein = []
Tc_Eliashberg_CDOS_a2F = []
Tc_Eliashberg_DOS_Einstein = []
Tc_Eliashberg_DOS_a2F = []
Tc_Eliashberg_intervalley = []

for directory in sorted(os.listdir('data')):
    x = float('0.' + re.search('dop_0(\d*)', directory).group(1))

    DOS_file = 'data/%s/dos.dat' % directory
    DOS2_file = 'data/%s/dos2.dat' % directory

    a2F_file = 'data/%s/a2f.dat' % directory
    a2F2_file = 'data/%s/a2f2.dat' % directory

    a2F = np.loadtxt('data/%s/800K_a2f_lam_FA.txt' % directory)
    a2F[:, 0] *= 1e-3
    np.savetxt(a2F_file, a2F, fmt='%9.6f')

    a2F2 = np.zeros((len(a2F), 5))
    a2F2[:, 0] = a2F[:, 0]
    a2F2[:, 2] = a2F[:, 1]
    a2F2[:, 3] = a2F[:, 1]
    np.savetxt(a2F2_file, a2F2, fmt='%9.6f')

    general = dict(
        n=x,
        cutoff=20.0,
        tell=False,
        )

    info = ebmb.get(
       dos=DOS_file,
       a2F=a2F_file,
       **general)

    print('directory: %s (x = %g)' % (directory, x))

    print('lambda = %g (%g)' % (info['lambda'], a2F[-1, -1]))

    for key in 'omegaLog', 'omega2nd', 'mu0', 'mu':
        print('%s = %g eV' % (key, info[key]))

    Tc = elphmod.eliashberg.Tc(info['lambda'], info['omegaLog'], muStar,
        info['omega2nd'], correct=True)

    if Tc < 1:
        print('Tc is too low!')
        continue

    SOC.append('soc' in directory.lower())

    doping.append(x)

    Tc_McMillan.append(elphmod.eliashberg.Tc(info['lambda'], info['omegaLog'],
        muStar))

    Tc_AllenDynes.append(Tc)

    settings = dict(
        program='critical',
        T=Tc,
        **general)

    Tc_Eliashberg_intervalley.append(ebmb.get(
        dos=DOS2_file,
        a2F=a2F2_file,
        muStar=[[0, muStar], [muStar, 0]],
        **settings))

    Tc_Eliashberg_DOS_a2F.append(ebmb.get(
        dos=DOS_file,
        a2F=a2F_file,
        muStar=muStar,
        **settings))

    Tc_Eliashberg_DOS_Einstein.append(ebmb.get(
        dos=DOS_file,
        lamda=info['lambda'],
        omegaE=info['omegaLog'],
        muStar=muStar,
        **settings))

    Tc_Eliashberg_CDOS_a2F.append(ebmb.get(
        a2F=a2F_file,
        muStar=muStar,
        **settings))

    Tc_Eliashberg_CDOS_Einstein.append(ebmb.get(
        lamda=info['lambda'],
        omegaE=info['omegaLog'],
        muStar=muStar,
        **settings))

with open(filename, 'w') as data:
    data.write(('%2s' + ' %6s' * 8 + '\n')
        % ('SO', 'NE', 'MM', 'AD', 'CE', 'CA', 'DE', 'DA', 'OD'))

    for i in range(len(doping)):
        data.write(('%2d' + ' %6.3f' * 8 + '\n') % (SOC[i], doping[i],
            Tc_McMillan[i], Tc_AllenDynes[i], Tc_Eliashberg_CDOS_Einstein[i],
            Tc_Eliashberg_CDOS_a2F[i], Tc_Eliashberg_DOS_Einstein[i],
            Tc_Eliashberg_DOS_a2F[i], Tc_Eliashberg_intervalley[i]))
