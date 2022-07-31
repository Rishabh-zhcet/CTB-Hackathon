# See LICENSE.vyoma for details

# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path
import numpy as np

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer

n=300
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

    Valid=0
    f=0     #Failed cased
    input_seq=[0,0,0,0,0];
    print('#----------------Valid Cases--------------#')   
    for i in range(2,n):
        await RisingEdge(dut.clk)
        input=random.randint(0,1)
        dut.w.value= input
        input_seq.append(input)
        await Timer(10, units='ns')

        #----------------Valid Cases------------------------#
        
        #Checking for non overlapping sequence of last 3 bits
        if(i%3==0):

            Valid=Valid+1
            #checking the parity bit by doing XOR operation on all three inputs

            if( (input_seq[i] ^ input_seq[i+1] ^input_seq[i+2])==1):
                
                if(dut.p.value==1):
                    result='------PASSED------'
                else:
                    result='------FAILED------'
                    f=f+1
            else:
                if(dut.p.value==1):
                    result='------FAILED EXPLICITLY------'
                    f=f+1
                else:
                    result='------------------'

            dut._log.info(f'last 3bits seq={input_seq[i:i+3]}  Parity={dut.p.value}, result={result}, i={i}')
            #assert dut.out.value == INPUT[i], "MUX output failed with: sel={SEL},  output={OUT}" .format( SEL= dut.sel.value, OUT=dut.out.value)
    print(f'***************************************************************************')
    print(f'*  Total Cases={n}, Valid Cases={Valid} Failed Cases={f}, Passed Cases={Valid-f}  *')
    print(f'***************************************************************************')
    assert f==0, 'Output Fails for some inputs'
         
@cocotb.test()
async def test_parity_generator_2(dut):
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

    Invalid=0
    f=0     #Failed cased
    input_seq=[0,0,0,0,0];
    print('#-------------------------------------------#\n#----------------Invalid Cases--------------#\n#-------------------------------------------#') 
    for i in range(2,n):
        await RisingEdge(dut.clk)
        input=random.randint(0,1)
        dut.w.value= input
        input_seq.append(input)
        await Timer(10, units='ns')

        #----------------Invalid Cases------------------------#
        #Checking for non overlapping sequence of last 3 bits
        if(i%3!=0):
            
            Invalid=Invalid+1
            #checking the parity bit by doing XOR operation on all three inputs
            if( (input_seq[i] ^ input_seq[i+1] ^input_seq[i+2])==1):
                
                if(dut.p.value==1):
                    result='------PASSED------'
                else:
                    result='------FAILED------'
                    f=f+1
            else:
                if(dut.p.value==1):
                    result='------FAILED EXPLICITLY------'
                    f=f+1
                else:
                    result='------------------'
                    f=f+1

            dut._log.info(f'last 3bits seq={input_seq[i:i+3]}  Parity={dut.p.value}, result={result}, i={i}')
            #assert dut.out.value == INPUT[i], "MUX output failed with: sel={SEL},  output={OUT}" .format( SEL= dut.sel.value, OUT=dut.out.value)
    print(f'***************************************************************************')
    print(f'*  Total Cases={n}, Invalid Cases={Invalid} Failed Cases={f}, Passed Cases={Invalid-f}  *')
    print(f'***************************************************************************')
    assert (Invalid-f)==0, 'Output Passes for some inputs'
