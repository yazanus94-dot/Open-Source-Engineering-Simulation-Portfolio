#!/bin/bash
set -e
iverilog -o sim tb.v alu.v && vvp sim            # RTL functional test
yosys -q -l yosys.log synth.ys                   # synth + equivalence check (fails if not equivalent)
cat stats.txt
iverilog -o sim_gate tb.v alu_gate.v && vvp sim_gate   # same testbench on the gate-level netlist
# diagram: yosys -p "read_verilog alu.v; hierarchy -top alu; proc; opt; show -format svg -prefix alu"
