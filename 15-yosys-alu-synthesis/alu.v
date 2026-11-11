// 8-bit ALU: add, sub, and, or, xor, shl, shr, set-less-than
module alu (
    input  wire [7:0] a,
    input  wire [7:0] b,
    input  wire [2:0] op,
    output wire [7:0] y,
    output wire       carry,
    output wire       zero
);
    reg [8:0] r;
    always @* begin
        case (op)
            3'd0: r = {1'b0, a} + {1'b0, b};
            3'd1: r = {1'b0, a} - {1'b0, b};
            3'd2: r = {1'b0, a & b};
            3'd3: r = {1'b0, a | b};
            3'd4: r = {1'b0, a ^ b};
            3'd5: r = {1'b0, a} << b[2:0];
            3'd6: r = {1'b0, a >> b[2:0]};
            default: r = {8'd0, (a < b)};
        endcase
    end
    assign y     = r[7:0];
    assign carry = r[8];
    assign zero  = (r[7:0] == 8'd0);
endmodule
