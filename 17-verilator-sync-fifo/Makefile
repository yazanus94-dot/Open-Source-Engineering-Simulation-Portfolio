all: run
obj_dir/Vfifo: fifo.v tb.cpp
	verilator -Wall --cc fifo.v --exe tb.cpp --trace --build -j 0
run: obj_dir/Vfifo
	./obj_dir/Vfifo
	@echo "Waveform: gtkwave fifo.vcd"
lint:
	verilator --lint-only -Wall fifo.v
clean:
	rm -rf obj_dir fifo.vcd
