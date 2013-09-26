#!/usr/bin/env python
# -*- coding: utf-8 -*-

import doctest
import unittest
import sys
import copy
from tests.testapiclients import Test_ApiClients
from tests.testapiusers import Test_ApiUsers
from tests.testapiwallets import Test_ApiWallets
from tests.testcardregistrations import CardRegistration
from tests.testconfigurations import Test_Configurations
from tests.testpayins import Test_PayIns
from tests.testpayouts import Test_PayOuts
from tests.testrefunds import TestRefunds
from tests.testtokens import Test_Tokens
from tests.testtransfers import Test_Transfers


suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(Test_ApiClients))
suite.addTest(unittest.makeSuite(Test_ApiUsers))
suite.addTest(unittest.makeSuite(Test_ApiWallets))
suite.addTest(unittest.makeSuite(Test_Configurations))
suite.addTest(unittest.makeSuite(Test_PayIns))
suite.addTest(unittest.makeSuite(Test_PayOuts))
suite.addTest(unittest.makeSuite(Test_Tokens))
suite.addTest(unittest.makeSuite(Test_Transfers))
suite.addTest(unittest.makeSuite(TestRefunds))
suite.addTest(unittest.makeSuite(CardRegistration))

modules = ['mangopaysdk']

for module in modules:
    m = __import__(module, fromlist=[module])

runner = unittest.TextTestRunner(verbosity=1)
result = runner.run(suite)

if not result.wasSuccessful():
    sys.exit(1)
