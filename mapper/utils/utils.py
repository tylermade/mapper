"""
Utility functions
"""

import os
import requests
from bs4 import BeautifulSoup
from utils import const

def requestvpn(ip_limit, https=True):
    """
    Get a list of VPNs

    Parameters:
    ip_limit (int): Number of VPN IP addresses to return
    https (bool): HTTPS protocol True or False

    Returns:
    list: List of VPN IP addresses
    """
    assert isinstance(ip_limit, int), "You must provide a integer below 150"
    assert ip_limit <= 150, "The max limit available is 150 IPs"

    response = requests.get(const.PROXY_URL)
    souped = BeautifulSoup(response.text, "html.parser")
    table = souped.find("table", {"id": "proxylisttable"})
    tr = table.tbody.findAll("tr")
    ips = [rowmapping(tds.findAll("td")) for tds in tr]
    if https:
        result = [rowformatting(ip) for ip in ips if ip["https"]]
    else:
        result = [rowformatting(ip) for ip in ips if not ip["https"]]
    if len(result) > ip_limit:
        return result[:ip_limit]
    else:
        return result

def rowmapping(_input):
    """
    Assign row to dictionary
    
    Parameters:
    _input (list): list of datapoints per row

    Returns:
    dict: Dictionary of parsed row
    """
    https = lambda x: True if "yes" == x else False
    mapping = {
        "ip": _input[0].text,
        "port": _input[1].text,
        "country_code": _input[2].text,
        "country": _input[3].text,
        "anonymity": _input[4].text,
        "https": https(_input[6].text),
        "last_update": _input[7].text
    }
    return mapping

def rowformatting(_input):
    """
    Formats dictionary into IP address format

    Parameters:
    _input (dict): Dictionary of pre-format data

    Returns:
    str: IP Address with Port
    """
    return "{}:{}".format(_input["ip"], _input["port"])

def vpnup(func):
    """
    Must fix
    """
    def addproxy():
        ip = requestvpn(1, https=True)
        os.environ["http_proxy"] = ip
        os.environ["https_proxy"] = ip
        func()
        return addproxy