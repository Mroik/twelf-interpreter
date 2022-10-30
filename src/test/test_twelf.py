from unittest import TestCase, main

from twelf.twelf import Twelf
from twelf.exceptions import AlreadyDefined, TypeNotDefined, FunctionNotDefined


class TestInterpreter(TestCase):
    def test_reserved_keywords(self):
        interpreter = Twelf()
        self.assertRaises(AlreadyDefined, interpreter.define_type, "<-")

    def test_type_definition_correct(self):
        interpreter = Twelf()
        interpreter.define_type("ciao")
        self.assertEqual(interpreter._types, ["type", "ciao"])

    def test_type_definition_already_exists(self):
        interpreter = Twelf()
        interpreter.define_type("ciao")
        self.assertRaises(AlreadyDefined, interpreter.define_type, "ciao")

    def test_constant_definition_correct(self):
        interpreter = Twelf()
        interpreter.define_type("int")
        interpreter.define_constant("z", "int")
        self.assertEqual(interpreter._constants["z"], "int")

    def test_constant_definition_type_not_defined(self):
        interpreter = Twelf()
        self.assertRaises(TypeNotDefined, interpreter.define_constant, "z", "int")

    def test_function_definition_correct(self):
        interpreter = Twelf()
        interpreter.define_type("int")
        interpreter.define_function("sum", ["int", "int", "int", "type"])
        self.assertEqual({"sum": ["int", "int", "int", "type"]}, interpreter._function)

    def test_function_definition_type_not_defined(self):
        interpreter = Twelf()
        self.assertRaises(TypeNotDefined, interpreter.define_function, "sum", ["int", "int", "int", "type"])

    def test_rule_definition_correct(self):
        interpreter = Twelf()
        interpreter.define_type("int")
        interpreter.define_function("sum", ["int", "int", "int", "type"])
        rule = [
            ("sum", ["X", "0", "X"]),
        ]
        interpreter.define_rule("sum/0", rule)
        self.assertEqual(
            {"sum/0": [
                ("sum", ["X", "0", "X"]),
            ]},
            interpreter._rule,
        )

    def test_rule_definition_function_not_defined(self):
        interpreter = Twelf()
        interpreter.define_type("int")
        rule = [
            ("sum", ["X", "0", "X"]),
        ]
        self.assertRaises(FunctionNotDefined, interpreter.define_rule, "sum/0", rule)


if __name__ == "__main__":
    main()
