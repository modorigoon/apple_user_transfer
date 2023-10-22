import json
import time
import jwt
import requests
from typing import Final

from termcolor import colored


class Apple:

    def __init__(self, private_key_file: str, team_id: str, key_id: str, client_id: str, target_team_id: str):
        self.__private_key_file: Final = private_key_file
        self.__team_id: Final = team_id
        self.__key_id: Final = key_id
        self.__client_id: Final = client_id
        self.__target_team_id: Final = target_team_id

        self.__APPLE_API_BASE_URL = 'https://appleid.apple.com'
        self.__client_secret = None
        self.__access_token = None

    def __generate_client_secret(self) -> str | None:
        with open(self.__private_key_file, 'r') as private_key_file:
            private_key = private_key_file.read()
            validity_minutes = 20
            now = int(time.time())
            token_expiration = now + (60 * validity_minutes)

            payload = {
                'iss': self.__team_id,
                'iat': now,
                'exp': token_expiration,
                'aud': self.__APPLE_API_BASE_URL,
                'sub': self.__client_id
            }

            try:
                return jwt.encode(
                    payload=payload, key=private_key.encode('utf-8'), algorithm='ES256', headers={'kid': self.__key_id}
                )
            except TypeError as e:
                print(colored(f'🔒 Generate client secret failed. (reason: {e})', 'red'))
                return None

    def __get_access_token(self) -> str | None:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'scope': 'user.migration',
            'client_id': self.__client_id,
            'client_secret': self.__client_secret
        }
        request_url = f'{self.__APPLE_API_BASE_URL}/auth/token'
        try:
            response = requests.post(request_url, headers=headers, data=body)
            auth_obj = json.loads(response.text)

            return auth_obj['access_token']
        except Exception as e:
            print(colored(f'🔒 Request access token failed. (reason: {e})', 'red'))
            return None

    def authorize(self) -> bool:
        self.__client_secret = self.__generate_client_secret()
        if self.__client_secret is None:
            return False
        self.__access_token = self.__get_access_token()
        if self.__access_token is None:
            return False

        return True

    def transfer_sub(self, sub: str):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Bearer {self.__access_token}'
        }
        body = {
            'sub': sub,
            'target': self.__target_team_id,
            'client_id': self.__client_id,
            'client_secret': self.__client_secret
        }
        request_url = f'{self.__APPLE_API_BASE_URL}/auth/usermigrationinfo'
        try:
            resource = requests.post(request_url, headers=headers, data=body)
            return json.loads(resource.text)
        except Exception as e:
            return {'error': 'request_error', 'error_description': str(e)}
