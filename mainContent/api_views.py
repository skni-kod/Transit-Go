from django.contrib.auth import authenticate, login
from rest_framework import viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.mixins import DestroyModelMixin, ListModelMixin, CreateModelMixin, RetrieveModelMixin, \
    UpdateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.mixins import DestroyModelMixin
from django.db.models import OuterRef, Subquery

from .serializers import *


class UserViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []


class BusStopViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer
    authentication_classes = []
    permission_classes = []


class CourseStageViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = CourseStage.objects.all()
    serializer_class = CourseStageSerializer
    authentication_classes = []
    permission_classes = []


class WorkScheduleViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = WorkSchedule.objects.all()
    serializer_class = WorkScheduleSerializer
    authentication_classes = []
    permission_classes = []


class VehicleVehFeatureViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = VehicleVehFeature.objects.all()
    serializer_class = VehicleVehFeatureSerializer
    authentication_classes = []
    permission_classes = []


class VehicleViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    authentication_classes = []
    permission_classes = []


class VehFeatureTravelerViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = VehFeatureTraveler.objects.all()
    serializer_class = VehFeatureTravelerSerializer
    authentication_classes = []
    permission_classes = []


class VehFeatureViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = VehFeature.objects.all()
    serializer_class = VehFeatureSerializer
    authentication_classes = []
    permission_classes = []


class TravelerViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = Traveler.objects.all()
    serializer_class = TravelerSerializer
    authentication_classes = []
    permission_classes = []


class TravRideViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = TravRide.objects.all()
    serializer_class = TravRideSerializer
    authentication_classes = []
    permission_classes = []


class SimulationViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = Simulation.objects.all()
    serializer_class = SimulationSerializer
    authentication_classes = []
    permission_classes = []


class TicketsViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = Tickets.objects.all()
    serializer_class = TicketsSerializer
    authentication_classes = []
    permission_classes = []


class TicketsClientViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = TicketsClient.objects.all()
    serializer_class = TicketsClientSerializer
    authentication_classes = []
    permission_classes = []


class SearchHistoryViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer
    authentication_classes = []
    permission_classes = []


class OpinionViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = Opinion.objects.all()
    serializer_class = OpinionSerializer
    authentication_classes = []
    permission_classes = []


class RaportsViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = Raports.objects.all()
    serializer_class = RaportsSerializer
    authentication_classes = []
    permission_classes = []


class DriverVehicleViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = DriverVehicle.objects.all()
    serializer_class = DriverVehicleSerializer
    authentication_classes = []
    permission_classes = []


class DriverViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    authentication_classes = []
    permission_classes = []


class BusStopsDistViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = BusStopsDist.objects.all()
    serializer_class = BusStopsDistSerializer
    authentication_classes = []
    permission_classes = []


class BusStopsTimeViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = BusStopsTime.objects.all()
    serializer_class = BusStopsTimeSerializer
    authentication_classes = []
    permission_classes = []


class ClientViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Client.objects.filter(user_id_user=user_id)


class ClientBusStopViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = ClientBusStop.objects.all()
    serializer_class = ClientBusStopSerializer
    authentication_classes = []
    permission_classes = []


class CourseViewSet(viewsets.ModelViewSet, DestroyModelMixin):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = []
    permission_classes = []


class ClientBusStopFromClientViewSet(viewsets.GenericViewSet,
                                     ListModelMixin,
                                     CreateModelMixin,
                                     RetrieveModelMixin,
                                     UpdateModelMixin,
                                     DestroyModelMixin):
    serializer_class = ClientBusStopSerializer

    def get_queryset(self):
        client_id = self.kwargs.get('client_id')  # Pobierz ID klienta z URL-a
        queryset = ClientBusStop.objects.filter(id_client=client_id)
        return queryset


class UserBusStopFromClientViewSet(viewsets.GenericViewSet,
                                   ListModelMixin,
                                   CreateModelMixin,
                                   RetrieveModelMixin,
                                   UpdateModelMixin,
                                   DestroyModelMixin):
    serializer_class = ClientBusStopSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')  # Pobierz ID użytkownika z URL-a

        # Podzapytanie, aby uzyskać id_client dla danego user_id
        client_id_subquery = Client.objects.filter(user_id_user=user_id).values('id_client')[:1]

        queryset = ClientBusStop.objects.filter(id_client__in=Subquery(client_id_subquery))
        return queryset


class TravelerFromClientViewSet(viewsets.GenericViewSet,
                                ListModelMixin,
                                CreateModelMixin,
                                RetrieveModelMixin,
                                UpdateModelMixin,
                                DestroyModelMixin):
    serializer_class = TravelerSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')

        # Podzapytanie, aby uzyskać client_id dla danego user_id
        client_id_subquery = Client.objects.filter(user_id_user=user_id).values('id_client')[:1]

        queryset = Traveler.objects.filter(client_id_client__in=client_id_subquery)
        return queryset
