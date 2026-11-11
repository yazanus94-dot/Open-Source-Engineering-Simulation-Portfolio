// Synchronous FIFO, registered read data, power-of-two depth
module fifo #(
    parameter WIDTH = 8,
    parameter ADDR  = 4
) (
    input  wire             clk,
    input  wire             rst_n,
    input  wire             wr_en,
    input  wire             rd_en,
    input  wire [WIDTH-1:0] din,
    output reg  [WIDTH-1:0] dout,
    output wire             full,
    output wire             empty
);
    reg [WIDTH-1:0] mem [0:(1<<ADDR)-1];
    reg [ADDR:0] wptr, rptr;

    assign empty = (wptr == rptr);
    assign full  = (wptr[ADDR-1:0] == rptr[ADDR-1:0]) && (wptr[ADDR] != rptr[ADDR]);

    wire do_wr = wr_en && !full;
    wire do_rd = rd_en && !empty;

    always @(posedge clk) begin
        if (!rst_n) begin
            wptr <= 0;
            rptr <= 0;
            dout <= 0;
        end else begin
            if (do_wr) begin
                mem[wptr[ADDR-1:0]] <= din;
                wptr <= wptr + 1'b1;
            end
            if (do_rd) begin
                dout <= mem[rptr[ADDR-1:0]];
                rptr <= rptr + 1'b1;
            end
        end
    end
endmodule
