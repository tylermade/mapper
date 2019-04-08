"""
Download module
"""

import requests
from utils.utils import vpnup

@vpnup
def download_tile(url):
    """
    Download map tile

    Parameters:
    url (str): url of map tile

    Returns:
    bytes: raw image binary file
    """
    response = requests.get(url)
    print(response)

if __name__ == "__main__":
    download_tile("https://realpython.com/primer-on-python-decorators/")