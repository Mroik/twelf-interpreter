from typing import List, Tuple, Dict
from enum import Enum, auto

from twelf.exceptions import (
    AlreadyDefined,
    TypeNotDefined,
    FunctionNotDefined,
    ExpectedParameters,
    ConstantNotDefined,
    TypeDontMatch,
)


class Parameter(Enum):
    VARIABLE = auto()
    CONSTANT = auto()


class Twelf:
    RESERVED = [
        ".",
        "->",
        "<-",
        ":",
        "%",
        "type",
    ]

    def __init__(self):
        self._types: str = []
        self._constants: Dict[str, str] = {}
        self._function: Dict[str, Tuple[List[str], str]] = {}
        self._rule: Dict[str, List[Tuple[str, List[Tuple[str, Parameter]]]]] = {}

    def _check_if_defined(func):
        def inner(self, name, *args):
            if name in self._types or name in self._function or name in self._rule or name in self.RESERVED:
                raise AlreadyDefined(f"{name} already defined")
            func(self, name, *args)
        return inner

    def _parameter_type(self, name: str) -> Parameter:
        if ord(name[0]) >= 65 and ord(name[0]) <= 90:
            return Parameter.VARIABLE
        if name in self._constants:
            return Parameter.CONSTANT
        raise ConstantNotDefined(f"Constant {name} not defined")

    @_check_if_defined
    def define_type(self, name: str):
        """define_type('int') becomes `int: type.`"""
        self._types.append(name)

    @_check_if_defined
    def define_constant(self, name: str, ttype: str):
        if ttype not in self._types:
            raise TypeNotDefined(f"{ttype} is not defined")
        self._constants[name] = ttype

    @_check_if_defined
    def define_function(self, name: str, parameters: List[str], return_type: str):
        for param in parameters:
            if param not in self._types:
                raise TypeNotDefined(f"Type {param} doesn't exist")

        if not (return_type == "type" or return_type in self._types):
            raise TypeNotDefined(f"Type {return_type} doesn't exist")
        self._function[name] = (parameters, return_type)

    # TODO typ checking for variables has to be implemented
    @_check_if_defined
    def define_rule(self, name: str, rule: List[Tuple[str, List[str]]]):
        """rule is a list of dictionaries with the name of the function
        as key and the parameters as value

        Example: define_rule('test', [('sum': ['X', 'Y', 'Z']), ('sub': ['Z', 'Y', 'X'])]) becomes

        test: sub Z Y X
            <- sum X Y Z.
        """
        parsed_rule = []
        for func in rule:
            if func[0] not in self._function:
                raise FunctionNotDefined(f"{func[0]} is not a defined function")
            if len(func[1]) != len(self._function[func[0]][0]):
                raise ExpectedParameters(f"{func[0]} expects {len(self._function[func[0]][0])} parameters")

            params = []
            for i in range(len(func[1])):
                param = func[1][i]
                if self._parameter_type(param) == Parameter.CONSTANT:
                    if self._constants[param] != self._function[func[0]][0][i]:
                        raise TypeDontMatch(f"{param} has type {self._constants[param]} where type" \
                                f" {self._function[func[0]][0][i]} is expected")

                params.append((param, self._parameter_type(param)))
            parsed_rule.append((func[0], params))

        self._rule[name] = parsed_rule
