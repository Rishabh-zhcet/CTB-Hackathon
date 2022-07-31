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

    

## Design Fix

## Verification Strategy



## Is the verification complete ?

