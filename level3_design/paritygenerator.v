`timescale 1ns / 1ps

module Top_module(
input w,
input clk,
input reset,
output reg p
   );

reg [2:0] PS, NS;
parameter S0=3'b000, S1=3'b001,S2=3'b010, S3=3'b011,  S4=3'b100, S5=3'b101;         

initial    
begin
PS=3'b000;
NS=3'b000;
end

always@(w,PS)
begin
case(PS)
S0: begin
    p=1'b0;
    if(!w)  NS=S1;
    else    NS=S2;
    end

S1: begin
    p=1'b0;
    if(!w)  NS=S3;
    else    NS=S4;
    end    
    
S2: begin
    p=1'b0;
    if(!w)  NS=S4;
    else    NS=S3;
    end 


S3: begin
    p=1'b0;
    if(!w)  NS=S0;
    else    NS=S5;
    end 
   
S4: begin
    p=1'b0;
    if(!w)  NS=S5;
    else    NS=S0;
    end 


S5: begin
    p=1'b1;
    if(!w)  NS=S1;
    else    NS=S2;
    end
    
default: begin end 
endcase
end  
    
always@(posedge clk)
begin
    if(reset)
        PS<=S0;
    else
        PS<=NS;
end


endmodule
