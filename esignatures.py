import requests
from requests.auth import HTTPBasicAuth
from loguru import logger
from typing import List


class ESignaturesError(Exception):
    pass


class Signer:
    
    def __init__(self, name, email, mobile="", 
                    company_name=None, 
                    redirect_url=None, 
                    signing_order="1",  # Keeping the sigining order value same across all Signers will send the contract to all of them at the same time
                    auto_sign="no",
                    embedded_sign_page="no",
                    embedded_redirect_iframe_only="no",
                    skip_signature_request="no",
                    skip_signer_identification="no",    # Let the signer verification happen, otherwise the contract would not be legally binding
                    skip_final_contract_delivery="no"
                ):
        
        if len(email) == 0 and len(mobile) == 0:
            raise ESignaturesError("Email or Mobile number is required for creating a Signer.")

        self.name = name
        self.email = email
        self.mobile = mobile

        self.company_name = company_name
        self.redirect_url = redirect_url
        self.signing_order = signing_order
        
        self.auto_sign = auto_sign
        self.embedded_sign_page = embedded_sign_page
        self.embedded_redirect_iframe_only = embedded_redirect_iframe_only
        self.skip_signature_request = skip_signature_request
        self.skip_signer_identification = skip_signer_identification
        self.skip_final_contract_delivery = skip_final_contract_delivery
    
    def get_dict(self):
        """
        Generates the required dictionary that is sent to eSignatures.io
        """
        t = {
            "name": self.name,
            "signing_order": self.signing_order,
            "auto_sign": self.auto_sign,
            "embedded_sign_page": self.embedded_sign_page,
            "embedded_redirect_iframe_only": self.embedded_redirect_iframe_only,
            "skip_signature_request": self.skip_signature_request,
            "skip_signer_identification": self.skip_signer_identification,
            "skip_final_contract_delivery": self.skip_final_contract_delivery
        }

        if len(self.email) > 0:
            t["email"] = self.email
        
        if len(self.mobile) > 0:
            t["mobile"] = self.mobile

        if self.company_name is not None:
            t["company_name"] = self.company_name
        
        if self.redirect_url is not None:
            t["redirect_url"] = self.redirect_url
        
        return t




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

    
    def send_contract(
        self, template_id: str, signers: List[Signer],
        title: str = "",
        metadata: str = "",
        locale: str = "en",
        test: str = "no"
    ):
        data = {
            "template_id": template_id,
            "signers": [signer.get_dict() for signer in signers],
            "locale": locale,
            "test": test
        }

        if len(title) > 0:
            data["title"] = title
        
        if len(metadata) > 0:
            data["metadata"] = metadata
        


        logger.debug(data)

        url = self.base_url + "contracts"
        response = requests.post(url, json=data)

        if response.status_code == requests.codes.ok:
            return response.json()
        
        else:
            logger.error(f"Unable to get list of templates. Status code: {response.status_code}")
            logger.error(f"Error message: {response.text}")

            raise ESignaturesError(f"Unable to query template. Status Code: {response.status_code}")
