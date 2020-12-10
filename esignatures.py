import requests
from requests.auth import HTTPBasicAuth
from loguru import logger


class ESignaturesError(Exception):
    pass

class ESginatures:
    
    def __init__(self, api_secret):
        self.api_secret = api_secret
        self.base_url = f"https://{api_secret}:@esignatures.io/api/"


    def list_templates(self):
        """
        Returns the list of templates you can send.
        """

        url = self.base_url+"templates/"

        r = requests.get(url, headers={'Content-type': 'application/json'})
        if r.status_code == requests.codes.ok:
            logger.success("")
            return r.json()["data"]

        else:
            logger.error(f"Unable to get list of templates. Status code: {r.status_code}")
            logger.error(f"Error message: {r.text}")

            raise ESignaturesError(f"Unable to get the list of templates. Status Code: {r.status_code}")
    

    def query_template(self, template_id):
        """
        Returns the details of the template. The Placeholder keys are specified with the template editor between {{ }} double curly brackets.
        """
        url = self.base_url + f"templates/{template_id}"
        response = requests.get(url)

        if response.status_code == requests.codes.ok:
            return response.json()["data"]
        
        else:
            logger.error(f"Unable to get list of templates. Status code: {r.status_code}")
            logger.error(f"Error message: {r.text}")

            raise ESignaturesError(f"Unable to query template. Status Code: {r.status_code}")

