
from starlette.authentication import AuthenticationBackend, AuthenticationError, AuthCredentials, SimpleUser

from werkzeug.security import check_password_hash
from database.user import UserQueries

import base64
import binascii

def check_user(username: str, password: str):
    user_db = UserQueries()
    user = user_db.get_user(username)

    if user:
        correct_password = check_password_hash(user[4], password)
        if correct_password:
            return user

    return None


class AuthBackend(AuthenticationBackend):
    def __init__(self):
        self.user_db = UserQueries()

    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return None

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                return None
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError('Invalid basic auth credentials')

        username, _, password = decoded.partition(":")
        user = check_user(username, password)
        
        if user:
            return AuthCredentials(["authenticated"]), SimpleUser(username)
        else:
            return None
