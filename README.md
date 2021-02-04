# esoteric-boolean-logic-language
A linear (1 Dimensional) boolean-algebra-based programming language.

### Functions:
|Symbol: |  Function:  |        Pass(no bits): | Outputs:      |       Examplar Syntax: |
|:---:|:---:|:---:|:---:|:---:|
|^        |  and             |  2            |  1bit               |  ```([A][B]^)``` |
|¬        |  not             |  1            |  1bit               |  ```([A]¬)``` |
|v        |  or              |  2            |  1bit               |  ```([A][B]v)``` |
|i        |  input           |  1            |  1bit               |  ```(i)``` |
|o        |  output          |  1            |  1bit to shell      |  ```([A]o)``` |
|U        |  unicode output  |  7            |  unicode character  |  ```([A]U)``` |
|x        |  exclusive or    |  2            |  1bit               |  ```([A]x[B])``` |

### Structure:
|Syntax: |  Function:                    |             Info:|
|:---:|:---:|:---:|
| [...]  |    declare a memory address             |   adds the enclosed / resulting value to the declared_values stack |
| (...)  |   declare a function                    |  used to seperate different circuits|

### Guide to structuring a function:
 1. Declare any values to be used within the function. 
    - Declared values exist only within the local scope, and are removed from the declared_values stack once you exit the scope.
    - Values declared on one level are accessible from any deeper levels, but not on any higher levels.
 2. Once all values you need have been declared, you can call a function. 
    - The number of values from the declared_values stack used depends upon the function itself. 
    - If the declared_values stack doesn't hold enough values, the program will usually crash (unless you are outputting an unicode character, in which case it will fill the deficit with 0's).
 3. The output from the function will be the only value retained from that function once it exits the
local scope.

### Simple half adder example program:
```
([A]i)([B]i)((x)o)(([A][B]^)o)
```

#### Step-by-step explanation:
```
([A]i)  <-  assign the input to index A
([B]i)  <-  assign the input to index B
((x)o)  <-  output the result of (x)
    (x)  <-  'exclusive or' gate, taking inputs from A and B
(([A][B]^)o)  <-  output the result of ([A][B]^)
    ([A][B]^)  <-  'and' gate, taking inputs from A and B
```

The reason why A and B is not assigned within the 'exclusive or' function scope is because both values are already on top of the stack. However, once the 'exclusive or' function returns a value (eg: C), A and B are no longer the topmost two values, instead C and B are. For this reason, we have to redeclare A and B within the 'and' function in order to reference them both.



Note that you can move values around in the declared_values stack instead of redeclaring them. This is
useful when you need the reference the output of a function that has since been lost in the bottom of
the stack. Using the {...} structure you can specify the current index of an item in the declared_values
stack and redeclare it, moving it to the top of the stack.