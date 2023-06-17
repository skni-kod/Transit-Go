from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated, PermissionDenied

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id_user', 'role', 'first_name', 'last_name', 'phone_number', 'email', 'username',
                  'home_address', 'password', 'last_login', 'is_superuser', 'is_staff',
                  'is_active', 'date_joined']


class BusStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStop
        fields = ['id_bus_stop', 'code_stop', 'city', 'name', 'gps_n', 'gps_e',
                  'loop', 'wait_time', 'charger_kw']


class CourseStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseStage
        fields = ['id_course_stage', 'stage', 'arr_time', 'dep_time', 'charging_time',
                  'id_bus_stop_start', 'id_course', 'id_bus_stop_end']


class WorkScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSchedule
        fields = ['id_work_shedule', 'id_course', 'start_time', 'end_time', 'id_driver']


class VehicleVehFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleVehFeature
        fields = ['id_vehicle_veh_feature', 'id_vehicle', 'id_feature']


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id_vehicle', 'nr_vehicle', 'model', 'brand', 'date_purchase',
                  'date_inspection', 'max_number_passengers', 'battery_kwh', 'cons_kwh']


class VehFeatureTravelerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehFeatureTraveler
        fields = ['id_veh_feature_traveler', 'id_feature', 'id_traveler']


class VehFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehFeature
        fields = ['id_feature', 'name', 'content']


class TravelerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traveler
        fields = ['id_traveler', 'start_time', 'stop_time', 'client_id_client',
                  'id_bus_stop_start', 'id_bus_stop_end']


class TravRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravRide
        fields = ['id_trav_ride', 'id_traveler', 'id_course', 'id_course_stage_start',
                  'id_course_stage_end', 'id_bus_stop_start', 'id_bus_stop_end']


class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = ['current_location', 'id_vehicle', 'id_user', 'number_free_seat']


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ['id_history', 'start_time', 'end_time', 'id_bus_stop_start',
                  'id_bus_stop_end', 'id_client']


class OpinionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opinion
        fields = ['id_opinion', 'content', 'rating', 'id_client',
                  'id_course']


class RaportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raports
        fields = ['id_raport', 'content']


class DriverVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverVehicle
        fields = ['id_driver_vehicle', 'id_driver', 'id_vehicle']


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id_driver', 'date_employment', 'id_user']


class BusStopsDistSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStopsDist
        fields = ['id_bus_stops_dist', 'id_bus_stop_start', 'id_bus_stop_end', 'distance', 'day_of_week', 'hour']


class BusStopsTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusStopsTime
        fields = ['id_bus_stops_time', 'id_bus_stop_start', 'id_bus_stop_end', 'day_of_week', 'hour', 'time']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id_client', 'user_id_user']


class ClientBusStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientBusStop
        fields = ['id_fav_place', 'name', 'id_bus_stop', 'id_client']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id_course', 'start_time', 'end_time', 'id_driver_vehicle']


class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = ['id_tickets', 'name', 'duration_time', 'price']


class TicketsClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketsClient
        fields = ['id_tickes_client', 'time_to_end', 'client_id_client', 'tickets_id_tickets']