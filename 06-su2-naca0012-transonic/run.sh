#!/bin/bash
set -e
python make_mesh.py
SU2_CFD naca0012.cfg | tee su2.log     # or: mpirun -n 4 SU2_CFD naca0012.cfg
python plot_cp.py
