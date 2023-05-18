from allauth.socialaccount.providers.google import views as google_views
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from authentication.endpoints import *

# from general.endpoints import *

urlpatterns = [
    # post user creds (username + password or token) and get JWT pain
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # post refresh token in body and get updated access token if refresh is valid
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),


    # Google Redirect URI endpoint. Overwrite needed to complete the Oauth handshake process to get the user token on the front end.
    path('authentication/google/login/callback/',
         google_oauth_login, name='google_callback'),

    # used by the standalone front end for the final POST request to get the user ID token. It takes a CODE (from Google) which it validates and then responds with a user token
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),

    # endpoint for the "Login with Google" button. Points to the allauth view which redirects to the Google login page
    path('auth/login', google_views.oauth2_login,
         name='login with google button'),

    # Test endpoint for checking permissions access on protected views
    path('testrequest', TestRequest.as_view(), name='test endpoint'),

    # dj rest auth URLS  (LIKELY NOT USED)
    path('dj-rest-auth/', include('dj_rest_auth.urls')),

    # general rest framework authentication endpoints (LIKELY NOT USED)
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # non-social auth user creation
    path('user/create', CreateNewUser.as_view(), name='create new user'),

    # google one-tap social login endpoint
    path('google/login/', GoogleOneTap.as_view(), name='google_onetap_login')

]
