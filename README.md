# Eliashberg calculations for doped MoS₂

This directory contains the data and scripts to calculate the superconducting
critical temperature of electron-doped MoS₂ monolayer using Eliashberg theory,
as shown by Girotto, Berges, Poncé, and Novko (2024).

Reproducing the calculations requires version 2.0.0 of the Eliashberg solver
[ebmb](https://github.com/janberges/ebmb) as well as the Python packages NumPy,
elphmod, and StoryLines, which can be installed by running (e.g., in a virtual
environment) `python3 -m pip install numpy elphmod==0.29 storylines==0.15`.

The `data` directory contains adiabatic (A), nonadiabatic (NA), and fully
nonadiabatic (FA) Eliashberg spectral functions (α²F) from density-functional
perturbation theory for different doping levels. Nonadiabatic phonon self-energy
corrections in the form of either only frequency shifts (NA) or also broadening
(FA) have been used, see Girotto and Novko, Phys. Rev. B 107, 064310 (2023).

It also contains the corresponding electronic Hamiltonians in a Wannier basis.
Running `python3 ../../dos.py` in the respective subdirectory yields the total
and valley-resolved density of states (DOS) of the lowest two conduction bands.
They can be plotted with `python3 ../../plot_dos.py`. To better understand the
selection of the two conduction bands, the orbital-resolved band structure can
be plotted using `python3 ../../plot_el.py`.

The superconducting critical temperatures for different levels of approximation
(McMillan's formula, the Allen-Dynes formula, and Eliashberg theory considering
the full DOS or its value at the Fermi level, the full α²F or the corresponding
Einstein spectrum, or the full valley-resolved DOS and α²F) are computed with
`python3 tc.py [μ*]`, where the Coulomb pseudopotential defaults to μ\* = 0.13.
The results and can be plotted with `python3 plot_tc.py [μ*]`.
