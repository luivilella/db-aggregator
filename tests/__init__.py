# coding: utf8
import unittest
from tests_dbaggregator import TestDBAggregator
from tests_utils_connection_string import TestUtilsConnectionString


def suite_tests():
    suite = unittest.TestSuite()
    suite.addTest(TestDBAggregator())
    suite.addTest(TestUtilsConnectionString())

    return suite


if __name__ == '__main__':
    suite_tests().main()
