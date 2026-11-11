// Self-checking testbench (iverilog) - golden model written behaviourally
`timescale 1ns/1ps
module tb;
    reg [7:0] a, b; reg [2:0] op;
    wire [7:0] y; wire carry, zero;
    reg [8:0] exp; integer i, errors;
    alu dut(.a(a), .b(b), .op(op), .y(y), .carry(carry), .zero(zero));
    initial begin
        errors = 0;
        for (i = 0; i < 20000; i = i + 1) begin
            a = $urandom; b = $urandom; op = $urandom; #1;
            case (op)
                0: exp = a + b;           1: exp = {1'b0,a} - {1'b0,b};
                2: exp = a & b;           3: exp = a | b;
                4: exp = a ^ b;           5: exp = {1'b0,a} << b[2:0];
                6: exp = a >> b[2:0];     default: exp = (a < b);
            endcase
            if ({carry, y} !== exp || zero !== (exp[7:0] == 0)) begin
                errors = errors + 1;
                if (errors < 5) $display("MISMATCH op=%0d a=%0d b=%0d got=%0d exp=%0d", op, a, b, {carry,y}, exp);
            end
        end
        $display("TB finished: %0d errors", errors);
        $finish;
    end
endmodule
