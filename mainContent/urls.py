from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from . import views, api_views
from mainContent.views import encrypt_passwords
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

router = DefaultRouter()
router.register(r'BusStop', api_views.BusStopViewSet)
router.register(r'BusStopsDist', api_views.BusStopsDistViewSet)
router.register(r'BusStopsTime', api_views.BusStopsTimeViewSet)
router.register(r'Course', api_views.CourseViewSet)
router.register(r'CourseStage', api_views.CourseStageViewSet)
router.register(r'Client', api_views.ClientViewSet)
router.register(r'ClientBusStop', api_views.ClientBusStopViewSet)
router.register(r'Driver', api_views.DriverViewSet)
router.register(r'DriverVehicle', api_views.DriverVehicleViewSet)
router.register(r'Opinion', api_views.OpinionViewSet)
router.register(r'Raports', api_views.RaportsViewSet)
# =router.register(r'Simulation', api_views.SimulationViewSet)
router.register(r'SearchHistory', api_views.SearchHistoryViewSet)
router.register(r'Tickets', api_views.TicketsViewSet)
router.register(r'TicketsClient', api_views.TicketsClientViewSet)
router.register(r'Traveler', api_views.TravelerViewSet)
router.register(r'TravRide', api_views.TravRideViewSet)
router.register(r'user', api_views.UserViewSet)
router.register(r'VehicleVehFeature', api_views.VehicleVehFeatureViewSet)
router.register(r'Vehicle', api_views.VehicleViewSet)
router.register(r'VehFeatureTraveler', api_views.VehFeatureTravelerViewSet)
router.register(r'VehFeature', api_views.VehFeatureViewSet)
router.register(r'WorkSchedule', api_views.WorkScheduleViewSet)

router.register(r'Client/(?P<client_id>\d+)/client_bus_stop', api_views.ClientBusStopFromClientViewSet,
                basename='client-bus-stop-from-client')
router.register(r'user/(?P<user_id>\d+)/client_bus_stop', api_views.UserBusStopFromClientViewSet,
                basename='user-bus-stop-from-client')
router.register(r'user/(?P<user_id>\d+)/traveler', api_views.TravelerFromClientViewSet,
                basename='traveler-from-user')

urlpatterns = [
    path('api/', include(router.urls)),
    path('login/', views.login_view, name='login'),
    # path('users/', views.users, name='users'),
    path('register/', views.register, name='register'),
    path('remind/', views.remind, name='remind'),
    path('TransitGoLogged/', views.transit_go_base_logged, name='TransitGoLogged'),
    path('encrypt-passwords/', encrypt_passwords, name='encrypt_passwords'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('tickets/', views.tickets, name='tickets'),
    path('trip_history/', views.trip_history, name='trip_history'),
    path('change_password/', views.change_password, name='change_password'),
    path('contact_us_logged/', views.contact_us_logged, name='contact_us_logged'),
    path('buy_tickets/', views.buy_tickets, name='buy_tickets'),

    path('favorite_BusStop/', views.favorite_bus_stop, name='favorite_BusStop'),
    path('api/user/<int:user_id>/', include(router.urls)),
    path('report/', views.report, name='report'),
    path('remind_send_mail/', views.remind_send_mail, name='remind_send_mail'),
    path('report_unlogged/', views.report_unlogged, name='report_unlogged'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('regulations/', views.regulations, name='regulations'),
    path('privacy/', views.privacy, name='privacy'),
    path('about_us/', views.about_us, name='about_us'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = 'reset_password.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = 'password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'password_reset_complete.html'), name='password_reset_complete'),
    path('', views.index, name='index'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('api/', views.get_api_base_url, name='api_base_url')
]
