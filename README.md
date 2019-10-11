# Keg -- (Ke)yboard (G)olfed
_Keg_ is a stack-based esolang with condensability as well as simplicity and readability in mind. It's main purpose is to be used for golfing, although it can be potentially used for other purposes. What makes this esolang different from others is that:

* Alphanumerical characters are automatically pushed (no need to wrap them in quotation marks)
* There are readable and intuitive `if` statements, `for` and `while` loops
* The number of functions to remember is small
* And much more

## A Few Conventions of This Document
* `∆ ... ∆` in a code snippet means that the code in the `...` is optional
* `>` in a code snippet means an input prompt
* `>>>` in a code snippet means a command prompt

## Design Principles
The main inspiration for _Keg_ comes from a want of an esolang where only symbols count as commands and everything else is pushed onto the stack as a literal. This is why there are only 12 functions, 7 'keywords' and 8 operators. As such, this system allows for shorter programs where strings are involved (_uncompressed_ strings in Keg are usually 1-2 bytes shorter than their counterparts in other languages).

Another design feature of _Keg_ is the look of `if` statements, `for` loops and `while` loops. These **structures** take on the form of:

    B...B

Where `B` is any of the three brackets (`(/)`, `[/]` or `{/}`) and `...` is any body of code

## The Basics
Most tutorials show how to print the string `Hello, World!` , so that's what this tutorial will do as well. Here is a simple 21 byte program to achieve the goal.

    Hello\, World\!^(!|,)

### Explanation

    Hello #Push the characters "H", "e", "l", "l" and "o" to the stack
    \, #Escape the "," and push it to the stack
    World #Push the characters "W", "o", "r", "l" and "d" to the stack
    \! #Escape the "!" and push it to the stack
    ^ #Reverse the stack
    (!| #Start a for loop and set the count to the length of the stack
        , #Print the last item on the stack as a character
    )

In the above example, 6 new functions and keywords are introduced:

`\` : Escapes the next command, and instead pushes it as a string (pushes its ascii value)
`,` : Prints the last item on the stack as a character
`!` : Pushes the length of the stack onto the stack
`^` : Reverses the stack
`(...)` : The for loop structure
`|` : Used in structures to switch from one branch to the other.

### The Stack
One of the most important parts of _Keg_ is the stack, which is where all operations are performed. A stack is a type of container (or list) where the last item in the container is the first item to be operated on (LIFO -- Last In First Out). In the following examples, the stack will be investigated.

    3# [3]
    4# [3, 4]
    +# [7]
    
In the above example, the numbers `3` and `4` are pushed onto the stack, and are then added using the `+` operator. The way it works is that the `+` pops what will be called `x` and `y` off the stack (the first and second last item) and pushes `y` + `x` back onto the stack. Note that the order of `x` and `y` are important when using the `-` and `\` operators, as `x` - `y` doesn't equal `y` - `x` most of the time (as is the same with `x` / `y` and `y` / `x`). This can be seen in the following example:

    34-.#Outputs -1
    43-.#Outputs 1
    34/.#Outputs 0.75
    43/.#Outputs 1.333333333333

_Note that the `.` function prints the last item on the stack as an integer._

### Input and Output
_Keg_ has two output functions and one input function. When taking input from the user, the next line from the Standard Input and push the ascii value of each character onto the stack. It will not push -1 anymore onto the stack to sigify the end of input (input as integers will be coming in a later version of _Keg_). Input is taken using the `?` command, as shown in the example program:

    ?(!|,)
    
    # > Example text
    # Example text

The two output functions (`.` -- Print as integer and `,` -- Print as string) have already been detailed in other sections

## Program Flow
### `If` Statements
As mentioned in the introduction, _Keg_ has a readable and intuative way of expressing `if` statements, `for` and `while` loops. The form of an `if` statement is:

    [...1 ∆| ...2∆]

When an `if` statement is run, the last item on the stack is popped, and if it is non-zero, `...1` is executed. If there is a `|...2`, it is executed if the popped value is 0.

### `For` Loops
The form of a `for` loop is:

    (∆...1|∆ ...2)

When a `for` loop is run, if `...1` is present, it will be evaluated as used as the number of times the loop will be run (if it isn't given, the length of the stack will be used). `...2` is the body of the `for` loop, which will be executed.

### `While` Loops
The form of a `while` loop is:

    { ∆...1|∆ ...2}

When a `while` loop is run,  `...1` (if given) will be the condition of the loop (if it isn't present, `1` will be used as the condition of the loop) and `...2` will be executed until the given condition is false.

## User Defined Functions
One of the special features of _Keg_ is user-defined functions, which are defined using the following form:

    @name ∆n∆ | ...@

Where:
`name` = the name of the function (note that it needs to be one full word, and that it can't contain any `@`'s)
`n` = the number of items popped from the stack
`...` = the body of the function

If `n` isn't present, no items will be popped from the stack, and all code in the function will be applied to the main stack

## Special Bits

* If nothing is printed during the run of the program, the whole stack will be joined together (stringified, with values less than 10 or greater than 256 being treated as integers) and printed

* Closing brackets can be left out of programs, and will be auto-completed in a LIFO matter

* There is also implicit input. If you use `^` and `:` on an empty stack, one line of input will be taken.

* The next edit of the interpreter does not have -1's being pushed to the input.

## Example Programs

### Hello World, Further Golfed

    Hello\, World\!

### Cat Program

    ^
    
### Fizzbuzz Program

    0(d|1+:35*%0=[ zzubzziF(9|,)|:5%0=[ zzuB(5|,)|:3%0=[ zziF(5|,)|:. ,]]])
   
### 99 Bottles of Beer Program

    c&(c|&:.& bottles of beer on the wall\, ^(!|,)&:.& bottles of beer\.91+^(!|,)Take one down\, pass it around\, ^(!|,)&1-&&:.& bottles of beer on the wall\.91+^(!|,))
    
### Quine

    Q

_This can be any series of alphabetical letters_

## Command Glossary
If the `^` or `:` commands tried to operate on an empty stack, an input will be taken (for shorter programs).

|Command|Description|Usage|Notes|
|------------|-------------|-------|-------|
| `!` |  Pushes the length of the stack onto the stack |  `!` | |
| `:` | Duplicates the last item on the stack | `:` | |
| `_` | Removes the last item on the stack | `_` | |
| `,` | Prints the last item on the stack as a character | `,` | |
| `.` | Prints the last item on the stack as an integer | `.` | |
| `?` | Gets input from the user | `?` | |
| `'` | Left shifts the stack | `'` | |
| `"` | Right shifts the stack | `"` | |
| `~` | Pushes a random number onto the stack | `~` | The number will be between 0 and 32767 |
| `^` | Reverses the stack | `^` | |
| `$` | Swaps the top two items on the stack | `$` | |
| `#` | Starts a comment | `#` | |
| `\|` | Branches to the next section of a structure | `B...\|...B`| `B` is any one bracket type |
| `\` | Escapes the next command, and pushes it as a string | `\<command>` | |
| `&` | Gets/sets the register value | `&` | |
| `@` | Define/call a function | `@ name ∆n∆ \| ...@` | |
| `+` | Pops `x` and `y` and pushes `y` + `x` | `<value><value>+` | |
| `-` | Pops `x` and `y` and pushes `y` - `x` | `<value><value>-` | |
| `*` | Pops `x` and `y` and pushes `y` * `x` | `<value><value>*` | |
| `/` | Pops `x` and `y` and pushes `y` / `x` | `<value><value>/` | Divison by zero gives an error |
| `%` | Pops `x` and `y` and pushes `y` % `x` | `<value><value>%` | Divison by zero gives an error |
| `<` | Pops `x` and `y` and pushes `y` < `x` | `<value><value><` | |
| `>` | Pops `x` and `y` and pushes `y` > `x` | `<value><value>>` | |
| `=` | Pops `x` and `y` and pushes `y` == `x` | `<value><value>=` | |
| `0-9` | Pushes the given integer onto the stack | `<value>` | |
| `a-z, A-Z` | Pushes the ascii value of the given character onto the stack | `<value>` | |

## Extended command glossary
These commands are added to Keg in order to make Keg programs shorter. These instructions can be implemented in Keg quite easily. These are NOT part of the official Keg. (From A__)

|Command|Description|Usage|Notes&Implementation|
|-------|-----------|-----|--------------------|
|`Ï`| Replaces the top of stack with all items from `top to 0`|`Ï`| this is under EASCII, of course;<br/>```(:\|:1-)```|
|`;`| Decrement the top of the stack | `;` | `1-` |
|`Ë`| Exponentation |`Ë`| `# Unknown`|
|`§`| Sine function |`§`| `# Unknown` |
|`¿`| Nice input | `¿`| Tries to eval as Float > Integer > List > String|
|`∂`| Exclusive range | `∂` | Pops `x`, `y` and `z` and pushes `z in range(y, x)`|
|`•`| Inclusive range | `•` | Pops `x`, `y` and `z` and pushes `z in range(y, x + 1)`|
|`ɧ`| Generate range | `ɧ` | Pops `x` and `y` and pushes `range(y, x + 1)`|
|`÷`| Item split | `÷`| Splits the top of stack into seperate parts|
|`¡`| Factorial| `¡` | Takes the factorial of the top of the stack|
|`ø`| Empties the stack |`ø`|None|
|`Ω`|Prints the entire stack|`Ω`|None|
|`∑`|Apply to all the stack|`∑`|Preprocesses to `(!;|`|
|`¬`|Logically nots the top of the stack|`¬`|None|
|`½`|Halves the top of the stack|`½`|None|

## Keg+ Extension

| Command | Description                                                                                               | Usage       | Notes                                                          | Implemented? |
|---------|-----------------------------------------------------------------------------------------------------------|-------------|----------------------------------------------------------------|--------------|
| `‡`     | Reads the source code until a non-number character is found                                               | `‡<number>` | Non-number character means that it isn't a valid float/integer | No           |
| `ℤℝ⅍℠ⁿ` | Converts the top of the stack to the desired type (integer, float, stack, string, character respectively) | `<type>`    |                                                                | Yes          |
| `⟰⟱⟷`   | Takes the top of the stack and uppercases it, lowercases it or togglecases it respectively                | `<mode>`    | Doesn't do anything to non-strings                             | Yes          |
| `²`     | Squares the top of the stack                                                                              | `²`         | Performs `top * top`                                           | Yes          |
| `᠀`     | Take input as a string                                                                                    | `᠀`         |                                                                | Yes          |
| `∀`     | Pushes 1 if everything on the stack is true, otherwise 0                                                  | `∀`         | Doesn't pop things from the stack                              | Yes          |
| `≌`     | Like above, but if everything is the same                                                                 | `≌`         |                                                                | Yes          |
| `⅀`     | Summates the entire stack                                                                                 | `⅀`         | Pretty much just `∑+)`                                         | Yes          |
| `ß`     | Takes the top of the stack and executes it as Keg code                                                    | `ß`         |                                                                | Kind of      |
| `©`     | Get the value of a variable                                                                               | `©name`     | `name` has to only contain letters                             | Yes          |
| `®`     | Set the value of a variable to the top of the stack (popping it)                                          | `®name`     | Same as above                                                  | Yes          |
