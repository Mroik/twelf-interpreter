from typing import List, Tuple, Dict
from enum import Enum, auto


RESERVED = (
    "%",
    ".",
    "<-",
    "->",
    "type",
    ":",
)


class TokenType(Enum):
    CONSTANT = auto()
    VARIABLE = auto()
    FUNCTION = auto()


class Type:
    DEFINER = "type"

    def __init__(self, name: str):
        self._name = name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        return self.name == other.name

    def __str__(self):
        return f"Type[{self._name}]"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self._name, ))

    @property
    def name(self):
        return self._name


class Constant:
    def __init__(self, name: str, ttype: Type):
        self._name = name
        self._type = ttype

    def __str__(self):
        return f"Constant[{self._name}, {self._type}]"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name == other.name

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type


class Function:
    def __init__(self, name: str, parameter_types: List[Type], return_type: Type):
        self._name = name
        if len(parameter_types) == 0:
            raise Exception
        self._parameter_types = parameter_types
        self._return_type = return_type

    def __str__(self):
        return f"{self._name}: {' -> '.join([x.name for x in self._parameter_types])} -> {self._return_type.name}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash((self._name, self.parameter_types, self._return_type))

    @property
    def name(self):
        return self._name

    @property
    def parameter_types(self):
        return tuple(self._parameter_types)

    @property
    def return_type(self):
        return self._return_type


class Parameter:
    def __init__(self, value: str | Constant | Function, parameters: List["Parameter"] = None):
        self._value = value
        if isinstance(value, str) and ord(value[0]) >= 65 and ord(value[0]) <= 90:
            self._token_type = TokenType.VARIABLE
        elif isinstance(value, Constant):
            self._token_type = TokenType.CONSTANT
        elif isinstance(value, Function):
            self._token_type = TokenType.FUNCTION
        else:
            raise Exception

        if self.token_type == TokenType.FUNCTION and parameters is None:
            raise Exception
        if self.token_type == TokenType.FUNCTION:
            self._check_parameter(value, parameters)
        self._parameters = parameters

    def __eq__(self, other):
        if self.token_type != other.token_type:
            return False
        if self.token_type == TokenType.VARIABLE or self.token_type == TokenType.CONSTANT:
            return self.value == other.value
        return self._parameters == other._parameters

    def __str__(self):
        if self._token_type == TokenType.FUNCTION:
            return f"Parameter[{self._value, self._parameters}]"
        return f"Parameter[{self._value}]"

    def __repr__(self):
        return self.__str__()

    def _check_parameter(self, func: Function, params: List["Parameter"]):
        if self._token_type != TokenType.FUNCTION:
            return
        if len(func.parameter_types) != len(params):
            raise Exception
        for x in range(len(params)):
            if params[x].token_type == TokenType.CONSTANT and params[x].value.type != func.parameter_types[x]:
                raise Exception
            if params[x].token_type == TokenType.FUNCTION and params[x].value.return_type != func.parameter_types[x]:
                raise Exception

    @property
    def value(self):
        return self._value

    @property
    def token_type(self):
        return self._token_type

    @property
    def parameters(self):
        if self._token_type != TokenType.FUNCTION:
            raise Exception
        return tuple(self._parameters)


class Rule:
    def __init__(self, name: str, functions: List[Tuple[Function, Tuple[Parameter]]]):
        self._name = name
        self._functions = functions

    def __iter__(self):
        self._func_index = 0
        return self

    def __next__(self):
        if self._func_index >= len(self._functions):
            raise StopIteration
        self._func_index += 1
        return self._functions[self._func_index]

    def __eq__(self, other):
        return self.name == other.name

    @property
    def name(self):
        return self._name

    @property
    def functions(self):
        return tuple(self._functions)


class Interpreter:
    def __init__(self):
        self._types: List[Type] = []
        self._constants: List[Constant] = []
        self._functions: List[Function] = []
        self._rules: List[Rule] = []
        self._t2c_f: Dict[Type, List[Constant | Function]] = {}
        self._f2r: Dict[Function, List[Rule]] = {}

    def _is_already_defined(func):
        def inner(self, name, *args):
            if name in [x.name for x in self._types] \
                    or name in [x.name for x in self._constants] \
                    or name in [x.name for x in self._functions] \
                    or name in [x.name for x in self._rules]:
                raise Exception
            return func(self, name, *args)
        return inner

    @_is_already_defined
    def define_type(self, name: str) -> Type:
        new_value = Type(name)
        self._types.append(new_value)
        self._t2c_f[new_value] = []
        return new_value

    @_is_already_defined
    def define_constant(self, name: str, ttype: Type) -> Constant:
        new_value = Constant(name, ttype)
        self._constants.append(new_value)
        self._t2c_f[ttype].append(new_value)
        return new_value

    @_is_already_defined
    def define_function(self, name: str, param_types: List[Type], return_type: Type) -> Function:
        new_value = Function(name, param_types, return_type)
        self._functions.append(new_value)
        if new_value.return_type != Type("type"):
            self._t2c_f[new_value.return_type].append(new_value)
        self._f2r[new_value] = []
        return new_value

    @_is_already_defined
    def define_rule(self, name: str, functions: List[Tuple[Function, Tuple[Parameter]]]) -> Rule:
        new_value = Rule(name, functions)
        self._rules.append(new_value)
        self._f2r[functions[0][0]].append(new_value)
        return new_value

    # https://www.javatpoint.com/ai-unification-in-first-order-logic#:~:text=The%20UNIFY%20algorithm%20is%20used,not%20match%20with%20each%20other.
    # I swear this was the only resource without any greek letter, made it so much easier to comprehend
    # if you want to better understand the theory behind it I'd advise you to checkout prof. Momigliano's
    # slides on unification (momigliano@di.unimi.it)
    def _unify(self, p1: Parameter, p2: Parameter):
        if p1.token_type == TokenType.VARIABLE or p1.token_type == TokenType.CONSTANT \
        or p2.token_type == TokenType.VARIABLE or p2.token_type == TokenType.CONSTANT:
            if p1 == p2:
                return []
            elif p1.token_type == TokenType.VARIABLE:
                if occurs(p2, p1):
                    return False
                else:
                    return [(p1, p2)]
            elif p2.token_type == TokenType.VARIABLE:
                if occurs(p1, p2):
                    return False
                else:
                    return [(p2, p1)]
            else:
                return False
        elif p1.value != p2.value:
            return False
        sub = []
        for x in range(len(p1.parameters)):
            temp = self._unify(p1.parameters[x], p2.parameters[x])
            if temp == False:
                return False
            if len(temp) > 0:
                sub = sub + temp
        return sub


def occurs(root: Parameter, p: Parameter):
    if root == p:
        return True
    if root.token_type != TokenType.FUNCTION:
        return False
    for x in root.parameters:
        if occurs(x, p):
            return True
    return False
