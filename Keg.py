# Keg to Python Reference
It's official. Keg is now a transpiled language, as interpreting it was just too hard. Here is a guide of how everything now works

```mermaid
graph TB
First[Preprocessor] --> Second
Second[Uncompressor] --> Third
Third[Parser] --> Fourth
Fourth[Translator] --> Fifth
Fifth[Execution] --> Output
```

## Command Glossary
### Alphanumeric characters
Characters in the range of `a-z` and `A-Z` will be pushed as so:

```python
letter()
``` 

As such, the program `ABC` would be transpiled as:

```python
A(); B(); C()
```

And `Hello World` would become:

```python
H(); e(); l(); l(); o(); space(); W(); o(); r(); l(); d()
```

This allows for letters to be redefined as macros if that makes sense. (More on that later)

Numbers in the range of `0-9` would follow as such:

	0: zero()
	1: one()
	2: two()
	3: three()
	4: four()
	5: five()
	6: six()
	7: seven()
	8: eight()
	9: nine()

Thenceforth, `89` would become:

```python
eight(); nine()
```
### Mathematical operators

Quite simple really:

	+: add(stack.pop(), stack.pop())
	-: minus(stack.pop(), stack.pop())
	*: times(stack.pop(), stack.pop())
	/: divide(stack.pop(), stack.pop())
	%: modulo(stack.pop(), stack.pop())

### Conditional Operators
I'mma start using a new way of writing these. All functions assume the parameters `stack.pop(), stack.pop()`

	=: eq()
	≠: nq()
	>: gt()
	<: lt()
	≥: ge()
	≤: le()
	≬: g0()

### Built-in FNS
These functions _don't_ assume any parameters

	!: length()
	$: swap()
	^: reverse()
	:: duplicate()
	": r_shift()
	': l_shift()
	,: nice()
	.: raw()
	?: _input()
	~: random()
	_: stack.pop()

### If Statements
Unlike all prior sections, this section shan't be so brief. Why? Because the humble `[...|...]` isn't just a function you see.

The general form will become:

```python
if bool(stack.pop):
	...
else:
	...
```

But what if there is only one section? (i.e. `[...]`)

```python
if bool(stack.pop()):
	...
```

But what if there is an empty `ifTrue` section but a filled `ifFalse` section? (i.e. `[|...]`)

```python
if bool(stack.pop()):
	pass
else:
	...
```
Although maybe this is more appropriate:
```python
if not bool(stack.pop()):
	...
```

I mean, really, the only person bothering with this is those making transpilers.

### For Loops
These are a bit harder, as, well, Keg loops are a little different.
Given the normal counted loop (no vars, integer as condition):

```python
for _ in _loop_eval(stack.pop())
	...
```
It is important to note that `_loop_eval()` is defined as such:

```python
def _loop_eval(expr):
	if type(expr) in [int, chr]:
		return range(expr)
	else:
		return expr
```

But what if there are three parts? (i.e. `(count|var|code)`)

```python
for var in _loop_eval(count):
	code
```

But what if there isn't a loop condition?

```python
length()
for _ in _loop_eval(stack.pop()):
	...
```
### While loops
While loops are pretty similar to for loops, but easier in a way:

```python
while bool(stack.pop()):
	...
```

But what if it is a post-test loop? (i.e. `{...|P|...}`)

```python
condition = True
while condition:
	...
	condition = bool(stack.pop())

```

### Functions
The function `@name n|...ƒ` turns into:

```python
def name(stack):
	temp = Stack()
	for _ in range(n): temp.push(stack.pop())
	...
	for item in temp:
		stack.push(item)
```

The function `@name *|...ƒ` gets turned into:

```python
def name(stack):
	...
```

The function `@name _|...ƒ` gets turned into:

```python
def name(stack):
	field = stack.pop()
	if type(field) in [int, float]:
		n = int(field)
	elif type(field) is str and len(field) == 1:
		n = _chr(field)
	else:
		n = len(field)
	
	temp = Stack()
	for _ in range(n):
		temp.push(stack.pop())
	
	...
	for item in temp:
		stack.push(item)
```

### Escaping Characters

Escaping characters is an interesting problem:

```python
stack.push("character")
```
or perhaps

```python
escape(CHARACTER)
```

### Comments
Comments aren't included in the transpiled program

### The Register
Hmm. The register. Toggled with `&`, it will be turned into:

```python
register()
```

## The Reg Extension

### Iota
```python
iota(stack)
```

### Sine
```python
sine(stack)
```

### Decrement
```python
decrement(stack)
```

### Nice Input
```python
stack.push(_eval(_input()))
```

### Apply to All
**preprocesses as usual**

### Exclusive Range
Pop `a`, `b` and `c` and generate a range from `a` to `b - 1` and return if `c` is in that range.

```python
def excl_range(stack):
	query = stack.pop()
	values = [stack.pop(), stack.pop()]
	start, stop = sorted(values)
	range_object = range(start, stop)
	if query in range_object:
		stack.push(1)
	else:
		stack.push(0)
```

### Inclusive Range
Pop `a`, `b` and `c` and generate a range from `a` to `b` and return if `c` is in that range.

```python
def incl_range(stack):
	query = stack.pop()
	values = [stack.pop(), stack.pop()]
	start, stop = sorted(values)
	range_object = range(start, stop + 1)
	if query in range_object:
		stack.push(1)
	else:
		stack.push(0)
```

### Generate Range
Pop `a` and `b` and generate a smart, inclusive range:

```python
def smart_range(stack):
	values = [stack.pop(), stack.pop()]
	start, stop = sorted(values)
	range_object = range(start, stop + 1)
	for item in range_object:
		stack.push(item)
```
### Item Split
This is an interesting one, as it requires type checking: nonetheless, here is what it probably transpile to:

```python
def item_split(stack):
	item = stack.pop()
	_type = type(item)
	if _type is int:
		for number in str(item):
			stack.push(int(item))
	elif _type is str and len(item) == 1:
		for number in str(_ord(item)):
			stack.push(int(item))
	else:
		for value in item:
			stack.push(value)
```
### Factorial

```python
def factorial(stack):
	number = stack.pop()
	import math
	try:
		result = math.factorial(number)
	except Exception as e:
		result = "" #A whole lot of who knows what?
	stack.push(result)
```
		

> Written with [StackEdit](https://stackedit.io/).
