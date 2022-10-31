from unittest import TestCase, main

from twelf.interpreter import Interpreter, Parameter
from twelf.exceptions import AlreadyDefined, TypeNotDefined, FunctionNotDefined, ConstantNotDefined, TypeDontMatch


class TestTypeDefinition(TestCase):
    def test_reserved_keywords(self):
        interpreter = Interpreter()
        self.assertRaises(AlreadyDefined, interpreter.define_type, "<-")

    def test_type_definition_correct(self):
        interpreter = Interpreter()
        interpreter.define_type("ciao")
        self.assertEqual(interpreter._types, ["ciao"])

    def test_type_definition_already_exists(self):
        interpreter = Interpreter()
        interpreter.define_type("ciao")
        self.assertRaises(AlreadyDefined, interpreter.define_type, "ciao")


class TestConstantDefinition(TestCase):
    def test_constant_definition_correct(self):
        interpreter = Interpreter()
        interpreter.define_type("int")
        interpreter.define_constant("z", "int")
        self.assertEqual(interpreter._constants["z"], "int")

    def test_constant_definition_type_not_defined(self):
        interpreter = Interpreter()
        self.assertRaises(TypeNotDefined, interpreter.define_constant, "z", "int")


class TestFunctionDefinition(TestCase):
    def test_parameter_is_constant(self):
        interpreter = Interpreter()
        interpreter.define_type("int")
        interpreter.define_constant("z", "int")
        self.assertEqual(interpreter._parameter_type("z"), Parameter.CONSTANT)

    def test_parameter_is_variable(self):
        interpreter = Interpreter()
        self.assertEqual(interpreter._parameter_type("X"), Parameter.VARIABLE)

    def test_parameter_is_undefined_constant(self):
        interpreter = Interpreter()
        self.assertRaises(ConstantNotDefined, interpreter._parameter_type, "z")

    def test_function_definition_correct(self):
        interpreter = Interpreter()
        interpreter.define_type("int")
        interpreter.define_function("sum", ["int", "int", "int"], "type")
        self.assertEqual({"sum": (["int", "int", "int"], "type")}, interpreter._function)

    def test_function_definition_with_return_type_user_defined(self):
        interpreter = Interpreter()
        interpreter.define_type("int")
        interpreter.define_function("s", ["int"], "int")
        self.assertEqual({"s": (["int"], "int")}, interpreter._function)

    def test_function_definition_type_not_defined(self):
        interpreter = Interpreter()
        self.assertRaises(TypeNotDefined, interpreter.define_function, "sum", ["int", "int", "int"], "type")


class TestRuleDefinition(TestCase):
    def test_rule_definition_correct(self):
        interpreter = Interpreter()
        interpreter.define_type("int")
        interpreter.define_constant("0", "int")
        interpreter.define_function("sum", ["int", "int", "int"], "type")
        rule = [
            ("sum", ["X", "0", "X"]),
        ]
        interpreter.define_rule("sum/0", rule)
        self.assertEqual(
            {"sum/0": [
                ("sum", [("X", Parameter.VARIABLE), ("0", Parameter.CONSTANT), ("X", Parameter.VARIABLE)]),
            ]},
            interpreter._rule,
        )

    def test_rule_definition_wrong_parameter_type(self):
        interpreter = Interpreter()
        interpreter.define_type("int")
        interpreter.define_type("float")
        interpreter.define_constant("0", "int")
        interpreter.define_constant("0,0", "float")
        interpreter.define_function("sum", ["int", "int", "int"], "type")
        rule = [
            ("sum", ["X", "0,0", "X"]),
        ]
        self.assertRaises(TypeDontMatch, interpreter.define_rule, "sum/0", rule)

    def test_rule_definition_function_not_defined(self):
        interpreter = Interpreter()
        interpreter.define_type("int")
        rule = [
            ("sum", ["X", "0", "X"]),
        ]
        self.assertRaises(FunctionNotDefined, interpreter.define_rule, "sum/0", rule)


if __name__ == "__main__":
    main()
