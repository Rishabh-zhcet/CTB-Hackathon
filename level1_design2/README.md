# Sequence Detector (level1_design2)

The verification environment is setup using Vyoma's UpTickPro provided for the hackathon.

![image](https://user-images.githubusercontent.com/65393666/182014417-a655843a-065d-4d84-a3dd-ba18d8a130f1.png)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed.

Clock signal of 10us period is created and For loop is used to give random input bits either '1' or '0'.
```
for i in range(n):
        await RisingEdge(dut.clk)
        input=random.randint(0,1)
        dut.inp_bit.value= input
        input_seq.append(input)
        await Timer(2, units='ns')
```

Now inside the For loop, if and else statements are used to check the ouput for each test case. 
The valid case is of last four bits='1011'. If the output fails, F is increased for each failed test case.

```
        if(input_seq[i+1:i+5]==[1 , 0, 1, 1]):
            valid_case=valid_case+1
            if(dut.seq_seen.value==1):
                result='-----------PASSED------------'
            else:
                result='-----------FAILED------------'
                f=f+1

        else:
            if(dut.seq_seen.value==1):
                result='------FAILED EXPLICITLY------'
                f=f+1
            else:
                #Implicitly PASSED Case
                result='-----------------------------'
     
        dut._log.info(f'Next_Input_bit={input}  last 4bits seq={input_seq[i+1:i+5]}  output={dut.seq_seen.value}, result={result}')
        
```

Finally at the end,Total Cases, Valid Cases, Failed Cases and Passed Cases are printed.

Assert statement is used to check if there is any test fails in the design by checking the value of f==0.

## Test Scenario

### 1st scenario(overlapped input)

```
1660002.00ns INFO     Next_Input_bit=1  last 4bits seq=[0, 1, 0, 0]  output=0, result=-----------------------------
1670002.00ns INFO     Next_Input_bit=0  last 4bits seq=[1, 0, 0, 1]  output=0, result=-----------------------------
1680002.00ns INFO     Next_Input_bit=1  last 4bits seq=[0, 0, 1, 0]  output=0, result=-----------------------------
1690002.00ns INFO     Next_Input_bit=1  last 4bits seq=[0, 1, 0, 1]  output=0, result=-----------------------------
1700002.00ns INFO     Next_Input_bit=0  last 4bits seq=[1, 0, 1, 1]  output=1, result=-----------PASSED------------
1710002.00ns INFO     Next_Input_bit=1  last 4bits seq=[0, 1, 1, 0]  output=0, result=-----------------------------
1720002.00ns INFO     Next_Input_bit=1  last 4bits seq=[1, 1, 0, 1]  output=0, result=-----------------------------
1730002.00ns INFO     Next_Input_bit=0  last 4bits seq=[1, 0, 1, 1]  output=0, result=-----------FAILED------------
1740002.00ns INFO     Next_Input_bit=0  last 4bits seq=[0, 1, 1, 0]  output=0, result=-----------------------------
```

### 2nd scenario(non-overlapped input)

```
1300002.00ns INFO     Next_Input_bit=1  last 4bits seq=[1, 0, 1, 0]  output=0, result=-----------------------------
1310002.00ns INFO     Next_Input_bit=0  last 4bits seq=[0, 1, 0, 1]  output=0, result=-----------------------------
1320002.00ns INFO     Next_Input_bit=1  last 4bits seq=[1, 0, 1, 0]  output=0, result=-----------------------------
1330002.00ns INFO     Next_Input_bit=1  last 4bits seq=[0, 1, 0, 1]  output=0, result=-----------------------------
1340002.00ns INFO     Next_Input_bit=0  last 4bits seq=[1, 0, 1, 1]  output=1, result=-----------PASSED------------
1350002.00ns INFO     Next_Input_bit=1  last 4bits seq=[0, 1, 1, 0]  output=0, result=-----------------------------
1360002.00ns INFO     Next_Input_bit=0  last 4bits seq=[1, 1, 0, 1]  output=0, result=-----------------------------
1370002.00ns INFO     Next_Input_bit=1  last 4bits seq=[1, 0, 1, 0]  output=0, result=-----------------------------
1380002.00ns INFO     Next_Input_bit=1  last 4bits seq=[0, 1, 0, 1]  output=0, result=-----------------------------
1390002.00ns INFO     Next_Input_bit=1  last 4bits seq=[1, 0, 1, 1]  output=1, result=-----------PASSED------------
```

From 1st and 2nd scenario, we can see that the design works well for non-overlapping inputs and fails for overlappig inputs. Hence the design has bug.

## Design Bug

```
  // state transition based on the input and current state
  always @(inp_bit or current_state)
  begin
    case(current_state)
      IDLE:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1;
        else
          next_state = IDLE;
      end
      SEQ_1:
      begin
        if(inp_bit == 1)
          next_state = IDLE;                            ===> BUG
        else
          next_state = SEQ_10;
      end
      SEQ_10:
      begin
        if(inp_bit == 1)
          next_state = SEQ_101;
        else
          next_state = IDLE;
      end
      SEQ_101:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1011;
        else
          next_state = IDLE;                            ===> BUG
      end
      SEQ_1011:
      begin
        next_state = IDLE;                              ===> BUG
      end
    endcase
  end
```

These bugs are checked from the test cases and the state diagram of the FSM. 

## Design Fix

The Changes are fixed by fixing the statediagram of the design.

_Earlier State Diagram_

![buggy](https://user-images.githubusercontent.com/65393666/182021214-137ae491-39b6-4263-89cd-06853731dec2.png)

_New State Diagram_

![fixed](https://user-images.githubusercontent.com/65393666/182021232-7eecd237-b8dc-4e2b-afe6-7feb052fb13d.png)

Accordingly the Code is modified as follows, the modified code is checked in as seq_detect_1011_fix.v

```
always @(inp_bit or current_state)
  begin
    case(current_state)
      IDLE:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1;                   ===> Modified
        else
          next_state = IDLE;
      end
      SEQ_1:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1;
        else
          next_state = SEQ_10;
      end
      SEQ_10:
      begin
        if(inp_bit == 1)
          next_state = SEQ_101;                 
        else
          next_state = IDLE;
      end
      SEQ_101:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1011;                
        else
          next_state = SEQ_10;                  ===> Modified
      end
      SEQ_1011:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1;                   ===> Modified        
        else
          next_state = SEQ_10;                  ===> Modified
      end
    endcase
  end
```

After all the changes in the design, test is run again and all the valid cases are verified!

![image](https://user-images.githubusercontent.com/65393666/182023260-7340195b-33f0-4d57-9949-bebb9044d488.png)

In this also,a flag is incorporated to check if any of the test fails.
The complete design verification is indicated by assert statement.
```
    print(f'***************************************************************************')
    print(f'*  Total Cases={n}, Valid Cases={valid_case} Failed Cases={f}, Passed Cases={valid_case-f}  *')
    print(f'***************************************************************************')

    assert f==0, 'The design fails for Some inputs'
```

## Verification Strategy

The verification streategy was to provide a new random input to the sequence detector and check if the ouput is '1' for the sequnce '1011'. 

Here valid case is the case in which the last 4 bits of the sequence is '1011' and rest all cases are considered as the invalid cases.The random inputs are provided using loop and random function. The result is verified for the valid cases as well as for the invalid cases if the output fails.

For Valid cases we look for the '1' at the ouput and for all the invalid cases we look for the '0' at the output.


## Is the verification complete ?

Since all the possiblities for valid and invalid cases are verified for 1000 random inputs, we can say that the verification is complete.

