# coding: utf8
import unittest
from tests_db_aggregator import TestDBAggregator

def suite_tests():
    suite = unittest.TestSuite()
    suite.addTest(TestDBAggregator())
    return suite

if __name__ == '__main__':
    suite_tests().main()
