# coding=utf-8
from WhileAST import *
from collections import deque
STEPS_AS_DIVERGENCE = 100


def small_program_A():
    """
    x := 3; if(x<5) x = x+1 else x = x-1
    """
    comm_1 = WhileASTCommAssign('x', WhileASTAExpIntLit(3))                                             # x := 3
    condi_1 = WhileASTBExpLT(WhileASTAExpVar('x'), WhileASTAExpIntLit(5))                               # x < 5
    comm_2 = WhileASTCommAssign('x', WhileASTAExpSum(WhileASTAExpVar('x'), WhileASTAExpIntLit(1)))      # x := x + 1
    comm_3 = WhileASTCommAssign('x', WhileASTAExpSubtract(WhileASTAExpVar('x'), WhileASTAExpIntLit(1))) # x := x - 1
    # if (x < 5): x := x + 1 else x := x - 1
    comm_4 = WhileASTCommIf(condi_1, comm_2, comm_3)
    # x := 3; if(x<5) x = x+1 else x = x-1
    program = WhileASTCommSeq(comm_1, comm_4)

    return program


def small_program_B():
    """
    1 var x = 3
    2 var y = 5
    3 var x = 6
    4 if (x == y and True):
    5     x = x - y
    6 else:
    7     x = y + 100; y = y * 2
    """
    commands = deque()
    commands.append(WhileASTCommAssign('x', WhileASTAExpIntLit(3)))                             # var x = 3
    commands.append(WhileASTCommAssign('y', WhileASTAExpIntLit(5)))                             # var y = 5
    commands.append(WhileASTCommAssign('x', WhileASTAExpIntLit(6)))                             # var x = 6

    condi_1 = WhileASTBExpEqual(WhileASTAExpVar('x'), WhileASTAExpVar('y'))                     # x == y
    condi_2 = WhileASTBExpBoolLit(True)                                                         # True
    exp_1 = WhileASTAExpSubtract(WhileASTAExpVar('x'), WhileASTAExpVar('y'))                    # x - y
    comm_1 = WhileASTCommAssign('x', exp_1)                                                     # x = x - y
    exp_2 = WhileASTAExpSum(WhileASTAExpVar('y'), WhileASTAExpIntLit(100))                      # y + 100
    comm_2 = WhileASTCommAssign('x', exp_2)                                                     # x = y + 100
    exp_3 = WhileASTAExpProduct(WhileASTAExpVar('y'), WhileASTAExpIntLit(2))                    # y * 2
    comm_3 = WhileASTCommAssign('y', exp_3)                                                     # y = y * 2
    comm_seq = WhileASTCommSeq(comm_2, comm_3)                                                  # x = y + 100; y = y * 2
    commands.append(WhileASTCommIf(WhileASTBExpAnd(condi_1, condi_2), comm_1, comm_seq))

    program = commands.popleft()
    while commands:
        program = WhileASTCommSeq(program, commands.popleft())
    return program


def small_program_C():
    """
    while (x < 5):
        x = x + 1
    if (not (x == 5)):
        x = -1
    else:
        skip
    """
    condi_1 = WhileASTBExpLT(WhileASTAExpVar('x'), WhileASTAExpIntLit(5))                       # x < 5
    exp_1 = WhileASTAExpSum(WhileASTAExpVar('x'), WhileASTAExpIntLit(1))                        # x + 1
    comm_1 = WhileASTCommAssign('x', exp_1)                                                     # x = x + 1
    comm_w = WhileASTCommWhile(condi_1, comm_1)                                                 # while (x < 5): x = x + 1

    condi_2 = WhileASTBExpNot(WhileASTBExpEqual(WhileASTAExpVar('x'), WhileASTAExpIntLit(5)))   # not(x==5)
    comm_2 = WhileASTCommAssign('x', WhileASTAExpIntLit(-1))                                    # x = -1

    # if (not(x == 5)): x = -1 else: skip
    comm_if = WhileASTCommIf(condi_2, comm_2, WhileASTCommSkip())
    return WhileASTCommSeq(comm_w, comm_if)


def small_program_D():
    """
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
    if_1 = WhileASTCommIf(condi_1, comm_1, comm_2)                                  # if (x < 0): var pos = False
                                                                                    # else: var pos = True
    condi_2 = WhileASTBExpNot(WhileASTBExpVar('pos'))  # not(pos)
    exp_1 = WhileASTAExpSubtract(WhileASTAExpIntLit(0), WhileASTAExpVar('x'))       # 0 - x
    comm_3 = WhileASTCommAssign('x', exp_1)                                         # x = 0 - x
    if_2 = WhileASTCommIf(condi_2, comm_3, WhileASTCommSkip())                      # if (not(pos)): x = 0 - x
                                                                                    # else: skip
    return WhileASTCommSeq(if_1, if_2)


def small_program_E():
    """
    while (true)
        x = x + 1
    """
    assign = WhileASTCommAssign('x', WhileASTAExpSum(WhileASTAExpVar('x'), WhileASTAExpIntLit(1)))      # x = x + 1
    return WhileASTCommWhile(WhileASTBExpBoolLit(True), assign)


def run_small(program: WhileASTComm, state: WhileASTState):
    step = 0
    comm = program
    while True:
        if step > STEPS_AS_DIVERGENCE:
            print("Stop running after %d steps." % STEPS_AS_DIVERGENCE)
            print("Program seems like diverging.")
            break
        print("Step %d:" % step)
        print(comm)
        print("State:", state)
        if not comm.comm_type == WhileASTComm.CommType.Skip:  # not the terminating skip command
            comm, state = comm.exec_small(state)
        else:  # the terminating skip command
            print("Program terminated.")
            break
        step += 1
        print()


if __name__ == '__main__':
    STEPS_AS_DIVERGENCE = 100

    print('---- SMALL Program_A ----')
    run_small(small_program_A(), WhileASTState({}))
    print('-------------------------\n')

    print('---- SMALL Program_B ----')
    run_small(small_program_B(), WhileASTState({}))
    print('-------------------------\n')

    print('---- SMALL Program_C 1 ----')
    run_small(small_program_C(), WhileASTState({'x': 0}))
    print('-------------------------\n')

    print('---- SMALL Program_C 2 ----')
    run_small(small_program_C(), WhileASTState({'x': 10}))
    print('-------------------------\n')

    print('---- SMALL Program_D 1 ----')
    run_small(small_program_D(), WhileASTState({'x': 10}))
    print('-------------------------\n')

    print('---- SMALL Program_D 2 ----')
    run_small(small_program_D(), WhileASTState({'x': -10}))
    print('-------------------------\n')

    # comment out below to run the divergent program (will stop at STEPS_AS_DIVERGENCE steps)
    # print('---- SMALL Program_E ----')
    # run_small(small_program_E(), WhileASTState({'x': 0}))
    # print('-------------------------\n')
