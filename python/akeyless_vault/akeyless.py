import json
from os import environ

import akeyless
from dotenv import load_dotenv

# create .env file with akeyless api access id and api access key
# load .env
load_dotenv()

# using public API endpoint
configuration = akeyless.Configuration(
    host="https://api.akeyless.io"
)

api_client = akeyless.ApiClient(configuration)
api = akeyless.V2Api(api_client)

body = akeyless.Auth(
    access_id=environ.get("AKEYLESS_ACCESS_ID"),
    access_key=environ.get("AKEYLESS_ACCESS_KEY")
)
res = api.auth(body)

# if auth was successful, there should be a token
token = res.token

body = akeyless.GetSecretValue(
    names=["postgres_neon"],
    token=token
)

body = akeyless.GetSecretValue(
    names=["postgres_neon"],
    token=token
)
res = api.get_secret_value(body)
