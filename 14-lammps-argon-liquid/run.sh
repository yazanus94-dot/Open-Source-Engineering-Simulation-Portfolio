#!/bin/bash
set -e
mpirun -np ${NP:-4} lmp -in in.argon -log log.argon
python analyze.py
