`timescale 1ns/1ps
module uart_tb;
 
reg clk, rst;
reg [7:0] data_in;
reg wr_en;
reg rdy_clr;
wire rdy;
wire [7:0] dout;
wire busy;

uart_top Main ( rst, data_in, wr_en, clk, rdy_clr, rdy, busy, dout);

initial 
 begin 
   $dumpfile("UART.vcd");
   $dumpvars(0,uart_tb);
   
   clk = 0;
   rst = 1;  //reset active  
   data_in = 0; 
   rdy_clr = 0;
   wr_en = 0;
  
   repeat(5) @(posedge clk);
   rst = 0;

   send_byte(8'h41);
   repeat(2) @(posedge clk);
   wait(!busy);  //wait until busy = 0
   wait(rdy);
   $display("recived data is %h ", dout);
   clear_ready;

   repeat(2) @(posedge clk);      //added
   send_byte(8'h55);
   repeat(2) @(posedge clk); //waits for 2 rising edge 
   wait(!busy);
   wait(rdy);
   $display("recived data is %h ", dout);
   clear_ready;

   #5000000 $finish; 
 
 end

 always #5 clk = ~clk;


 
 task send_byte (input [7:0] din);
  begin
   @(negedge clk);
    wr_en = 1'b1;
    data_in = din;

   @(negedge clk);
    wr_en = 1'b0;
  end 
 endtask

 task clear_ready;
  begin
   @(negedge clk)
    rdy_clr = 1'b1;
   @(negedge clk)
    rdy_clr = 1'b0;
  end
 endtask

   
endmodule
 