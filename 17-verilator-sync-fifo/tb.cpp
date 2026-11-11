// Verilator C++ testbench: random traffic checked against a std::queue reference model, VCD waveform dump
#include <cstdio>
#include <cstdlib>
#include <queue>
#include <memory>
#include "Vfifo.h"
#include "verilated.h"
#include "verilated_vcd_c.h"

static vluint64_t sim_time = 0;

static void tick(Vfifo* top, VerilatedVcdC* tfp) {
    top->clk = 0; top->eval(); tfp->dump(sim_time++);
    top->clk = 1; top->eval(); tfp->dump(sim_time++);
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    Verilated::traceEverOn(true);
    auto* top = new Vfifo;
    auto* tfp = new VerilatedVcdC;
    top->trace(tfp, 99);
    tfp->open("fifo.vcd");

    std::queue<int> ref;
    int errors = 0, writes = 0, reads = 0, max_fill = 0;
    srand(1234);

    top->rst_n = 0; top->wr_en = 0; top->rd_en = 0; top->din = 0;
    for (int i = 0; i < 4; i++) tick(top, tfp);
    top->rst_n = 1;

    for (int cyc = 0; cyc < 200000; cyc++) {
        // bursty traffic: alternate write-heavy and read-heavy phases to hit full and empty
        int phase = (cyc / 500) % 2;
        top->wr_en = (rand() % 100) < (phase ? 30 : 80);
        top->rd_en = (rand() % 100) < (phase ? 80 : 30);
        top->din = rand() & 0xFF;
        top->clk = 0; top->eval();                 // settle combinational full/empty
        bool do_wr = top->wr_en && !top->full;
        bool do_rd = top->rd_en && !top->empty;
        int expected = 0;
        if (do_rd) { expected = ref.front(); ref.pop(); reads++; }
        if (do_wr) { ref.push(top->din); writes++; }
        if ((int)ref.size() > max_fill) max_fill = ref.size();
        tick(top, tfp);
        if (do_rd && top->dout != expected) {
            if (errors < 5) printf("MISMATCH cycle %d: got %d expected %d\n", cyc, top->dout, expected);
            errors++;
        }
        if (top->full != (ref.size() == 16) || top->empty != ref.empty()) {
            if (errors < 5) printf("FLAG MISMATCH cycle %d\n", cyc);
            errors++;
        }
    }
    printf("writes=%d reads=%d max_fill=%d errors=%d -> %s\n", writes, reads, max_fill, errors, errors ? "FAIL" : "PASS");
    tfp->close(); top->final(); delete tfp; delete top;
    return errors ? 1 : 0;
}
