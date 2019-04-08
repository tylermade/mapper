"""
Test for Utility Functions
"""

import os
import unittest
import mock
import requests
from mapper.utils import utils

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
sample_res_file = os.path.join(CURR_DIR, "docs/sample_vpn_response.html")

class sample_http_response():
    def __init__(self, _input):
        with open(sample_res_file, "r") as fp:
            self.text = fp.read()

class sample_data_point():
    def __init__(self, _input):
        self.text = _input

class TestRequestVpn(unittest.TestCase):
    @mock.patch("requests.get", side_effect=sample_http_response)
    def test_requestvpn(self, sample_http_input):
        result = utils.requestvpn(1, https=True)
        assert result == ["104.248.7.88:3128"]
    
    @mock.patch('requests.get', side_effect=sample_http_response)
    def test_requestvpn_many(self, sample_http_input):
        result = utils.requestvpn(150, https=False)
        assert len(result) == 150
        
    def test_rowmapping_http(self):
        fake_input = [
            sample_data_point("104.248.7.88"),
            sample_data_point("3128"),
            sample_data_point("US"),
            sample_data_point("United States"),
            sample_data_point("Anonymous"),
            sample_data_point("None"),
            sample_data_point("no"),
            sample_data_point("1 hour ago")
        ]
        expected_output = {
            "ip": "104.248.7.88",
            "port": "3128",
            "country_code": "US",
            "country": "United States",
            "anonymity": "Anonymous",
            "https": False,
            "last_update": "1 hour ago"
        }
        result = utils.rowmapping(fake_input)
        self.assertDictEqual(result, expected_output)

    def test_rowmapping_https(self):
        fake_input = [
            sample_data_point("104.248.7.88"),
            sample_data_point("3128"),
            sample_data_point("US"),
            sample_data_point("United States"),
            sample_data_point("Anonymous"),
            sample_data_point("None"),
            sample_data_point("yes"),
            sample_data_point("1 hour ago")
        ]
        expected_output = {
            "ip": "104.248.7.88",
            "port": "3128",
            "country_code": "US",
            "country": "United States",
            "anonymity": "Anonymous",
            "https": True,
            "last_update": "1 hour ago"
        }
        result = utils.rowmapping(fake_input)
        self.assertDictEqual(result, expected_output)
    
    def test_rowformatting(self):
        _input = {
            "ip": "104.248.7.88",
            "port": "3128",
            "country_code": "US",
            "country": "United States",
            "anonymity": "Anonymous",
            "https": True,
            "last_update": "1 hour ago"
        }
        result = utils.rowformatting(_input)
        assert result == "104.248.7.88:3128"