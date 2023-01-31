import json
from os import environ

import akeyless
from dotenv import load_dotenv

class Akeyless:
    """Class containing methods to interact with akeyless api"""

    def __init__(self, access_id=None, access_key=None):
        """Instantiate Akeyless class

        Args:
            access_id (str, optional): Access id value
            access_key (str, optional): Access key value

        Returns:

        """

        # load .env
        load_dotenv()
        self.api = self._get_api_client()
        self.access_id = environ.get("AKEYLESS_ACCESS_ID") if not access_id else access_id
        self.access_key = environ.get("AKEYLESS_ACCESS_KEY")if not access_key else access_key
        self.token = self._get_auth_token()

    def _get_api_client(self):
        """Get akeyless api client

        Args:

        Returns:
            akeyless.api object

        """

        # using public API endpoint
        configuration = akeyless.Configuration(
            host="https://api.akeyless.io"
        )

        api_client = akeyless.ApiClient(configuration)
        return akeyless.V2Api(api_client)
        
    def _get_auth_token(self) -> str:
        """Get auth token
        https://github.com/akeylesslabs/akeyless-python/blob/master/docs/Auth.md

        Args:

        Returns:
            str: Auth token

        """

        body = akeyless.Auth(
            access_id=self.access_id,
            access_key=self.access_key
        )
        return self.api.auth(body).token

    def get_secret(self, secret_names) -> dict:
        """Get secret value from akeyless vault
        https://github.com/akeylesslabs/akeyless-python/blob/master/docs/GetSecretValue.md

        Args:
            secret_name (list): Name of secret in akeyless vault

        Returns:
            dict: Dictionary containing secret value

        """

        body = akeyless.GetSecretValue(
            names=secret_names,
            token=self.token
        )

        return self.api.get_secret_value(body)

    def create_static_secret(self, secret_name, secret_value) -> dict:
        """Create static secret
        https://github.com/akeylesslabs/akeyless-python/blob/master/docs/CreateSecret.md

        Args:
            secret_name (str): Name of secret
            secret_value (str): Value of secret

        Returns:
            dict: Dictionary containing name of new secret

        """

        body = akeyless.CreateSecret(
            name=secret_name,
            value=secret_value,
            token=self.token
        )
        return self.api.create_secret(body)

    # def create_role(self, role_name, roles):
    #     """Create role in akeyless vault
    #     https://github.com/akeylesslabs/akeyless-python/blob/master/docs/CreateRole.md
    #     https://github.com/akeylesslabs/akeyless-python/blob/master/docs/SetRoleRule.md

    #     Args:

    #     Returns:

    #     """

    #     body = akeyless.CreateRole(
    #         token=self.token,
    #         name=role_name
    #     )
    #     api.create_role(body)

    #     body = akeyless.SetRoleRule(
    #         capability=roles,
    #         path="/dev/*",
    #         role_name=role_name,
    #         token=self.token
    #     )

    #     for rule_type in ["role-rule", "item-rule", "auth-method-rule"]:
    #         body.rule_type = rule_type
    #         api.set_role_rule(body)
