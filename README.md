# Nugly
Nugly is a concatenative stack-based programming language that generates x86_64 Assembly.
Reverse Polish Notation is used extensively.

**WARNING: This language is only intended to be run on Linux operating systems.**

Linux x86_64 Assembly libraries.
```
grab asm<io>
grab asm<linux64>
grab asm<generics>
```

Stack expressions to organise and re-use.
```
stackexpr <identifier>
	<expression>
end
```
```
stackexpr push_num 
	10 8 +
end
```

Stack expressions can be called. This performs the set of instructions defined in the specified stack expression.
```
call push_num
```

An entry point needs to be defined to indicate the start of the main program.
```
entry
	<program body>
end
```

Example program that pushes two items to the stack, adds them and prints them.
```
grab asm<io>
grab asm<linux64>
grab asm<generics>

stackexpr math
	3 4 +
end

entry
	call math
	call putI64
end
```

Conditionals.
```
<expression> if
	<body>
end
```
The following program pushes two numbers to the stack and checks whether they are equal, if so it prints "they are equal".
```
stackexpr push_num
	2 2
end

entry
	call push_num
	== if
		putS invoke " they are equal"
	end
end
```

