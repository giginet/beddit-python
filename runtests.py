import unittest

if __name__ == '__main__':
    suite = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=1).run(suite)
