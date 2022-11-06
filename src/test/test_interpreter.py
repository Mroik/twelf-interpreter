from unittest import TestCase
from random import randint

from twelf.interpreter import Type, Constant, Function, Parameter, TokenType, Rule, Interpreter


class TestType(TestCase):
    def test_type_definition(self):
        name = f"{randint(0, 100) for x in range(10)}"
        to_test = Type(name)
        self.assertEqual(name, to_test.name)

    def test_type_equality(self):
        name = f"{randint(0, 100) for x in range(10)}"
        to_test = Type(name)
        oracle = Type(name)
        self.assertEqual(to_test, oracle)


class TestConstant(TestCase):
    def test_constant_definition(self):
        typea = Type("int")
        zero = Constant("0", typea)
        self.assertEqual(zero.name, "0")
        self.assertEqual(typea, zero.type)


class TestFunction(TestCase):
    def test_function_definition(self):
        int_type = Type("int")
        func = Function("sum", [int_type, int_type, int_type], Type(Type.DEFINER))
        self.assertEqual("sum", func.name)
        self.assertEqual((int_type, int_type, int_type), func.parameter_types)
        self.assertEqual(Type(Type.DEFINER), func.return_type)


class TestParameter(TestCase):
    def test_variable_parameter(self):
        param = Parameter("Ciao")
        self.assertEqual(param.token_type, TokenType.VARIABLE)

    def test_invalid_variable_parameter(self):
        self.assertRaises(Exception, Parameter, "ciao")

    def test_constant_parameter(self):
        ttype = Type("int")
        const = Constant("0", ttype)
        param = Parameter(const)
        self.assertEqual(param.token_type, TokenType.CONSTANT)

    def test_function_parameter(self):
        ttype = Type("int")
        func = Function("sum", [ttype, ttype, ttype], Type(Type.DEFINER))
        param = Parameter(func, [
            Parameter("X"),
            Parameter("Y"),
            Parameter("Z"),
        ])
        self.assertEqual(param.token_type, TokenType.FUNCTION)

    def test_invalid_function_parameter(self):
        int_type = Type("int")
        float_type = Type("float")
        zero = Constant("0,0", float_type)
        func = Function("sum", [int_type, int_type, int_type], Type(Type.DEFINER))
        self.assertRaises(Exception, Parameter, func, [
            Parameter("X"),
            Parameter("Y"),
            Parameter(zero),
        ])


class TestRule(TestCase):
    def test_rule_definition(self):
        int_type = Type("int")
        func = Function("sum", [int_type, int_type, int_type], Type(Type.DEFINER))
        rule = Rule("aa", [(func, tuple([
            Parameter("X"),
            Parameter("Y"),
            Parameter("Z"),
        ]))])
        self.assertEqual(rule.name, "aa")
        oracle = ((func, (
            Parameter("X"),
            Parameter("Y"),
            Parameter("Z"),
        )), )
        self.assertEqual(rule.functions, oracle)


class TestInterpreter(TestCase):
    def test_type_definition(self):
        inter = Interpreter()
        inter.define_type("int")
        self.assertEqual(inter._types, [Type("int")])

    def test_constant_definition(self):
        inter = Interpreter()
        integer = inter.define_type("int")
        inter.define_constant("1", integer)
        self.assertEqual(inter._constants, [Constant("1", integer)])

    def test_function_definition(self):
        inter = Interpreter()
        integer = inter.define_type("int")
        inter.define_function("sum", [integer, integer, integer], Type(Type.DEFINER))
        self.assertEqual(inter._functions, [Function("sum", [integer, integer, integer], Type(Type.DEFINER))])

    def test_rule_definition(self):
        inter = Interpreter()
        integer = inter.define_type("int")
        func = inter.define_function("sum", [integer, integer, integer], Type(Type.DEFINER))
        inter.define_rule("ss", [(func, (
            Parameter("X"),
            Parameter("Y"),
            Parameter("Z"),
        ))])
        self.assertEqual(inter._rules, [Rule("ss", [(func, (
            Parameter("X"),
            Parameter("Y"),
            Parameter("Z"),
        ))])])
