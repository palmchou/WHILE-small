WHILE-small
-----------
WHILE language small step interpreter implementation with tests.

### Description
Implementation Language: **Python3**

Previous homeworks and implementation language

1. Arith: C++
2. WHILE AST and Interpreter: Python 3
3. WHILE small step interpreter: Python 3

### Environment
Should work on any `Python3` environment.
Developed and tested on `Python 3.6 on macOS 10.12.6`.

### Tests
Program A:

    x := 3;
    if (x < 5)
        x := x + 1
    else
        x := x - 1
Result: x = 105, y = 10


Program B:

    x := 3;
    y := 5;
    x := 6;
    if (x == y && true)
        x := x - y
    else
        x := y + 100;
        y := y * 2


Program C:

    while (x < 5)
        x := x + 1;
    if (!x == 5)
        x := -1
    else
        SKIP

Program D(abs):

    if (x < 0)
        pos := false
    else
        pos := true;
    if (!pos)
        x := 0 - x
    else
        SKIP

Divergent Program E:

    while (true)
        x := x + 1

### Credits
Course [CMPS203 Programming Languages](https://classes.soe.ucsc.edu/cmps203/Spring18/), Spring 2018, UCSC
Guideline of WHILE: [An Imperative Language: WHILE](https://classes.soe.ucsc.edu/cmps203/Winter17/04-while-bigstep.pdf)

### License
MIT License, Copyright (c) \[2018\] [Shuai Zhou](http://shuaizhou.me)
