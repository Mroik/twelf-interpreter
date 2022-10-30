from typing import List, Tuple

from twelf.exceptions import AlreadyDefined, TypeNotDefined, FunctionNotDefined, ExpectedParameters


class Twelf:
    def __init__(self):
        self._types = ["type"]
        self._function = {}
        self._rule = {}

    def _check_if_defined(func):
        def inner(self, name, *args):
            if name in self._types or name in self._function or name in self._rule:
                raise AlreadyDefined(f"{name} already defined")
            func(self, name, *args)
        return inner

    @_check_if_defined
    def define_type(self, name: str):
        """define_type('int') becomes `int: type.`"""
        self._types.append(name)

    @_check_if_defined
    def define_function(self, name: str, parameters: List[str]):
        for param in parameters:
            if param not in self._types:
                raise TypeNotDefined(f"Type {param} doesn't exist")
        self._function[name] = parameters

    @_check_if_defined
    def define_rule(self, name: str, rule: List[Tuple[str, List[str | None]]]):
        """rule is a list of dictionaries with the name of the function
        as key and the parameters as value

        Example: define_rule('test', [('sum': ['X', 'Y', 'Z']), ('sub': ['Z', 'Y', 'Z'])]) becomes

        test: sub Z Y X
            <- sum X Y Z.
        """
        for func in rule:
            if func[0] not in self._function:
                raise FunctionNotDefined(f"{func[0]} is not a defined function")
            n_params = len(self._function[func[0]])
            if self._function[func[0]][-1] == "type":
                n_params -= 1
            if len(func[1]) != n_params:
                raise ExpectedParameters(f"{func[0]} expects {len(self._function[func[0]])} parameters")
        self._rule[name] = rule
