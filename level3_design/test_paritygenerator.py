# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path
import numpy as np

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer

@cocotb.test()
async def test_parity_generator(dut):
    """Test for seq detection """

   
    #dut.seq_seen.value= output

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start())        # Start the clock

    # reset
    dut.reset.value = 1
    await RisingEdge(dut.clk) 
    await Timer(2, units='ns')

    dut.reset.value = 0
    await RisingEdge(dut.clk)
    await Timer(2, units='ns')

    input_seq=[0,0,0,0,0];
    for i in range(2,300):
        await RisingEdge(dut.clk)
        input=random.randint(0,1)
        dut.w.value= input
        input_seq.append(input)
        await Timer(10, units='ns')

        #Checking for non overlapping sequence of last 3 bits
        if(i%3==0):
            #checking the parity bit by doing XOR operation on all three inputs
            if( (input_seq[i] ^ input_seq[i+1] ^input_seq[i+2])==1):
                
                if(dut.p.value==1):
                    result='------PASSED------'
                else:
                    result='------FAILED------'
            else:
                if(dut.p.value==1):
                    result='------FAILED EXPLICITLY------'
                else:
                    result='------------------'

            dut._log.info(f'last 3bits seq={input_seq[i:i+3]}  Parity={dut.p.value}, result={result}, i={i}')
            #assert dut.out.value == INPUT[i], "MUX output failed with: sel={SEL},  output={OUT}" .format( SEL= dut.sel.value, OUT=dut.out.value)
            