from datetime import datetime
from typing import Optional

from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        jwt_auth = JWTAuthentication()
        try:
            validated = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated)
            request.user = user
            return user
        except Exception:
            return None


jwt_auth = JWTAuth()
