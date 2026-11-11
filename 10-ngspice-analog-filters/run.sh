#!/bin/bash
set -e
ngspice -b rlc_lowpass.cir -o rlc.log
ngspice -b rc_diode_clipper.cir -o clipper.log
python plot.py
