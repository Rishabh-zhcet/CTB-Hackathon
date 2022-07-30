# See LICENSE.iitm for details
# See LICENSE.vyoma for details

import random
import sys
import cocotb
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge
from cocotb.result import TestFailure
from cocotb.clock import Clock

from model_mkbitmanip import *

# Clock Generation
@cocotb.coroutine
def clock_gen(signal):
    while True:
        signal.value <= 0
        yield Timer(1) 
        signal.value <= 1
        yield Timer(1) 

# Sample Test
@cocotb.test()
def run_test(dut):

    # clock
    cocotb.fork(clock_gen(dut.CLK))

    # reset
    dut.RST_N.value <= 0
    yield Timer(10) 
    dut.RST_N.value <= 1
    
    ######### CTB : Modify the test to expose the bug #############
    # input transaction
    mav_putvalue_instr=[]
    mav_putvalue_src1 = 0x1A46D635
    mav_putvalue_src2 = 0x21116784
    mav_putvalue_src3 = 0x89862685
    p=0 #Pass Cases
    f=0 #Failed Cases
    #--ANDN 1
    mav_putvalue_instr.append( 0x40007033)
    #--ORN 2
    mav_putvalue_instr.append( 0x40006033)
    #--XNOR 3
    mav_putvalue_instr.append( 0x40004033)
    #--SLO  4
    mav_putvalue_instr.append( 0x20001033)
    #--SRO  5
    mav_putvalue_instr.append( 0x20005033)
    #--ROL  6
    mav_putvalue_instr.append( 0x60001033)
    #--ROR  7
    mav_putvalue_instr.append( 0x60005033)
    #--SH1ADD  8
    mav_putvalue_instr.append( 0x20002033)
    #--SH2ADD  9
    mav_putvalue_instr.append( 0x20004033)
    #--SH3ADD  10
    mav_putvalue_instr.append( 0x20006033)
    #--SBCLR   11
    mav_putvalue_instr.append( 0x48001033)
    #--SBSET   12
    mav_putvalue_instr.append( 0x28001033)
    #--SBINV  13
    mav_putvalue_instr.append( 0x68001033)
    #--SBEXT  14
    mav_putvalue_instr.append( 0x48005033)
    #--GORC 15 (check)
    mav_putvalue_instr.append( 0x28005033)
    #--GREV  16 (should check)
    mav_putvalue_instr.append( 0x68005033)
    #--CMIX  17
    mav_putvalue_instr.append( 0x06001033)
    #--CMOV 18
    mav_putvalue_instr.append( 0x06005033)
    #--FSL 19
    mav_putvalue_instr.append( 0x04001033)
    #--FSR  20(check)
    mav_putvalue_instr.append( 0x04005033)
    #--CLZ   21
    mav_putvalue_instr.append( 0x60001013)
    #--CTZ    22
    mav_putvalue_instr.append( 0x60101013)
    #--PCNT   23
    mav_putvalue_instr.append( 0x60201013)
    #--SEXT.B  24
    mav_putvalue_instr.append( 0x60401013)
    #--SEXT.H  25
    mav_putvalue_instr.append( 0x60501013)
    #--CRC32.B 26
    mav_putvalue_instr.append( 0x61001013)
    #--CRC32.H  27
    mav_putvalue_instr.append( 0x61101013)
    #--CRC32.W  28
    mav_putvalue_instr.append( 0x61201013)
    #--CRC32C.B 29
    mav_putvalue_instr.append( 0x61801013)
    #--CRC32C.H  30
    mav_putvalue_instr.append( 0x61901013)
    #--CRC32C.W  31
    mav_putvalue_instr.append( 0x61A01013)
    #--CLMUL  32
    mav_putvalue_instr.append( 0x0A001033)
    #--CLMULH  33
    mav_putvalue_instr.append( 0x0A003033)
    #--CLMULR  34
    mav_putvalue_instr.append( 0x0A002033)
    #--MIN  35
    mav_putvalue_instr.append( 0x0A004033)
    #--MAX 36
    mav_putvalue_instr.append( 0x0A005033)
    #--MINU  37
    mav_putvalue_instr.append( 0x0A006033)
    #--MAXU 38
    mav_putvalue_instr.append( 0x0A007033)
    #--BDEP 39
    mav_putvalue_instr.append( 0x48006033)
    #--BEXT 40
    mav_putvalue_instr.append( 0x08006033)
    #--PACK 41
    mav_putvalue_instr.append( 0x08004033)
    #--PACKU 42
    mav_putvalue_instr.append( 0x48004033)
    #--PACKH 45
    mav_putvalue_instr.append( 0x08007033)
    #--SLOI  46
    mav_putvalue_instr.append( 0x20001013)
    #--SROI 47
    mav_putvalue_instr.append( 0x22005013)
    #--RORI  48
    mav_putvalue_instr.append( 0x62005013)
    #--SBCLRI   49
    mav_putvalue_instr.append( 0x48001013)
    #--SBSETI   50
    mav_putvalue_instr.append( 0x28001013)
    #--SBINVI  51
    mav_putvalue_instr.append( 0x68001013)
    #--SBEXTI  52
    mav_putvalue_instr.append( 0x48005013)
    #--SHFL  53
    mav_putvalue_instr.append( 0x08001033)
    #--UNSHFL  54
    mav_putvalue_instr.append( 0x08005033)
    #--SHFLI  55 (check)
    mav_putvalue_instr.append( 0x08001013)
    #--UNSHFLI  56  (check)
    mav_putvalue_instr.append( 0x08005013)
    #--GORCI 57
    mav_putvalue_instr.append( 0x2A005013)
    #--GREVI  58
    mav_putvalue_instr.append( 0x6A005013)
    #--_FSRI  59
    mav_putvalue_instr.append( 0x04005013)
    #--BFP  60
    mav_putvalue_instr.append( 0x48007033)


    dut.mav_putvalue_src1.value = mav_putvalue_src1
    dut.mav_putvalue_src2.value = mav_putvalue_src2
    dut.mav_putvalue_src3.value = mav_putvalue_src3
    dut.EN_mav_putvalue.value = 1
    n=58
    for i in range(n):
    # expected output from the model
        expected_mav_putvalue = bitmanip(mav_putvalue_instr[i], mav_putvalue_src1, mav_putvalue_src2, mav_putvalue_src3)

    # driving the input transaction
    
        dut.mav_putvalue_instr.value = mav_putvalue_instr[i]
  
        yield Timer(1) 

        # obtaining the output
        dut_output = dut.mav_putvalue.value

        if(dut_output == expected_mav_putvalue):
            p=p+1;
            print('---------------pass-------')
            print(f'------------------------DUT OUTPUT={hex(dut_output)}-------EXPECTED OUTPUT={hex(expected_mav_putvalue)}\n')
        else:
            f=f+1
            print('---------------failed------')
            print(f'------------------------Value mismatch:  DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}\n'
        )

        #cocotb.log.info(f'DUT OUTPUT={hex(dut_output)}')
        #cocotb.log.info(f'EXPECTED OUTPUT={hex(expected_mav_putvalue)}')
        
        # comparison
        error_message = f'Value mismatch DUT = {hex(dut_output)} does not match MODEL = {hex(expected_mav_putvalue)}'
    print(f'Passed Cases={p}, Failed Cases={f}, Total Cases={n}')
    assert f==0, error_message
        