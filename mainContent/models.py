from django.db import models
from django.forms import widgets
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager


class BusStop(models.Model):
    id_bus_stop = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    code_stop = models.CharField(max_length=5)
    city = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    gps_n = models.DecimalField(max_digits=18, decimal_places=9)
    gps_e = models.DecimalField(max_digits=18, decimal_places=9)
    loop = models.DecimalField(max_digits=1, decimal_places=0)
    wait_time = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    charger_kw = models.DecimalField(max_digits=5, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'bus_stop'


class BusStopsDist(models.Model):
    id_bus_stops_dist = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    id_bus_stop_start = models.ForeignKey(BusStop, models.DO_NOTHING, db_column='id_bus_stop_start')
    id_bus_stop_end = models.ForeignKey(BusStop, models.DO_NOTHING,
                                        db_column='id_bus_stop_end', related_name='busstopsdist_id_bus_stop_end_set')
    distance = models.DecimalField(max_digits=4, decimal_places=0)
    day_of_week = models.CharField(max_length=15)
    hour = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bus_stops_dist'


class BusStopsTime(models.Model):
    id_bus_stops_time = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    id_bus_stop_start = models.ForeignKey(BusStop, models.DO_NOTHING, db_column='id_bus_stop_start')
    id_bus_stop_end = models.ForeignKey(BusStop, models.DO_NOTHING,
                                        db_column='id_bus_stop_end', related_name='busstopstime_id_bus_stop_end_set')
    day_of_week = models.CharField(max_length=15)
    hour = models.DateTimeField()
    time = models.DecimalField(max_digits=4, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'bus_stops_time'


class Client(models.Model):
    id_client = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    user_id_user = models.OneToOneField('User', models.DO_NOTHING, db_column='user_id_user')

    class Meta:
        managed = False
        db_table = 'client'


class ClientBusStop(models.Model):
    id_fav_place = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    name = models.CharField(max_length=30)
    id_bus_stop = models.ForeignKey(BusStop, models.DO_NOTHING, db_column='id_bus_stop')
    id_client = models.ForeignKey(Client, models.DO_NOTHING, db_column='id_client')

    class Meta:
        managed = False
        db_table = 'client_bus_stop'

    def __str__(self):
        return(f"{self.id_fav_place}")


class Course(models.Model):
    id_course = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    id_driver_vehicle = models.ForeignKey('DriverVehicle', models.DO_NOTHING, db_column='id_driver_vehicle')

    class Meta:
        managed = False
        db_table = 'course'


class CourseStage(models.Model):
    id_course_stage = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    stage = models.DecimalField(max_digits=3, decimal_places=0)
    arr_time = models.DateTimeField()
    dep_time = models.DateTimeField()
    charging_time = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    id_bus_stop_start = models.ForeignKey(BusStop, models.DO_NOTHING, db_column='id_bus_stop_start')
    id_course = models.ForeignKey(Course, models.DO_NOTHING, db_column='id_course')
    id_bus_stop_end = models.ForeignKey(BusStop, models.DO_NOTHING,
                                        db_column='id_bus_stop_end', related_name='coursestage_id_bus_stop_end_set')

    class Meta:
        managed = False
        db_table = 'course_stage'


class Driver(models.Model):
    id_driver = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    date_employment = models.DateField()
    id_user = models.OneToOneField('User', db_column='id_user', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'driver'


class DriverVehicle(models.Model):
    id_driver_vehicle = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    id_driver = models.ForeignKey(Driver, models.DO_NOTHING, db_column='id_driver')
    id_vehicle = models.ForeignKey('Vehicle', models.DO_NOTHING, db_column='id_vehicle')

    class Meta:
        managed = False
        db_table = 'driver_vehicle'


class Opinion(models.Model):
    id_opinion = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    content = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    id_client = models.ForeignKey(Client, models.DO_NOTHING, db_column='id_client')
    id_course = models.ForeignKey(Course, models.DO_NOTHING, db_column='id_course')

    class Meta:
        managed = False
        db_table = 'opinion'


class Raports(models.Model):
    id_raport = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    content = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'raports'

class RaportsUnlogged(models.Model):
    id_raport = models.AutoField(primary_key=True)
    content = models.TextField(max_length=1024,)

    class Meta:
        managed = False
        db_table = 'raports'

class SearchHistory(models.Model):
    id_history = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    id_bus_stop_start = models.ForeignKey(BusStop, models.DO_NOTHING, db_column='id_bus_stop_start')
    id_bus_stop_end = models.ForeignKey(BusStop, models.DO_NOTHING,
                                        db_column='id_bus_stop_end', related_name='searchhistory_id_bus_stop_end_set')
    id_client = models.ForeignKey(Client, models.DO_NOTHING, db_column='id_client')

    class Meta:
        managed = False
        db_table = 'search_history'


class Simulation(models.Model):
    current_location = models.DecimalField(max_digits=8, decimal_places=0)
    id_vehicle = models.DecimalField(max_digits=4, decimal_places=0)
    id_user = models.DecimalField(max_digits=4, decimal_places=0)
    number_free_seat = models.DecimalField(max_digits=4, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'simulation'


class Tickets(models.Model):
    id_tickets = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    name = models.CharField(max_length=30)
    duration_time = models.DecimalField(max_digits=4, decimal_places=0)
    price = models.DecimalField(max_digits=4, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'tickets'


class TicketsClient(models.Model):
    id_tickes_client = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    time_to_end = models.DateTimeField()
    client_id_client = models.ForeignKey(Client, models.DO_NOTHING, db_column='client_id_client')
    tickets_id_tickets = models.ForeignKey(Tickets, models.DO_NOTHING, db_column='tickets_id_tickets')

    class Meta:
        managed = False
        db_table = 'tickets_client'


class TravRide(models.Model):
    id_trav_ride = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    id_traveler = models.OneToOneField('Traveler', models.DO_NOTHING, db_column='id_traveler')
    id_course = models.ForeignKey(Course, models.DO_NOTHING, db_column='id_course', blank=True, null=True)
    id_course_stage_start = models.ForeignKey(CourseStage, models.DO_NOTHING, db_column='id_course_stage_start')
    id_course_stage_end = models.ForeignKey(CourseStage, models.DO_NOTHING, db_column='id_course_stage_end',
                                            related_name='travride_id_course_stage_end_set')
    id_bus_stop_start = models.ForeignKey(BusStop, models.DO_NOTHING, db_column='id_bus_stop_start')
    id_bus_stop_end = models.ForeignKey(BusStop, models.DO_NOTHING,
                                        db_column='id_bus_stop_end', related_name='travride_id_bus_stop_end_set')

    class Meta:
        managed = False
        db_table = 'trav_ride'


class Traveler(models.Model):
    id_traveler = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField()
    client_id_client = models.ForeignKey(Client, models.DO_NOTHING, db_column='client_id_client')
    id_bus_stop_start = models.ForeignKey(BusStop, models.DO_NOTHING, db_column='id_bus_stop_start')
    id_bus_stop_end = models.ForeignKey(BusStop, models.DO_NOTHING,
                                        db_column='id_bus_stop_end', related_name='traveler_id_bus_stop_end_set')

    class Meta:
        managed = False
        db_table = 'traveler'


class CustomUserManager(BaseUserManager):
    def create_user(self, id_user, role, first_name, last_name, phone_number, email, username, home_address,
                    password, **extra_fields):
        """
        Tworzy i zapisuje użytkownika z podanymi danymi.
        """
        if not email:
            raise ValueError('Email użytkownika musi być ustawiony.')

        user = self.model(
            id_user=id_user,
            role=role,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=self.normalize_email(email),
            username=username,
            home_address=home_address,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id_user, role, first_name, last_name, phone_number, email, username, home_address,
                         password, **extra_fields):
        """
        Tworzy i zapisuje superużytkownika (administratora) z podanymi danymi.
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superużytkownik musi mieć is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superużytkownik musi mieć is_staff=True.')

        return self.create_user(id_user, role, first_name, last_name, phone_number, email, username, home_address,
                                password, **extra_fields)


class User(AbstractUser):
    id_user = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    role = models.CharField(max_length=30)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.DecimalField(max_digits=12, decimal_places=0)
    email = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    home_address = models.CharField(max_length=200)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField()

    objects = CustomUserManager()

    class Meta:
        managed = False
        db_table = 'user'


class VehFeature(models.Model):
    id_feature = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    name = models.CharField(max_length=100)
    content = models.CharField(max_length=100)

    objects = CustomUserManager()

    class Meta:
        managed = False
        db_table = 'veh_feature'


class VehFeatureTraveler(models.Model):
    id_veh_feature_traveler = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    id_feature = models.ForeignKey(VehFeature, models.DO_NOTHING, db_column='id_feature')
    id_traveler = models.ForeignKey(Traveler, models.DO_NOTHING, db_column='id_traveler')

    class Meta:
        managed = False
        db_table = 'veh_feature_traveler'


class Vehicle(models.Model):
    id_vehicle = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    nr_vehicle = models.DecimalField(max_digits=4, decimal_places=0)
    model = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    date_purchase = models.DateField()
    date_inspection = models.DateField()
    max_number_passengers = models.DecimalField(max_digits=2, decimal_places=0)
    battery_kwh = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    cons_kwh = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehicle'


class VehicleVehFeature(models.Model):
    id_vehicle_veh_feature = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    id_vehicle = models.ForeignKey(Vehicle, models.DO_NOTHING, db_column='id_vehicle')
    id_feature = models.ForeignKey(VehFeature, models.DO_NOTHING, db_column='id_feature')

    class Meta:
        managed = False
        db_table = 'vehicle_veh_feature'


class WorkSchedule(models.Model):
    id_work_shedule = models.DecimalField(primary_key=True, max_digits=4, decimal_places=0)
    id_course = models.DecimalField(max_digits=4, decimal_places=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    id_driver = models.ForeignKey(Driver, models.DO_NOTHING, db_column='id_driver')

    class Meta:
        managed = False
        db_table = 'work_schedule'



