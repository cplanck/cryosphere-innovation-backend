
from django.urls import include, path
from rest_framework import routers

from instruments.endpoints import *

router = routers.DefaultRouter()

router.register('internal/instruments', InternalInstrumentEndpoint,
                basename='internal_instruments')

router.register('internal/deployments', InternalDeploymentEndpoint,
                basename='internal_deployments')

router.register('internal/simb3_instrument_migration',
                SIMB3MigrationEndpoint, basename='simb3_instrument_migration')

router.register('internal/simb3_deployment_migration',
                SIMB3DeploymentMigrationEndpoint, basename='simb3_deployment_migration')
urlpatterns = [
    path('', include(router.urls)),
]
