#!/bin/bash
set -e
python make_inp.py 40 4 4
ccx beam                # solves beam.inp -> beam.frd, beam.dat
python check.py
# visualise: cgx -v beam.frd   (CalculiX GraphiX) or convert with ccx2paraview
