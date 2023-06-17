import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import json
from django.http import JsonResponse, HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm
from mainContent.models import User, TicketsClient
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.conf import settings

from datetime import datetime, timedelta

from .models import ClientBusStop
from .forms import RaportForm
from .models import RaportsUnlogged


def index(request):
    if request.user.is_authenticated:
        return render(request, 'transit_go_logged.html')
    else:
        return render(request, 'base.html')


def registration(request):
    return render(request, "registration.html")


def remind(request):
    return render(request, "remind.html")


@login_required(login_url='login')
def transit_go_base_logged(request):
    return render(request, "transit_go_logged.html")


@login_required(login_url='login')
def user_profile(request):
    return render(request, "user_profile.html")


@login_required(login_url='login')
def tickets(request):

    return render(request, "tickets.html")


@login_required(login_url='login')
def trip_history(request):
    return render(request, "trip_history.html")


@login_required(login_url='login')
def contact_us_logged(request):
    return render(request, "contact_us_logged.html")


def add_month(date):
    date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
    next_month = date_obj + timedelta(days=30)
    return next_month.strftime("%d-%m-%Y")


@login_required(login_url='login')
def buy_tickets(request):
    current_user = int(request.user.pk)

    if request.method == 'POST':
        ticketsList = requests.get('http://127.0.0.1:8000/api/TicketsClient/?client_id_client={}'.format(current_user))
        ticketsListJSON = ticketsList.json()

        if 'buy_jednorazowy' in request.POST:
            data = {
                "id_tickes_client": "",
                "time_to_end": "1000-01-01T15:00:00+01:00",
                "client_id_client": current_user,
                "tickets_id_tickets": 2
            }

            liczba_biletow_jednorazowych = sum(ticket['tickets_id_tickets'] == 2 for ticket in ticketsListJSON)

            max_of_id = 0
            for obj in ticketsListJSON:
                if int(obj['id_tickes_client']) > max_of_id:
                    max_of_id = int(obj['id_tickes_client'])

            data['id_tickes_client'] = str(max_of_id + 1)

            response = requests.post('http://127.0.0.1:8000/api/TicketsClient/', json=data)
            if response.status_code == 201:
                pass
            else:
                pass

        elif 'buy_monthly_ticket' in request.POST:
            monthly_ticket = next((ticket for ticket in ticketsListJSON if ticket['tickets_id_tickets'] == 1), None)
            if monthly_ticket:
                current_date = monthly_ticket['time_to_end']
                next_month = add_month(current_date)
                monthly_ticket['time_to_end'] = next_month
                response = requests.put('http://127.0.0.1:8000/api/TicketsClient/{}/'.format(monthly_ticket['id_tickes_client']), json=monthly_ticket)
                if response.status_code == 200:
                    pass
                else:
                    pass

    ticketsList = requests.get('http://127.0.0.1:8000/api/TicketsClient/?client_id_client={}'.format(current_user))
    ticketsListJSON = ticketsList.json()

    liczba_biletow_jednorazowych = sum(ticket['tickets_id_tickets'] == 2 for ticket in ticketsListJSON)

    monthly_ticket = next((ticket for ticket in ticketsListJSON if ticket['tickets_id_tickets'] == 1), None)
    monthly_ticket_date = add_month(monthly_ticket['time_to_end']) if monthly_ticket else None

    return render(request, "buy_tickets.html",
                  {'ticketsList': ticketsListJSON, 'liczba_biletow_jednorazowych': liczba_biletow_jednorazowych,
                   'monthly_ticket_date': monthly_ticket_date})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')
            if new_password1 == new_password2:
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Twoje hasło zostało pomyślnie zmienione.')
                return redirect('user_profile')
            else:
                messages.error(request, 'Hasła nie są identyczne.')
        else:
            print(form.errors)
            messages.error(request, 'Hasło nie spełnia wymagań.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})


@login_required(login_url='login')
def favorite_bus_stop(request):
    rekordy = ClientBusStop.objects.all()
    busStopsList = requests.get(f'{settings.API_BASE_URL}BusStop/')
    przystanki = busStopsList.json()

    if request.method == 'POST':
        # Pobieranie danych z formularza
        nameOfFavPlace = request.POST.get('nameOfFavPlace')
        id_bus_stop = request.POST.get('przystanki')
        current_user = int(request.user.pk)

        # Tworzenie danych do wysłania w formacie JSON
        data_from_raport = {
            "id_fav_place": '300',
            "name": nameOfFavPlace,
            "id_bus_stop": id_bus_stop,
            "id_client":  current_user
        }

        data = requests.get(f'{settings.API_BASE_URL}ClientBusStop/')
        clientBusStopJson = data.json()
        max_of_id = 0
        for obj in clientBusStopJson:
            if int(obj['id_fav_place']) > max_of_id:
                max_of_id = int(obj['id_fav_place'])

        data_from_raport['id_fav_place'] = str(max_of_id + 1)

        json_data = json.dumps(data_from_raport)

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(f'{settings.API_BASE_URL}ClientBusStop/', data=json_data, headers=headers)

    return render(request, "favorite_BusStop.html", {'rekordy': rekordy, 'przystanki': przystanki})



def report(request):
    return render(request, "report.html")


def remind_send_mail(request):
    return render(request, "remind_send_mail.html")


def report_unlogged(request):
    if request.method == "POST":
        form = RaportForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "report_unlogged_status.html")
    else:
        form = RaportForm()
    return render(request, "report_unlogged.html", {'form': form})


def regulations(request):
    return render(request, "regulations.html")


def privacy(request):
    return render(request, "privacy.html")


def about_us(request):
    return render(request, "about_us.html")


def users(request):
    response = requests.get('http://localhost:8000/api/user/')
    data = response.json()

    # # Tworzenie użytkownika
    # user = User.objects.create_user(
    #     id_user=13,
    #     role='user',
    #     first_name='John',
    #     last_name='Doe',
    #     phone_number='123456789',
    #     email='example@example.com',
    #     username='johndoe',
    #     home_address='123 Street',
    #     password='password123',
    #     last_login=timezone.now(),
    #     date_joined=timezone.now()
    # )
    #
    # # Tworzenie superużytkownika
    # superuser = User.objects.create_superuser(
    #     id_user=12,
    #     role='admin',
    #     first_name='Admin',
    #     last_name='User',
    #     phone_number='987654321',
    #     email='admin@example.com',
    #     username='adminuser',
    #     home_address='456 Avenue',
    #     password='adminpassword!',
    #     last_login=timezone.now(),
    #     date_joined=timezone.now()
    # )
    # Pobieranie rekordów z tabeli 'client'

    headers = {
        "Content-Type": "application/json"
    }

    client_data = requests.get('http://localhost:8000/api/Client/')
    clients_json = client_data.json()

    max_client_id = 0
    for obj in clients_json:
        if int(obj['id_client']) > max_client_id:
            max_client_id = int(obj['id_client'])

    # Tworzenie rekordu w tabeli 'client' za pomocą API
    client_data = {
        "id_client": str(max_client_id + 1),
        "user_id_user": 13
    }
    client_response = requests.post('http://localhost:8000/api/Client/', data=json.dumps(client_data), headers=headers)
    if client_response.status_code != 201:
        # Obsłuż błąd tworzenia rekordu w tabeli 'client'
        return render(request, 'register.html', {'error': 'Błąd podczas tworzenia rekordu w tabeli client'})

    return render(request, 'users.html', {'data': data})


def encrypt_passwords(request):
    # Pobierz wszystkich użytkowników
    users = User.objects.all()

    # Zaszyfruj hasło dla każdego użytkownika
    for user in users:
        user.password = make_password(user.password)
        user.save()

    return HttpResponse("Hasła zostały zaszyfrowane.")


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('TransitGoLogged')
            else:
                return render(request, 'login.html', {'error': 'Nieprawidłowe dane'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        # Pobieranie danych z formularza
        role = request.POST.get('role')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('e_mail')
        username = request.POST.get('username')
        home_address = request.POST.get('home_address')
        password = request.POST.get('password')

        # Tworzenie danych do wysłania w formacie JSON
        data_from_raport = {
            "id_user": '1000',
            "role": role,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "email": email,
            "username": username,
            "home_address": home_address,
            "password": make_password(password),
            "last_login": timezone.now().isoformat(),
            "is_superuser": False,
            "is_staff": False,
            "is_active": True,
            "date_joined": timezone.now().isoformat()
        }

        data = requests.get(f'{settings.API_BASE_URL}user/')
        users_json = data.json()

        max_of_id = 0
        for obj in users_json:
            if int(obj['id_user']) > max_of_id:
                max_of_id = int(obj['id_user'])

        data_from_raport['id_user'] = str(max_of_id + 1)
        if role == 'Klient':
            data_from_raport['role'] = 'client'
        else:
            data_from_raport['role'] = 'driver'

        json_data = json.dumps(data_from_raport)

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(f'{settings.API_BASE_URL}user/', data=json_data, headers=headers)

        if response.status_code == 201:
            if role == 'client':
                # Pobieranie rekordów z tabeli 'client'
                client_data = requests.get(f'{settings.API_BASE_URL}Client/')
                clients_json = client_data.json()

                max_client_id = 0
                for obj in clients_json:
                    if int(obj['id_client']) > max_client_id:
                        max_client_id = int(obj['id_client'])

                # Tworzenie rekordu w tabeli 'client' za pomocą API
                client_data = {
                    "id_client": str(max_client_id + 1),
                    "user_id_user": data_from_raport['id_user']
                }
                headers = {
                    "Content-Type": "application/json"
                }

                client_response = requests.post(f'{settings.API_BASE_URL}/Client/', data=json.dumps(client_data), headers=headers)
                if client_response.status_code != 201:
                    # Obsłuż błąd tworzenia rekordu w tabeli 'client'
                    return render(request, 'register.html', {'error': 'Błąd podczas tworzenia rekordu w tabeli client'})
            return redirect('login')

        # dane nie zgadzają się, wyświetlamy błąd
        return render(request, 'register.html', {'error': 'Nieprawidłowe dane'})

    # GET request, zwracamy pusty formularz
    return render(request, 'register.html')


@login_required(login_url='login')
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        # Odczytaj dane z formularza
        user = request.user
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        home_address = request.POST['home_address']

        # Zaktualizuj dane użytkownika
        user.username = username
        #user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.email = email
        user.home_address = home_address

        user.save()
        # Przekierowanie do profilu po zapisaniu zmian
        return redirect('user_profile')

    context = {
        'user': user
    }
    return render(request, 'edit_profile.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, "Logged out successfully!")
        return redirect('base')


def reset_password(request):
    # Kod obsługujący żądanie resetowania hasła
    return render(request, 'reset_password.html')


def password_reset_done(request):
    # Kod obsługujący żądanie po wysłaniu linka do resetowania hasła
    return render(request, 'password_reset_done.html')


def reset_password_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Twoje hasło zostało pomyślnie zresetowane.')
                return redirect('login')
            else:
                messages.error(request, 'Wystąpił błąd podczas resetowania hasła.')
        else:
            form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'Link resetujący hasło jest nieprawidłowy.')
        return redirect('reset_password')


def password_reset_complete(request):
    # Kod obsługujący żądanie po zresetowaniu hasła
    return render(request, 'password_reset_complete.html')

  
def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Zaimplementuj tutaj kod obsługujący wysłanie wiadomości

        return render(request, 'contact_us.html', {'success': True})
    else:
        return render(request, 'contact_us.html', {'success': False})


def get_api_base_url(request):
    return JsonResponse({'api_base_url': settings.API_BASE_URL})
