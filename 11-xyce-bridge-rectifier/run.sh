#!/bin/bash
set -e
Xyce bridge.cir        # serial; parallel: mpirun -np 4 Xyce bridge.cir
python analyze.py
