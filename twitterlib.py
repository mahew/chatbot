import os
import json, requests


# https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/master/User-Lookup/get_users_with_bearer_token.py
def auth():
    return "AAAAAAAAAAAAAAAAAAAAAFs6IgEAAAAAYs15iNGgomSWNmnQ3NB1ZqZwrHA%3DPDZU6maEku0jJIIbU8b3laIcAsaADfjYNFoMfpsfCqQzJzyFmK"


def create_url(handle):
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    usernames = "usernames={}".format(handle)
    user_fields = "user.fields=description,created_at"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_user_details(handle):
    bearer_token = auth()
    url = create_url(handle)
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    print(json.dumps(json_response, indent=4, sort_keys=True))