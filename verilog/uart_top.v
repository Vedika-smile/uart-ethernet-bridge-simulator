module uart_top (input rst, input [7:0] data_in, input wr_enb, clk, rdy_clr, output rdy, busy, output [7:0] data_out);

wire tx_enb, rx_enb; // collecting output of baud rate gen

wire tx_temp;              // connecting output of tx module 

baudrate_gen bg (clk,rst, tx_enb, rx_enb);
UART_TX trans ( tx_temp, busy, clk, wr_enb, tx_enb, rst, data_in);
UART_RX rx (clk,rst,tx_temp,rdy_clr, rx_enb, rdy, data_out);

endmodule 

