import unittest

from solution import strict

class TestStrict(unittest.TestCase):
    def test_basic_int_function(self):
        @strict
        def sum_two(a: int, b: int) -> int:
            return a + b
            
        self.assertEqual(sum_two(1, 2), 3)
        self.assertRaises(TypeError, sum_two, 1, 2.4)
        self.assertRaises(TypeError, sum_two, "1", 2)
        self.assertRaises(TypeError, sum_two, 1, "2")

    def test_float_function(self):
        @strict
        def divide(a: float, b: float) -> float:
            return a / b
            
        self.assertEqual(divide(6.0, 2.0), 3.0)
        self.assertRaises(TypeError, divide, 6, 2.0)
        self.assertRaises(TypeError, divide, 6.0, 2)
        self.assertRaises(TypeError, divide, "6.0", 2.0)

    def test_string_function(self):
        @strict
        def concatenate(a: str, b: str) -> str:
            return a + b
            
        self.assertEqual(concatenate("hello", "world"), "helloworld")
        self.assertRaises(TypeError, concatenate, "hello", 123)
        self.assertRaises(TypeError, concatenate, 123, "world")
        self.assertRaises(TypeError, concatenate, True, "world")

    def test_bool_function(self):
        @strict
        def logical_and(a: bool, b: bool) -> bool:
            return a and b
            
        self.assertEqual(logical_and(True, True), True)
        self.assertEqual(logical_and(True, False), False)
        self.assertRaises(TypeError, logical_and, 1, True)
        self.assertRaises(TypeError, logical_and, True, 1)
        self.assertRaises(TypeError, logical_and, "True", True)

    def test_mixed_types_function(self):
        @strict
        def process_data(name: str, age: int, is_active: bool, score: float) -> str:
            return f"{name} ({age}) - {is_active} - {score}"
            
        self.assertEqual(process_data("John", 25, True, 95.5), "John (25) - True - 95.5")
        self.assertRaises(TypeError, process_data, 123, 25, True, 95.5)
        self.assertRaises(TypeError, process_data, "John", "25", True, 95.5)
        self.assertRaises(TypeError, process_data, "John", 25, 1, 95.5)
        self.assertRaises(TypeError, process_data, "John", 25, True, "95.5")

    def test_keyword_arguments(self):
        @strict
        def calculate(a: int, b: int, c: int) -> int:
            return a + b + c
            
        self.assertEqual(calculate(1, 2, 3), 6)
        self.assertEqual(calculate(a=1, b=2, c=3), 6)
        self.assertEqual(calculate(1, b=2, c=3), 6)
        self.assertRaises(TypeError, calculate, a=1, b=2.0, c=3)
        self.assertRaises(TypeError, calculate, 1, b="2", c=3)

    def test_empty_function(self):
        @strict
        def empty_func() -> None:
            pass
            
        self.assertIsNone(empty_func())

if __name__ == '__main__':
    unittest.main()