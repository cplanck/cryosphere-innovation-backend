from django.urls import include, path
from rest_framework import routers

from user_profiles.endpoints import *

router = routers.DefaultRouter()

router.register('profile', UserProfileEndpoint, basename='user_profile')

urlpatterns = [
    path('', include(router.urls)),
]
