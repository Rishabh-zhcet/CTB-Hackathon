# Multiplexer Design Verification(level1_design1)


The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![image](https://user-images.githubusercontent.com/65393666/181939156-770b0991-845e-4f8f-b921-b8e07808d0df.png)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed.

An array named 'INPUT' of 31 elements is declared with each element='1' ---'HIGH'

INPUT=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

Now the each input is driven by each element of the array respectively,

```
    dut.inp0.value=INPUT[0]
    dut.inp1.value=INPUT[1]
    dut.inp2.value=INPUT[2]
    dut.inp3.value=INPUT[3]
    dut.inp4.value=INPUT[4]
     .     .     .      .
     .     .     .      .
     .     .     .      .
    dut.inp29.value=INPUT[29]
    dut.inp30.value=INPUT[30]
```

The for loop is used to check the output for each select input. 

dut._log.info is used for checking input and ouput.

```
for i in range (31):
        SEL=i
        dut.sel.value= SEL

        await Timer(2, units='ns')

        dut._log.info(f'Sel={SEL:05} Input={INPUT[i]:02} DUT_OUTPUT={(dut.out.value)}')
```

Now if statement is used inside for loop to check the result for each test case, if fail, the following statement is used to print the error message. The flag is also made eqaul to 1.

```
 if (dut.out.value != INPUT[i]):
            print(f"FOR: sel={SEL},  INPUT!=OUTPUT        [test]  [------------Failed------------]")
            flag=1
```
if flag is not equal to 1. means no test fails. Then assert statement is used for checking the complete verification of design.

  ```
  assert flag== 0, "MUX output failed "
```

## Test Scenario **(Important)**

Following error message exposed that there is a bug in the design:'

- 6.00ns INFO     Sel=00012 Input=01 DUT_OUTPUT=00
- FOR: sel=12,  INPUT!=OUTPUT        [test]  [------------Failed------------]

Another Error Message:

- 62.00ns INFO     Sel=00030 Input=01 DUT_OUTPUT=00
- FOR: sel=30,  INPUT!=OUTPUT        [test]  [------------Failed------------]


Output mismatches for the above inputs proving that there is a design bug. This also gives us information about which inputs fails the test.

## Design Bug
Based on the above test input and analysing the design, we see the following

```
 case(sel)
      5'b00000: out = inp0;  
      5'b00001: out = inp1;  
      5'b00010: out = inp2;  
      5'b00011: out = inp3;  
      5'b00100: out = inp4;  
      5'b00101: out = inp5;  
      5'b00110: out = inp6;  
      5'b00111: out = inp7;  
      5'b01000: out = inp8;  
      5'b01001: out = inp9;  
      5'b01010: out = inp10;
      5'b01011: out = inp11;
      5'b01101: out = inp12;        ===>BUG
      5'b01101: out = inp13;
      5'b01110: out = inp14;
      5'b01111: out = inp15;
      5'b10000: out = inp16;
      5'b10001: out = inp17;
      5'b10010: out = inp18;
      5'b10011: out = inp19;
      5'b10100: out = inp20;
      5'b10101: out = inp21;
      5'b10110: out = inp22;
      5'b10111: out = inp23;
      5'b11000: out = inp24;
      5'b11001: out = inp25;
      5'b11010: out = inp26;
      5'b11011: out = inp27;
      5'b11100: out = inp28;
      5'b11101: out = inp29;
                                    ===>BUG
      default: out = 0;
    endcase
```
For the selecting inp12 the select input 'sel' should be '1100' instead of '1101'.

Also, as we are verifying a 31x1 mux, it should have 31 inputs. In this case there were only 30 inputs and select condition of inp30 was not given in the design. 
Hence, one select case should be added for inp30.

## Design Fix
Updating the design and re-running the test makes the test pass.

![image](https://user-images.githubusercontent.com/65393666/181988568-8d73488f-d5b4-405f-8d9b-5fbd1af198c6.png)

The updated design is checked in as mux_fix.v

## Verification Strategy

The idea was to under the design specification. Accordingly for mux, need to assign a value to input and test the same value at output for a partiular select input.
Hence an array is designed with size equal to input ports. A flag signal is used to detect is the output fails for any of the select input.

## Is the verification complete ?

As the design is tested for each possible combination of select inputs, we can say that the verification for this design is complete.
