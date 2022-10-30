class InterpreterException(Exception):
    pass


class AlreadyDefined(InterpreterException):
    pass


class NotDefined(InterpreterException):
    pass


class TypeNotDefined(NotDefined):
    pass


class FunctionNotDefined(NotDefined):
    pass


class TypeAlreadyDefined(AlreadyDefined):
    pass


class FunctionAlreadyDefined(AlreadyDefined):
    pass


class RuleAlreadyDefined(AlreadyDefined):
    pass


class ExpectedParameters(InterpreterException):
    pass
