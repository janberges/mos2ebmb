# Eliashberg calculations for doped MoS₂

This directory contains the data and scripts to calculate the superconducting
critical temperature of electron-doped MoS₂ monolayer using Eliashberg theory,
as shown in this paper:

> Nina Girotto Erhardt, Jan Berges, Samuel Poncé, and Dino Novko,
  *Understanding the origin of superconducting dome in electron-doped MoS₂
  monolayer*, [arXiv:2412.02822](https://arxiv.org/abs/2412.02822)

Reproducing the calculations requires version 2.0.0 of the Eliashberg solver
[ebmb](https://github.com/janberges/ebmb) and the Python packages elphmod and
StoryLines, which can be installed using pip (e.g., in a virtual environment):

    python3 -m pip install elphmod==0.29 storylines==0.15

The `data` directory contains adiabatic (A), nonadiabatic (NA), and fully
nonadiabatic (FA) Eliashberg spectral functions (α²F) from density-functional
perturbation theory for different doping levels. Nonadiabatic phonon self-energy
corrections in the form of either only frequency shifts (NA) or also broadening
(FA) have been used, see Girotto and Novko, Phys. Rev. B 107, 064310 (2023).

It also contains the corresponding electronic Hamiltonians in a Wannier basis.
Running the following commands in the respective subdirectory yields the total
and valley-resolved density of states (DOS) of the lowest two conduction bands
and plots them:

    python3 ../../dos.py
    python3 ../../plot_dos.py

Visualizing the orbital-resolved band structure helps understand the selection
of the two conduction bands:

    python3 ../../plot_el.py

The superconducting critical temperatures for different levels of approximation
(McMillan's formula, the Allen-Dynes formula, and Eliashberg theory considering
the full DOS or its value at the Fermi level, the full α²F or the corresponding
Einstein spectrum, or the full valley-resolved DOS and α²F) can also be computed
and plotted for different Coulomb pseudopotentials (μ\* = 0.13 by default):

    python3 tc.py [μ*]
    python3 plot_tc.py [μ*]
