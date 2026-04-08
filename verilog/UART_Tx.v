module UART_TX ( tx, busy, clk, wr_enb, enb, rst, data_in);
 output reg tx;
 output busy;
 input clk, wr_enb, rst, enb;
 input [7:0] data_in;

 reg [7:0] data;
 reg [2:0] index;
 reg [1:0] state;
 parameter idle=2'b00, start=2'b01, data_state=2'b10, stop=2'b11;
 

 always @(posedge clk) begin
   if (rst) begin
    tx <= 1'b1;
     state <= idle;
     index <= 3'h0;
     data <= 8'h0;  //just added
   end else begin                        //two always block should not drive same reg
    case (state)
     idle: begin 
 	tx <= 1'b1;
          if (wr_enb) 
           begin
	    state <= start;
	    data <= data_in;
            index <= 3'h0;
  	   end
          end
    start: begin
	    if (enb)   //baude rate enb 
             begin
 	      tx <= 1'b0;         // tx 1 -> 0 means start bit, 0 is start bit
              state <= data_state;
             end
           // else
             //state <= start;
           end
    data_state: 
     begin
      if (enb) begin 
       tx <= data [index];
        if (index == 3'h7) begin
         state <= stop;
        end
        else
          index <= index +3'h1;
        
       end
     end

 
    stop : 
     begin
      if (enb)
       begin 
        tx <= 1'b1;    //  1 is stop bit 
        state <= idle;
       end
     end
    default: begin
      tx <= 1'b1;
      state <= idle;
      
     end
   endcase
  end
  end

 assign busy = (state != idle) ? 1 : 0;   //state if not idle toh its busy

endmodule 

     
    
 		      