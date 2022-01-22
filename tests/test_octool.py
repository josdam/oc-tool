"""Tests for OC Tool"""

import os
import unittest

import octool

TEST_DIR = os.path.dirname(__file__)


class TestOCTool(unittest.TestCase):
    """Tests for OC Tool"""

    def test_read_config_file(self):
        """Test read config file"""
        octool.OC_LOGIN_CONFIG_FILE = TEST_DIR + "/config.yml"
        octool.read_config_file()
        self.assertEqual(octool.SERVERS, [['test-server',
                                           'test description',
                                           'https://api.server',
                                           'https://console.server']])


if __name__ == '__main__':
    unittest.main()
