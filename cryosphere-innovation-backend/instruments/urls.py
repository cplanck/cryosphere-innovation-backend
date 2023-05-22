
from django.urls import include, path
from rest_framework import routers

from instruments.endpoints import *

router = routers.DefaultRouter()

router.register('internal/instruments', InternalInstrumentEndpoint,
                basename='internal_instruments')
router.register('deployments', DeploymentEndpoint, basename='deployments')

urlpatterns = [
    path('', include(router.urls)),
]
