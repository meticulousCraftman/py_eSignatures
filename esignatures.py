import requests
from requests.auth import HTTPBasicAuth
from loguru import logger

class ESignaturesError(Exception):
    pass

class ESginatures:
    
    def __init__(self, api_secret):
        print(f"API Secret -> {api_secret}")

        self.api_secret = api_secret
        self.base_url = f"https://{api_secret}:@esignatures.io/api/"


    def list_templates(self):

        url = self.base_url+"templates/"
        logger.debug(f"Target URL for fetching list of templates -> {url}")

        r = requests.get(url, headers={'Content-type': 'application/json'})
        if r.status_code == requests.codes.ok:
            return r.json()["data"]

        else:
            logger.error("Unable to get list of templates.")
            logger.error(f"Status code: {r.status_code}")
            logger.error(f"Error message: {r.text}")
            raise ESignaturesError(f"Unable to get the list of templates. Status Code: {r.status_code}")


