module UART_RX (input clk,rst,rx,rdy_clr,clk_en,output reg rdy,output reg [7:0] data_out);
 parameter start=2'b00, data_state =2'b01, stop = 2'b10;
 reg [1:0] state = start;
 reg [3:0] sample = 0;
 reg [2:0] index = 0;
 reg [7:0] temp = 8'b0;

 always @(posedge clk)
  begin 
   if (rst) 
    begin
     rdy <= 0;
    data_out <= 0;
    state <= start;
    sample <= 0;
    index <= 0;
    temp <= 0;
    end

   else if (rdy_clr) // highest priority clear ready immeadiately 
    rdy <= 1'b0;
   else if (clk_en) begin // clk_enb from baudrate
    case(state) 
      start : begin
        if (rx == 0) 
         sample <= sample + 1;
	else 
	  sample <= 0;

        if (sample == 7) //half bit or middle
          begin
           state <= data_state;
           sample <= 0;
           index <= 0;
           temp <= 0;
         end
       end

      // data_state : begin
         // sample <= sample + 1;
        // if (sample == 8)
         // begin
          // temp[index] <= rx;
           //index <= index + 1; 
      
        //  end
        
        // if (index == 8 && sample == 4'hf) begin
          //state <= stop;
         // sample <= 0 ;
       //  end
  
        //end

      data_state : begin
         sample <= sample + 1;
         if (sample == 8) begin      // Sample at bit middle
           temp[index] <= rx;
           if (index == 7) begin     // 8th bit done
             state <= stop;
             sample <= 0;
           end
           else
             index <= index + 1;
         end
       end

       stop : 
        begin
         if (sample == 15)
          begin
           state <= start;
           data_out <= temp;
           rdy <= 1;
           sample <= 0;
          end
         else
          sample <= sample + 1;
        end
       
       default: state <= start;
  
      endcase
    end
  end
endmodule 
  