from authentication.http_cookie_authentication import CookieTokenAuthentication
from django.db.models import Q
from django.shortcuts import render
from rest_framework import pagination, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import (IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Deployment, Instrument
from .serializers import (DeploymentGETSerializer, DeploymentSerializer,
                          InstrumentSerializer)


class InstrumentPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class InternalInstrumentEndpoint(viewsets.ModelViewSet):
    """
    Endpoint for CRUD on Instrument model for internally made
    instruments, e.g., SIMB3. The create() method is only available
    to staff users. list() returns a paginated response of istruments
    with internal = True.

    If an instrument has a deployment that with private=True, then it is
    automatically removed from public view unless the user viewing is either
    1) the owner of the instrument or 2) listed in the collaborators.


    The main purpose of this endpoint is for consumption by the CI frontend.
    It largely replaces the SIMB3 endpoint and instead returns all internal
    instruments.
    """
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    serializer_class = InstrumentSerializer
    pagination_class = InstrumentPagination
    queryset = Instrument.objects.filter(
        internal=True).order_by('-last_modified')

    def get_queryset(self):
        """
        Get a queryset of all instruments, unless the instrument has a deployment with private=True
        AND the request.user is not either 1) the owner of the instrument or 2) on the list of
        collaborators
        """
        if self.request.user.is_anonymous:
            instruments = Instrument.objects.exclude(
                Q(deployment__private=True))
        else:
            instruments = Instrument.objects.exclude(
                Q(deployment__private=True) & ~(
                    Q(owner=self.request.user) | Q(
                        deployment__collaborators=self.request.user)
                )
            )
        return instruments.order_by('-last_modified')

    def create(self, request):

        if request.user.is_staff:
            data = request.data
            data['internal'] = True
            serializer = self.get_serializer(data=data)

            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            else:
                return Response('There was a problem with your request', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class DeploymentPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class InternalDeploymentEndpoint(viewsets.ModelViewSet):

    """
    Endpoint for returning users deployments, either all or by ID. Handles
    all CRUD. For GET requests it returns an instrument object with each
    deployment. For POST/PUT/PATCH requests it accepts only an ID for instrument.

    This endpoint does a couple things
    -Return deployment(s) when given an instrument_id as a query param (main use cases for CI frontend)
    -Return the list of deployments that meet the following criteria
        - Are public (private=False)
        - Are of instruments they are listed as owners on
        - Are deployments that they are listed as collaborators on
    """
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    pagination_class = DeploymentPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DeploymentGETSerializer
        else:
            return DeploymentSerializer

    def get_queryset(self):

        deployments = Deployment.objects.exclude(
            Q(private=True) & ~(
                Q(instrument__owner=self.request.user) | Q(
                    collaborators=self.request.user)
            )
        )
        deployments = deployments.order_by('-last_modified')
        instrument_id = self.request.query_params.get('instrument')
        deployments = deployments if not instrument_id else deployments.filter(
            instrument__id=instrument_id)

        return deployments

    def create(self, request):

        if request.user.is_staff:
            data = request.data
            data['internal'] = True
            serializer = self.get_serializer(data=data)

            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            else:
                return Response('There was a problem with your request', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class SIMB3MigrationEndpoint(viewsets.ModelViewSet):

    """
    Temporary endpoint for porting SIMB3s from the old system to the new system

    """
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    serializer_class = InstrumentSerializer
    pagination_class = InstrumentPagination

    def create(self, request):

        print(request.data)
        data = request.data
        data['internal'] = True
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response('There was a problem with your request', status=status.HTTP_400_BAD_REQUEST)


class SIMB3DeploymentMigrationEndpoint(viewsets.ViewSet):

    """
    Temporary endpoint for porting SIMB3s deployment data from the old system to the new system

    """

    def partial_update(self, request, *args, **kwargs):
        instrument_id = kwargs['pk']

        deployment_to_update = Deployment.objects.get(
            instrument=instrument_id)

        deployment_to_update = Deployment.objects.get(instrument=instrument_id)
        serializer = DeploymentSerializer(
            deployment_to_update, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'Deployment updated'}, status=status.HTTP_200_OK)
        else:
            return Response({'There was a problem with the request'}, status=status.HTTP_400_BAD_REQUEST)
