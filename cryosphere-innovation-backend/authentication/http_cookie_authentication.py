import jwt
from django.conf import settings
from django.contrib.auth.models import User
from dotenv import load_dotenv
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

load_dotenv()


class CookieTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        access_token = self.get_token_from_cookie(request)

        if not access_token:
            return None

        try:
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        user_id = payload.get('user_id')

        if not user_id:
            raise AuthenticationFailed('Missing user_id in token payload')

        # You should implement your own logic for fetching the user based on the user_id
        user = User.objects.get(id=user_id)

        return (user, access_token)

    def get_token_from_cookie(self, request):
        access_token = None

        if 'access_token' in request.COOKIES:
            access_token = request.COOKIES['access_token']

        return access_token
