# coding=utf-8
from WhileAST import *


def testA(state):
    """
    Test A
    testee:
        Storage: WhileASTState, WhileASTVar
        Literal: WhileASTIntLit, WhileASTBoolLit
        AExp: WhileASTAExpIntLit, WhileASTAExpVar, WhileASTAExpSum, WhileASTAExpProduct
        BExp: WhileASTBExpAnd, WhileASTBExpEqual
        Comm: WhileASTCommAssign, WhileASTCommIf, WhileASTCommSeq
    Program TestA:
    var x = 3
    var y = 5
    var x = 6
    if (x == y and True):
        x = x - y
    else:
        x = y + 100; y = y * 2

    Result: x = 105, y = 10
    """
    state = WhileASTCommAssign('x', WhileASTAExpIntLit(3)).exec(state)              # var x = 3
    state = WhileASTCommAssign('y', WhileASTAExpIntLit(5)).exec(state)              # var y = 5
    state = WhileASTCommAssign('x', WhileASTAExpIntLit(6)).exec(state)              # var x = 6
    condi_1 = WhileASTBExpEqual(WhileASTAExpVar('x'), WhileASTAExpVar('y'))         # x == y
    condi_2 = WhileASTBExpBoolLit(True)                                             # True
    exp_1 = WhileASTAExpSubtract(WhileASTAExpVar('x'), WhileASTAExpVar('y'))       # x - y
    comm_1 = WhileASTCommAssign('x', exp_1)                                         # x = x - y
    exp_2 = WhileASTAExpSum(WhileASTAExpVar('y'), WhileASTAExpIntLit(100))          # y + 100
    comm_2 = WhileASTCommAssign('x', exp_2)                                         # x = y + 100
    exp_3 = WhileASTAExpProduct(WhileASTAExpVar('y'), WhileASTAExpIntLit(2))        # y * 2
    comm_3 = WhileASTCommAssign('y', exp_3)                                         # y = y * 2
    comm_seq = WhileASTCommSeq(comm_2, comm_3)                                      # x = y + 100; y = y * 2
    state = WhileASTCommIf(WhileASTBExpAnd(condi_1, condi_2), comm_1, comm_seq).exec(state)
    return state


def testB(state):
    """
    Test B
    testee:
        Storage: WhileASTState, WhileASTVar
        Literal: WhileASTIntLit
        AExp: WhileASTAExpIntLit, WhileASTAExpVar, WhileASTAExpSum
        BExp: WhileASTBExpLT, WhileASTBExpEqual, WhileASTBExpNot
        Comm: WhileASTCommWhile, WhileASTCommIf

    Program TestB:
    while (x < 5):
        x = x + 1
    if (not (x == 5)):
        x = -1
    else:
        skip
    """
    condi_1 = WhileASTBExpLT(WhileASTAExpVar('x'), WhileASTAExpIntLit(5))           # x < 5
    exp_1 = WhileASTAExpSum(WhileASTAExpVar('x'), WhileASTAExpIntLit(1))            # x + 1
    comm_1 = WhileASTCommAssign('x', exp_1)                                         # x = x + 1
    state = WhileASTCommWhile(condi_1, comm_1).exec(state)                          # while (x < 5): x = x + 1

    condi_2 = WhileASTBExpNot(WhileASTBExpEqual(WhileASTAExpVar('x'), WhileASTAExpIntLit(5)))   # not(x==5)
    comm_2 = WhileASTCommAssign('x', WhileASTAExpIntLit(-1))                        # x = -1
    state = WhileASTCommIf(condi_2, comm_2, WhileASTCommSkip()).exec(state)         # if (not(x == 5)): x = -1 else: skip
    return state


def testC(state):
    """
    Test C
    testee:
        Storage: WhileASTState, WhileASTVar
        Literal: WhileASTIntLit
        AExp: WhileASTAExpIntLit, WhileASTAExpVar, WhileASTAExpSum
        BExp: WhileASTBExpLT, WhileASTBExpEqual, WhileASTBExpNot
        Comm: WhileASTCommWhile, WhileASTCommIf

    Program TestC:
    if (x < 0):
        var pos = False
    else:
        var pos = True
    if (not(pos)):
        x = 0 - x
    else:
        skip
    """
    condi_1 = WhileASTBExpLT(WhileASTAExpVar('x'), WhileASTAExpIntLit(0))           # x < 0
    comm_1 = WhileASTCommAssign('pos', WhileASTBExpBoolLit(False))                  # var pos = False
    comm_2 = WhileASTCommAssign('pos', WhileASTBExpBoolLit(True))                   # var pos = True
    state = WhileASTCommIf(condi_1, comm_1, comm_2).exec(state)                     # if (x < 0): var pos = False
                                                                                    # else: var pos = True
    condi_2 = WhileASTBExpNot(WhileASTBExpVar('pos'))  # not(pos)
    exp_1 = WhileASTAExpSubtract(WhileASTAExpIntLit(0), WhileASTAExpVar('x'))       # 0 - x
    comm_3 = WhileASTCommAssign('x', exp_1)                                         # x = 0 - x
    state = WhileASTCommIf(condi_2, comm_3, WhileASTCommSkip()).exec(state)           # if (not(pos)): x = 0 - x
                                                                                    # else: skip
    return state


if __name__ == '__main__':
    """
    Program TestA:
    var x = 3
    var y = 5
    var x = 6
    if (x == y and True):
        x = x - y
    else:
        x = y + 100; y = y * 2

    Result: x = 105, y = 10
    """
    print('Test A:')
    testA_state = testA(WhileASTState())
    testA_state.reveal()  # var x = 105, var y = 10
    print()

    """
    Program TestB:
    while (x < 5):
        x = x + 1
    if (not (x == 5)):
        x = -1
    else:
        skip
    """
    print('Test B1:')
    state_x_0 = WhileASTState({'x': 0})
    print('before:')
    state_x_0.reveal()
    testB1_state = testB(state_x_0)
    print('after:')
    state_x_0.reveal()
    print()

    print('Test B2:')
    state_x_10 = WhileASTState({'x': 10})
    print('before:')
    state_x_0.reveal()
    testB2_state = testB(state_x_10)
    print('after:')
    testB2_state.reveal()
    print()

    """
    Program TestC (abs):
    if (x < 0):
        var pos = False
    else:
        var pos = True
    if (not(pos)):
        x = 0 - x
    else:
        skip
    """
    print('Test C1:')
    state_x_neg = WhileASTState({'x': -10})
    print('before:')
    state_x_neg.reveal()
    testC1_state = testC(state_x_neg)
    print('after:')
    testC1_state.reveal()
    print()

    print('Test C2:')
    state_x_pos = WhileASTState({'x': 100})
    print('before:')
    state_x_pos.reveal()
    testC2_state = testC(state_x_pos)
    print('after:')
    testC2_state.reveal()
    print()
