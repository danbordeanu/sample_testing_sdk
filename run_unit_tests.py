import unittest

from helpers.config_parser import check_if_config_exists


class MyUnitTest(unittest.TestCase):

    def test_is_there_config(self):
        '''
        Test if there is config file
        :return:
        '''
        self.assertTrue(check_if_config_exists('../config.ini'), 'Uhhh, no config file')

if __name__ == '__main__':
    unittest.main()
