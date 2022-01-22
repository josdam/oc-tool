import os
import unittest

import octool

test_dir = os.path.dirname(__file__)


class TestOCTool(unittest.TestCase):

    def test_read_config_file(self):
        octool.OC_LOGIN_CONFIG_FILE = test_dir + "/config.yml"
        octool.read_config_file()
        self.assertEqual(octool.SERVERS, [['test-server',
                                           'test description',
                                           'https://api.server',
                                           'https://console.server']])


if __name__ == '__main__':
    unittest.main()
