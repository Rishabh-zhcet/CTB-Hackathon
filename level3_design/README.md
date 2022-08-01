# Parity Generator(level3_design)

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![Screenshot (1224)](https://user-images.githubusercontent.com/65393666/182028028-087790db-2c14-4328-93b5-4732a5c92191.png)

## Verification Environment
The [CoCoTb](https://www.cocotb.org/) based Python test is developed. As our design is a 3-bit parity generator for non-overlapping inputs. We have generated two test cases in same file: one for checking the output on Valid cases and one for checking the output on invalid cases.

The random sequence of '1' or '0' is generated using random function and appended to an empty array using for loop.

```
for i in range(2,n):
        await RisingEdge(dut.clk)
        input=random.randint(0,1)
        dut.w.value= input
        input_seq.append(input)
        await Timer(10, units='ns')
```
**The Whole verification code is devided into two parts:**

**1) TEST1: For Valid Cases** 

**2) TEST2: For Invalid Cases**

### TEST1: Checking Valid cases

Valid cases are after every 3 bits, we have to check the output not after occurace of each bit. So we have to basicalling do the parsing of 3-3 bits. 
**In this we look if we are getting output 'FAILED' for any valid case.**

For all the valid cases, if the output=1, then the test is **"PASSED"**, otherwise **"FAILED".**

For all Valid cases if the "FAILED" cases are zero then the **TEST1** is **"PASS".**

```
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
            
```
Here 'f' is the number of **FAILED** cases. 
If these are zero, then the test 1 is "PASSED".

assert statement is used to final check of valid cases, which is not in the loop.

```
print(f'***************************************************************************')
    print(f'*  Total Cases={n}, Valid Cases={Valid} Failed Cases={f}, Passed Cases={Valid-f}  *')
    print(f'***************************************************************************')
    assert f==0, 'Output Fails for some inputs'
```
### TEST2: Checking Invalid cases

Rest all cases except valid cases are Invalid. We expect the design do not "PASS" any invalid case.

For all the invalid cases, if the output=0, then the test is **"FAILED"**, otherwise **"PASSED".**

For all Valid cases if the "PASSED" cases are zero then the **TEST1** is **"PASS".**

```
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

```
Here 'f' is the number of **FAILED** cases. 
If all cases failed then (Valid cases-failed cases)=0 and the **TEST2** for checking the design for invalid cases is **"PASS"**.

assert statement is used to final check of invalid cases, which is not in the loop.
```
    print(f'***************************************************************************')
    print(f'*  Total Cases={n}, Invalid Cases={Invalid} Failed Cases={f}, Passed Cases={Invalid-f}  *')
    print(f'***************************************************************************')
    assert (Invalid-f)==0, 'Output Passes for some inputs'
```
## Introducing Bug to the Design

One state of FSM is changed with other.

The buggy design is checked in as **buggy_parity_generator.v**
```

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
    //###-------------BUG INSERTED HERE------------### S2 is replaced with S0 in else case
    else    NS=S0; 
    end
    
default: begin end 
endcase
end  
```

## Test Scenario 

### TEST1: test_parity_generator 
```
#----------------Valid Cases--------------#
 30010.00ns INFO     last 3bits seq=[0, 0, 0]  Parity=0, result=------------------, i=3
 60010.00ns INFO     last 3bits seq=[1, 1, 1]  Parity=1, result=------PASSED------, i=6
 90010.00ns INFO     last 3bits seq=[1, 1, 0]  Parity=0, result=------------------, i=9
120010.00ns INFO     last 3bits seq=[1, 0, 0]  Parity=0, result=------FAILED------, i=12
.                .                .                .                .                .                  
.                .                .                .                .                .     
.                .                .                .                .                .     
2730010.00ns INFO     last 3bits seq=[1, 1, 0]  Parity=0, result=------------------, i=273
2760010.00ns INFO     last 3bits seq=[0, 1, 0]  Parity=1, result=------PASSED------, i=276
2790010.00ns INFO     last 3bits seq=[0, 1, 0]  Parity=1, result=------PASSED------, i=279
2820010.00ns INFO     last 3bits seq=[1, 1, 0]  Parity=0, result=------------------, i=282
2850010.00ns INFO     last 3bits seq=[1, 0, 1]  Parity=0, result=------------------, i=285
2880010.00ns INFO     last 3bits seq=[1, 1, 0]  Parity=0, result=------------------, i=288
2910010.00ns INFO     last 3bits seq=[0, 0, 0]  Parity=0, result=------------------, i=291
2940010.00ns INFO     last 3bits seq=[0, 0, 0]  Parity=0, result=------------------, i=294
2970010.00ns INFO     last 3bits seq=[1, 0, 1]  Parity=0, result=------------------, i=297
***************************************************************************
*  Total Cases=300, Valid Cases=99 Failed Cases=35, Passed Cases=64  *
***************************************************************************
```
### TEST2:test_parity_generator_2

```
#-------------------------------------------#
#----------------Invalid Cases--------------#
#-------------------------------------------#
3020020.00ns INFO     last 3bits seq=[0, 0, 0]  Parity=0, result=------------------, i=2
3040020.00ns INFO     last 3bits seq=[0, 0, 0]  Parity=0, result=------------------, i=4
3050020.00ns INFO     last 3bits seq=[0, 0, 0]  Parity=0, result=------------------, i=5
3070020.00ns INFO     last 3bits seq=[0, 1, 1]  Parity=0, result=------------------, i=7
3080020.00ns INFO     last 3bits seq=[1, 1, 1]  Parity=0, result=------FAILED------, i=8
3100020.00ns INFO     last 3bits seq=[1, 1, 0]  Parity=0, result=------------------, i=10
.                .                .                .                .                .                  
.                .                .                .                .                .     
.                .                .                .                .                .     
5840020.00ns INFO     last 3bits seq=[0, 0, 1]  Parity=1, result=------PASSED------, i=284
5860020.00ns INFO     last 3bits seq=[1, 1, 0]  Parity=0, result=------------------, i=286
5870020.00ns INFO     last 3bits seq=[1, 0, 1]  Parity=0, result=------------------, i=287
5890020.00ns INFO     last 3bits seq=[1, 0, 0]  Parity=0, result=------FAILED------, i=289
5900020.00ns INFO     last 3bits seq=[0, 0, 0]  Parity=0, result=------------------, i=290
5920020.00ns INFO     last 3bits seq=[0, 1, 1]  Parity=0, result=------------------, i=292
5930020.00ns INFO     last 3bits seq=[1, 1, 0]  Parity=0, result=------------------, i=293
5950020.00ns INFO     last 3bits seq=[0, 1, 1]  Parity=0, result=------------------, i=295
5960020.00ns INFO     last 3bits seq=[1, 1, 0]  Parity=0, result=------------------, i=296
5980020.00ns INFO     last 3bits seq=[0, 1, 1]  Parity=0, result=------------------, i=298
5990020.00ns INFO     last 3bits seq=[1, 1, 1]  Parity=0, result=------FAILED------, i=299
***************************************************************************
*  Total Cases=300, Invalid Cases=199 Failed Cases=176, Passed Cases=23  *
***************************************************************************
```

### final result
```
                      
5990020.00ns INFO     ******************************************************************************************************
                      ** TEST                                          STATUS  SIM TIME (ns)  REAL TIME (s)  RATIO (ns/s) **
                      ******************************************************************************************************
                      ** test_paritygenerator.test_parity_generator     FAIL     2990010.00           0.07   41133443.02  **
                      ** test_paritygenerator.test_parity_generator_2   FAIL     3000010.00           0.09   34629632.34  **
                      ******************************************************************************************************
                      ** TESTS=2 PASS=0 FAIL=2 SKIP=0                            5990020.00           0.55   10838723.02  **
                      ******************************************************************************************************
```

The message above shows that there is a bug in the design but we aren't find exactly where the bug is. for this we have to look for design specification and its state diagram.
## Verification Strategy

To check is the design fails on any of the valid cases. The random inputs are given using random function.

## Is the verification complete ?

yes, as the design has been checked for 300 input sequences, the original design do not pass any error. In the buggy design, we have done a smaller change and it has been detected very easily.




