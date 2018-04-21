WHILE-Lang
---
WHILE language AST implementation and AST interpreter with tests.

### Description
Implementation Language: **Python3** (ARITH, **C++**)
New Feature: Bool Variable, See TestC()

### Environment
Should work on any `Python3` environment.
Developed and tested on `Python 3.6 on macOS 10.12.6`.

### Tests
Program TestA:

    var x = 3
    var y = 5
    var x = 6
    if (x == y and True):
        x = x - y
    else:
        x = y + 100; y = y * 2
Result: x = 105, y = 10


Program TestB:

    while (x < 5):
        x = x + 1
    if (not (x == 5)):
        x = -1
    else:
        skip


Program TestC:

    if (x < 0):
        var pos = False
    else:
        var pos = True
    if (not(pos)):
        x = 0 - x
    else:
        skip

### Credits
Course [CMPS203 Programming Languages](https://classes.soe.ucsc.edu/cmps203/Spring18/), Spring 2018, UCSC
Guideline of WHILE: [An Imperative Language: WHILE](https://classes.soe.ucsc.edu/cmps203/Winter17/04-while-bigstep.pdf)

### License
MIT License
