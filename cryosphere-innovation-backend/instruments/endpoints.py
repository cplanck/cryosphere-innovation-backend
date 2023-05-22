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
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class InternalInstrumentEndpoint(viewsets.ModelViewSet):
    """
    Endpoint for CRUD on Instrument model for internally made 
    instruments, e.g., SIMB3. The create() method is only available 
    to staff users. list() returns a paginated response of all istruments
    with internal = True.

    The main purpose of this endpoint is for consumption by the CI frontend.
    It largely replaces the SIMB3 endpoint and instead returns all internal
    instruments. 

    Right now there is no support for privacy checks. In the future, we should overwrite 
    the list() method to refine the queryset to check if:
        - the user is the owner
        - the user is in the collaborators
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


class DeploymentEndpoint(viewsets.ModelViewSet):

    """
    Endpoint for returning users deployments, either all or by ID. Handles
    all CRUD. For GET requests it returns an instrument object with each 
    deployment. For POST/PUT/PATCH requests it accepts only an ID for instrument.
    """
    authentication_classes = [CookieTokenAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = DeploymentPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DeploymentGETSerializer
        else:
            return DeploymentSerializer

    def get_queryset(self):
        instrument_id = self.request.query_params.get('instrument')
        qs = Deployment.objects.filter(
            user=self.request.user).order_by('-last_modified')
        qs = qs if not instrument_id else qs.filter(
            instrument__id=instrument_id)
        return qs
