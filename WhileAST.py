# coding=utf-8
import enum
from typing import Tuple


def indent(s):
    return '\t' + str(s).replace('\n', '\n\t')


class WhileASTVar(object):
    desc = 'assignable variable'
    _val = None
    _id = None
    _type = None

    def __init__(self, var_id, var_type, val):
        self._id = var_id
        self._type = var_type
        self._val = val

    def eval(self):
        return self._val

    def assign(self, val):
        self._val = val

    def type(self):
        return self._type


class WhileASTState(object):
    desc = 'State of a program'

    def __init__(self, vars=dict()):
        self.state_dict = {}
        for var_id, value in vars.items():
            self.assign_var(var_id, value)

    def eval_var(self, var_id):
        if var_id in self.state_dict:
            return self.state_dict[var_id].eval()
        else:
            raise NameError('var %s not in this state' % var_id)

    def assign_var(self, var_id, val):
        var_type = type(val).__name__
        if var_id not in self.state_dict:
            if var_type not in ['int', 'bool']:
                raise TypeError('type of value %s is not integer nor boolean.' % str(val))
            self.state_dict[var_id] = WhileASTVar(var_id, var_type, val)
        else:
            variable = self.state_dict[var_id]
            if var_type != variable.type():
                raise TypeError('type of value %s is not compatible with %s' % var_id, variable.type())
            variable.assign(val)

    def reveal(self):
        for var_id, var in self.state_dict.items():
            print("var_id: %2s, type: %4s, value: %4s" % (var_id, var.type(), str(var.eval())))

    def __str__(self):

        return '{%s}' % (', '.join(('%s: %s' % (var_id, str(var.eval())) for var_id, var in self.state_dict.items())))


class WhileASTTypeLit(object):
    desc = 'Abstract Class for integer and boolean type'

    def value(self):
        raise NotImplementedError


class WhileASTExp(object):
    desc = 'Abstract Class for WHILE AST Expression'

    def eval(self, state):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class WhileASTAExp(WhileASTExp):
    class AExpType(enum.Enum):
        NotImplemented = 0
        IntLit = 1
        IntVar = 2
        SumExp = 3
        SubtractExp = 4
        ProductExp = 5

    desc = 'Abstract Class for WHILE AST Arith Expression'
    exp_type = AExpType.NotImplemented

    def eval(self, state):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class WhileASTAExpIntLit(WhileASTAExp):
    desc = 'Aexp for integer literal'
    exp_type = WhileASTAExp.AExpType.IntLit

    def __init__(self, n):
        self.int_value = n

    def eval(self, state):
        return self.int_value, state

    def __str__(self):
        return str(self.int_value)


class WhileASTAExpVar(WhileASTAExp):
    desc = 'Aexp for integer literal'
    exp_type = WhileASTAExp.AExpType.IntVar
    var_id = None

    def __init__(self, var_id):
        self.var_id = var_id

    def eval(self, state):
        """
        :param state: WhileASTState
        :return:
        """
        return state.eval_var(self.var_id), state

    def __str__(self):
        return self.var_id


class WhileASTAExpSum(WhileASTAExp):
    desc = 'Aexp for sum'
    exp_type = WhileASTAExp.AExpType.SumExp
    exp1 = None
    exp2 = None

    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

    def eval(self, state):
        """
        :param state: WhileASTState
        :return:
        """
        return self.exp1.eval(state)[0] + self.exp2.eval(state)[0], state

    def __str__(self):
        return '%s + %s' % (self.exp1, self.exp2)


class WhileASTAExpSubtract(WhileASTAExp):
    desc = 'Aexp for subtract'
    exp_type = WhileASTAExp.AExpType.SubtractExp
    exp1 = None
    exp2 = None

    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

    def eval(self, state):
        """
        :param state: WhileASTState
        :return:
        """
        return self.exp1.eval(state)[0] - self.exp2.eval(state)[0], state

    def __str__(self):
        return '%s - %s' % (self.exp1, self.exp2)


class WhileASTAExpProduct(WhileASTAExp):
    desc = 'Aexp for product'
    exp_type = WhileASTAExp.AExpType.ProductExp
    exp1 = None
    exp2 = None

    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

    def eval(self, state):
        """
        :param state: WhileASTState
        :return:
        """
        return self.exp1.eval(state)[0] * self.exp2.eval(state)[0], state

    def __str__(self):
        return '%s * %s' % (self.exp1, self.exp2)


class WhileASTBExp(WhileASTExp):
    class BExpType(enum.Enum):
        NotImplemented = 0
        BoolLit = 1
        Equality = 2
        LessThan = 3
        LogicNot = 4
        LogicOr = 5
        LogicAnd = 6
        BoolVar = 7

    desc = 'Abstract Class for WHILE AST Boolean Expression'
    exp_type = BExpType.NotImplemented

    def eval(self, state):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class WhileASTBExpVar(WhileASTBExp):
    desc = 'Bexp for bool variable'
    exp_type = WhileASTBExp.BExpType.BoolVar
    var_id = None

    def __init__(self, var_id):
        self.var_id = var_id

    def eval(self, state):
        """
        :param state: WhileASTState
        :return:
        """
        return state.eval_var(self.var_id), state

    def __str__(self):
        return self.var_id


class WhileASTBExpBoolLit(WhileASTBExp):
    desc = 'Bexp for boolean literal'
    exp_type = WhileASTBExp.BExpType.BoolLit

    def __init__(self, boolean):
        self.bool_value = boolean

    def eval(self, state):
        return self.bool_value, state

    def __str__(self):
        return 'true' if self.bool_value else 'false'


class WhileASTBExpEqual(WhileASTBExp):
    desc = 'Bexp for equality'
    exp_type = WhileASTBExp.BExpType.Equality
    exp1 = None
    exp2 = None

    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

    def eval(self, state):
        """
        :param state: WhileASTState
        :return:
        """
        return self.exp1.eval(state)[0] == self.exp2.eval(state)[0], state

    def __str__(self):
        return '%s == %s' % (self.exp1, self.exp2)


class WhileASTBExpLT(WhileASTBExp):
    desc = 'Bexp for less than'
    exp_type = WhileASTBExp.BExpType.LessThan
    exp1 = None
    exp2 = None

    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

    def eval(self, state):
        """
        :param state: WhileASTState
        :return:
        """
        return self.exp1.eval(state)[0] < self.exp2.eval(state)[0], state

    def __str__(self):
        return '%s < %s' % (self.exp1, self.exp2)


class WhileASTBExpNot(WhileASTBExp):
    desc = 'Bexp for logical not'
    exp_type = WhileASTBExp.BExpType.LogicNot
    exp = None

    def __init__(self, exp):
        self.exp = exp

    def eval(self, state):
        """
        :param state: WhileASTState
        :return:
        """
        return not self.exp.eval(state)[0], state

    def __str__(self):
        return '!%s' % self.exp


class WhileASTBExpOr(WhileASTBExp):
    desc = 'Bexp for logical or'
    exp_type = WhileASTBExp.BExpType.LogicOr
    exp1 = None
    exp2 = None

    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

    def eval(self, state):
        """
        :param state: WhileASTState
        :return:
        """
        return self.exp1.eval(state)[0] or self.exp2.eval(state)[0], state

    def __str__(self):
        return '%s || %s' % (self.exp1, self.exp2)


class WhileASTBExpAnd(WhileASTBExp):
    desc = 'Bexp for logical and'
    exp_type = WhileASTBExp.BExpType.LogicAnd
    exp1 = None
    exp2 = None

    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

    def eval(self, state):
        """
        :param state: WhileASTState
        :return:
        """
        return self.exp1.eval(state)[0] and self.exp2.eval(state)[0], state

    def __str__(self):
        return '%s && %s' % (self.exp1, self.exp2)


class WhileASTComm(object):
    class CommType(enum.Enum):
        NotImplemented = 0
        Skip = 1
        Assign = 2
        Sequence = 3
        IfStatement = 4
        WhileStatement = 5

    comm_type = CommType.NotImplemented

    def exec(self, state: WhileASTState) -> WhileASTState:
        raise NotImplementedError

    def exec_small(self, state: WhileASTState):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class WhileASTCommSkip(WhileASTComm):
    comm_type = WhileASTComm.CommType.Skip

    def exec(self, state):
        return state

    def exec_small(self, state: WhileASTState) -> Tuple[WhileASTComm, WhileASTState]:
        raise NotImplementedError("Should never execute skip command in small step.")

    def __str__(self):
        return 'SKIP'


class WhileASTCommAssign(WhileASTComm):
    comm_type = WhileASTComm.CommType.Assign
    var_id = None
    exp = None

    def __init__(self, var_id, exp):
        self.var_id = var_id
        self.exp = exp

    def exec(self, state):
        value = self.exp.eval(state)[0]
        state.assign_var(self.var_id, value)
        return state

    def exec_small(self, state: WhileASTState) -> Tuple[WhileASTComm, WhileASTState]:
        return WhileASTCommSkip(), self.exec(state)

    def __str__(self):
        return '%s := %s' % (self.var_id, self.exp)


class WhileASTCommSeq(WhileASTComm):
    comm_type = WhileASTComm.CommType.Sequence
    comm_A: WhileASTComm = None
    comm_B: WhileASTComm = None

    def __init__(self, comm_a: WhileASTComm, comm_b: WhileASTComm):
        self.comm_A = comm_a
        self.comm_B = comm_b

    def exec(self, state):
        state_prime = self.comm_A.exec(state)
        return self.comm_B.exec(state_prime)

    def exec_small(self, state: WhileASTState) -> Tuple[WhileASTComm, WhileASTState]:
        if not self.comm_A.comm_type == WhileASTComm.CommType.Skip:  # seq-rule 1
            comm_A_prime, state_prime =  self.comm_A.exec_small(state)
            return WhileASTCommSeq(comm_A_prime, self.comm_B), state_prime
        else:  # seq-rule 2
            return self.comm_B, state

    def __str__(self):
        return '%s;\n%s' % (self.comm_A, self.comm_B)


# if b then c1 else c2 for c1,c2 ∈ Comm and b∈Bexp
class WhileASTCommIf(WhileASTComm):
    comm_type = WhileASTComm.CommType.IfStatement
    bool_b = None
    comm_1 = None
    comm_2 = None

    def __init__(self, b, c1, c2):
        self.bool_b = b
        self.comm_1, self.comm_2 = c1, c2

    def exec(self, state):
        if self.bool_b.eval(state)[0]:
            return self.comm_1.exec(state)
        else:
            return self.comm_2.exec(state)

    def exec_small(self, state: WhileASTState) -> Tuple[WhileASTComm, WhileASTState]:
        if self.bool_b.eval(state)[0]:  # if-true rule
            return self.comm_1, state
        else:  # if-false rule
            return self.comm_2, state

    # def __str__(self):
    #     return 'if (%s) %s else %s' % (self.bool_b, self.comm_1, self.comm_2)

    def __str__(self):
        return 'if (%s)\n%s\nelse\n%s' % (self.bool_b, indent(self.comm_1), indent(self.comm_2))


# while b do c for c ∈ Comm and b ∈ Bexp
class WhileASTCommWhile(WhileASTComm):
    comm_type = WhileASTComm.CommType.WhileStatement
    bool_b = None
    body_comm = None

    def __init__(self, b: WhileASTBExp, comm: WhileASTComm):
        self.bool_b = b
        self.body_comm = comm

    def exec(self, state):
        condition = self.bool_b.eval(state)[0]
        if condition:
            next_s = self.body_comm.exec(state)
            return self.exec(next_s)
        else:
            return state

    def exec_small(self, state: WhileASTState) -> Tuple[WhileASTComm, WhileASTState]:
        condition = self.bool_b.eval(state)[0]
        if not condition:  # while-false rule
            return WhileASTCommSkip(), state
        else:  # while-true rule
            return WhileASTCommSeq(self.body_comm, self), state

    # def __str__(self):
    #     return 'while (%s) %s' % (self.bool_b, self.body_comm)

    def __str__(self):
        return 'while (%s)\n%s' % (self.bool_b, indent(self.body_comm))
