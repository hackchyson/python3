#!/usr/bin/env python3
"""
@project: python3
@file: test_doctest_
@author: mike
@time: 2021/2/20
 
@function:
"""
import doctest
import unittest
import doctest_

suite = unittest.TestSuite()
suite.addTest(doctest.DocTestSuite(doctest_))
runner = unittest.TextTestRunner()
print(runner.run(suite))
