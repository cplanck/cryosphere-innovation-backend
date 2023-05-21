import json
import os
import re
import urllib.parse
import uuid
from random import seed

# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from dotenv import load_dotenv
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from user_profiles.models import UserProfile
from user_profiles.serializers import UserProfileSerializer

from authentication.http_cookie_authentication import CookieTokenAuthentication

load_dotenv()


class CreateNewUser(APIView):

    def post(self, request):
        username = str(uuid.uuid4())
        email = request.data.get('email')
        password = request.data.get('password')

        if not all([username, email, password]):
            return Response({'error': 'Please provide an email and a password.'}, status=status.HTTP_400_BAD_REQUEST)

        elif email in User.objects.values_list('email', flat=True):
            print('YOU MADE IT IN HERE')
            return Response({'error': 'This email already exists in our system.'}, status=status.HTTP_400_BAD_REQUEST)

        elif not re.match(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email):
            return Response({'error': 'You may have not entered a valid email'}, status=status.HTTP_400_BAD_REQUEST)

        elif len(email) > 100 or len(password) > 100:
            return Response({'error': 'Your email or password might be too long'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                username=username, email=email, password=password)
        except:
            return Response({'error': 'Failed to create user.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({'access': str(access_token), 'refresh': str(refresh)}, status=status.HTTP_201_CREATED)


# class GoogleLogin(SocialLoginView):

#     """
#     This endpoint takes a POST request with the CODE from the Google URL in the body and returns the access/refresh tokens
#     """

#     adapter_class = GoogleOAuth2Adapter
#     callback_url = settings.WEBSITE_ROOT + \
#         '/auth/authentication/google/login/callback/'
#     client_class = OAuth2Client


# def google_oauth_login(request):
#     """
#     After successful Google authentication, this returns the CODE in the URL
#     which is used in dj-rest-auth/google/ to return the key
#     """

#     params = urllib.parse.urlencode(request.GET)
#     url = f'{settings.STANDALONE_FRONTEND_ROOT}/login/google/{params}'
#     return redirect(url)


class GoogleOneTap(APIView):
    def post(self, request):
        try:
            user_info = id_token.verify_oauth2_token(
                request.data, requests.Request(), os.environ['GOOGLE_CLIENT_ID'])
            # check if email exists, if so, return user info and access keys

            user = User.objects.get(email=user_info['email'])
            user_profile = UserProfile.objects.get(user=user)

            if user:
                print(user)
                refresh_token = RefreshToken.for_user(user)
                access_token = refresh_token.access_token
                # return JWT + user info
                response = HttpResponse(
                    json.dumps({
                        'refresh_token': str(refresh_token),
                        'access_token': str(access_token),
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'full_name': user_info['name'],
                        'user': UserProfileSerializer(user_profile).data
                    }))
                response.set_cookie('access_token', str(
                    access_token), httponly=True)
                response.set_cookie('refresh_token', str(
                    refresh_token), httponly=True)
                print(access_token)
                response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
                response['Access-Control-Allow-Credentials'] = 'true'
                return response
        except Exception as e:
            # invalid ID or bad request
            print(e)
            return HttpResponse(json.dumps({'endpoint': 'worked'}))


class TestRequest(APIView):

    authentication_classes = [CookieTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # print(request.META)
        print(request.user)
        # print(request.COOKIES)
        response = HttpResponse(json.dumps(
            {'User Requesting': request.user.username}))

        return response
