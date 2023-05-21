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

    # non-social auth user creation
    path('user/create', CreateNewUser.as_view(), name='create new user'),

    # google one-tap social login endpoint
    path('google/login/', GoogleOneTap.as_view(), name='google_onetap_login')

]
