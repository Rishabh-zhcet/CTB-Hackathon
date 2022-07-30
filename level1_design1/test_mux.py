# See LICENSE.vyoma for details
 
import cocotb
from cocotb.triggers import Timer
import random

#For capturing first Bug
@cocotb.test()
async def test_mux_01(dut):
    """Test for mux2"""
     # input driving
 
    #Driving each input with '01'---'HIGH'
    INPUT=[,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1];
    dut.inp0.value=INPUT[0]
    dut.inp1.value=INPUT[1]
    dut.inp2.value=INPUT[2]
    dut.inp3.value=INPUT[3]
    dut.inp4.value=INPUT[4]
    dut.inp5.value=INPUT[5]
    dut.inp6.value=INPUT[6]
    dut.inp7.value=INPUT[7]
    dut.inp8.value=INPUT[8]
    dut.inp9.value=INPUT[9]
    dut.inp10.value=INPUT[10]
    dut.inp11.value=INPUT[11]
    dut.inp12.value=INPUT[12]
    dut.inp13.value=INPUT[13]
    dut.inp14.value=INPUT[14]
    dut.inp15.value=INPUT[15]
    dut.inp16.value=INPUT[16]
    dut.inp17.value=INPUT[17]
    dut.inp18.value=INPUT[18]
    dut.inp19.value=INPUT[19]
    dut.inp20.value=INPUT[20]
    dut.inp21.value=INPUT[21]
    dut.inp22.value=INPUT[22]
    dut.inp23.value=INPUT[23]
    dut.inp24.value=INPUT[24]
    dut.inp25.value=INPUT[25]
    dut.inp26.value=INPUT[26]
    dut.inp27.value=INPUT[27]
    dut.inp28.value=INPUT[28]
    dut.inp29.value=INPUT[29]
    dut.inp30.value=INPUT[30]
 
    
    for i in range (31):
        SEL=i
        dut.sel.value= SEL

        await Timer(2, units='ns')

        dut._log.info(f'Sel={SEL:05} Input={INPUT[i]:02} DUT={(dut.out.value)}')
        assert dut.out.value == INPUT[i], "MUX output failed with: sel={SEL},  output={OUT}" .format( SEL= dut.sel.value, OUT=dut.out.value)
 
#For capturing second Bug
@cocotb.test()
async def test_mux_02(dut):
    """Test for mux2"""
     # input driving
     #Driving each input with '01'---'HIGH'
    INPUT=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1];
    dut.inp0.value=INPUT[0]
    dut.inp1.value=INPUT[1]
    dut.inp2.value=INPUT[2]
    dut.inp3.value=INPUT[3]
    dut.inp4.value=INPUT[4]
    dut.inp5.value=INPUT[5]
    dut.inp6.value=INPUT[6]
    dut.inp7.value=INPUT[7]
    dut.inp8.value=INPUT[8]
    dut.inp9.value=INPUT[9]
    dut.inp10.value=INPUT[10]
    dut.inp11.value=INPUT[11]
    dut.inp12.value=INPUT[12]
    dut.inp13.value=INPUT[13]
    dut.inp14.value=INPUT[14]
    dut.inp15.value=INPUT[15]
    dut.inp16.value=INPUT[16]
    dut.inp17.value=INPUT[17]
    dut.inp18.value=INPUT[18]
    dut.inp19.value=INPUT[19]
    dut.inp20.value=INPUT[20]
    dut.inp21.value=INPUT[21]
    dut.inp22.value=INPUT[22]
    dut.inp23.value=INPUT[23]
    dut.inp24.value=INPUT[24]
    dut.inp25.value=INPUT[25]
    dut.inp26.value=INPUT[26]
    dut.inp27.value=INPUT[27]
    dut.inp28.value=INPUT[28]
    dut.inp29.value=INPUT[29]
    dut.inp30.value=INPUT[30]
 
    
    for i in range (13,31):
        SEL=i
        dut.sel.value= SEL

        await Timer(2, units='ns')

        dut._log.info(f'Sel={SEL:05} Input={INPUT[i]:02} DUT={(dut.out.value)}')
        assert dut.out.value == INPUT[i], "MUX output failed with: sel={SEL},  output={OUT}" .format( SEL= dut.sel.value, OUT=dut.out.value)
 