from typing import List, Tuple
from enum import Enum, auto


class TokenType(Enum):
    CONSTANT = auto()
    VARIABLE = auto()
    FUNCTION = auto()


class Type:
    DEFINER = "type"

    def __init__(self, name: str):
        self._name = name

    def __eq__(self, other):
        return self.name == other.name

    @property
    def name(self):
        return self._name


class Constant:
    def __init__(self, name: str, ttype: Type):
        self._name = name
        self._type = ttype

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type


class Function:
    def __init__(self, name: str, parameter_types: List[Type], return_type: Type):
        self._name = name
        self._parameter_types = parameter_types
        self._return_type = return_type

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

    @property
    def name(self):
        return self._name

    @property
    def functions(self):
        return tuple(self._functions)


class Interpreter:
    pass
