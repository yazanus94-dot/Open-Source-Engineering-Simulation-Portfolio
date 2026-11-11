#!/bin/bash
set -e
python convergence.py
# band structure at converged lattice: scf with 30 Ry then bands
sed 's/__ALAT__/10.26/;s/__ECUT__/30/;s/__K__/8/' scf.in.template > scf_final.in
mpirun -np ${NP:-2} pw.x -in scf_final.in > scf_final.out
mpirun -np ${NP:-2} pw.x -in bands.in > bands.out
bands.x -in bandsx.in > bandsx.out
python plot_bands.py
