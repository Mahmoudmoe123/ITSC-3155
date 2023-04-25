import unittest
from tests import TestDatabaseConnection, TestRoutes

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDatabaseConnection)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestRoutes))

    runner = unittest.TextTestRunner(verbosity=2)
    test_results = runner.run(suite)
