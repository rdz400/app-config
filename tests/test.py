import unittest
from unittest import TestCase
from config_manager.main import (
    replace_env_ref_with_abs,
    validate_config_name,
    InvalidNameError
)


class MainTest(TestCase):

    def setUp(self) -> None:
        import os
        os.environ['ABC'] = 'Ronald'

    def test_env_replacement_when_found(self):
        string_to_test = '%ABC% test'
        result = replace_env_ref_with_abs(string_to_test)
        self.assertEqual(result, 'Ronald test')

    def test_env_replacement_when_not_found(self):
        import os
        if 'DEF' in os.environ:
            del os.environ['DEF']  # Ensuring DEF is not present
        string_to_test = '%DEF% test'
        with self.assertRaises(Exception):
            replace_env_ref_with_abs(string_to_test)

    def test_validate_config_name(self):
        config_name = 'abc-def'  # valid name
        self.assertEqual(config_name, validate_config_name(config_name))

    def test_invalidate_config_name(self):
        config_name = '13abc-def'  # invalid name
        with self.assertRaises(InvalidNameError):
            validate_config_name(config_name)

def main():
    unittest.main()

if __name__ == '__main__':
    main()