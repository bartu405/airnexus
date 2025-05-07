
import string
import random
from traceback import print_tb
from unicodedata import name
from urllib import request
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.http import JsonResponse
import json
from amadeus import Client, ResponseError, Location
from django.core.paginator import Paginator
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import ast


def timeReverse(value):
    list = value.split('-')
    list.reverse()
    new_value = list[0] + "-" + list[1] + "-" + list[2]
    return new_value


def index(request):

    amadeus = Client(
        client_id='zOx1FXJgfvWwkpNZgHYkU0vckUC9X3LP',
        client_secret='ulH6gowVlW321vOY'
    )

    if 'term' in request.GET:
        try:
            data = amadeus.reference_data.locations.get(
                keyword=request.GET.get('term', None), subType=Location.ANY).data
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)

        return HttpResponse(get_city_airport_list(data))

    return render(request, "travel/index.html")


def login_page(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, 'travel/login.html', {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "travel/login.html")


def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_page(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "travel/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "travel/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "travel/register.html")


def about(request):
    return render(request, 'travel/about.html')


@csrf_exempt
def profile(request, profile_name):

    if request.method == 'POST':
        email = request.POST["email"]
        username = request.user.username
        user = User.objects.get(username=username)
        user.email = email
        user.save()
        return HttpResponseRedirect(reverse('profile', kwargs={'profile_name': username}))

    if request.user.is_authenticated:

        requested_path = request.path
        requested_path = requested_path.replace("/", "")

        if not requested_path == request.user.username:
            return render(request, "travel/404.html")

        profile_name = request.user.username

        email = False
        profile_email = ""

        if request.user.email:
            profile_email = request.user.email
            email = True

        return render(request, "travel/profile.html", {
            "profile_name": profile_name,
            "email": email,
            "profile_email": profile_email,
        })
    else:
        return render(request, "travel/404.html")


def error(request, wrong_path):
    return render(request, "travel/404.html")


# BIGGEST NOTES : In input type="text", also put name="something". You will get the value from the post request in that request.POST["something"]
@csrf_exempt
def air(request):

    if request.method == 'POST':

        origin = request.POST["origin"]
        destination = request.POST["destination"]

        depart_date = request.POST["depart"]
        return_date = ""

        if 'return' in request.POST:
            return_date = request.POST["return"]

        amadeus = Client(
            client_id='zOx1FXJgfvWwkpNZgHYkU0vckUC9X3LP',
            client_secret='ulH6gowVlW321vOY'
        )

        if return_date == "":

            try:
                response = amadeus.shopping.flight_offers_search.get(
                    originLocationCode=origin[:3],
                    destinationLocationCode=destination[:3],
                    departureDate=depart_date,
                    adults=1,
                    currencyCode='USD',
                )

                # print(response) # this outputs an object
                # dir() gives all attributes of an OBJECT like "response", such as response.data, response.body, response.header...
                # response.data only gives "data" part of json
                # response.body gives "meta", "data", "dictionaries" parts as string
                # attribute = dir(response)
                # print(attribute)

                # we convert response.body string to dictionary(json) data
                bro = response.body
                bro = json.loads(bro)

                if bro["meta"]["count"] == 0:
                    offers = []
                    airlines = ""
                    planes = ""
                    origin = ""
                    destination = ""
                    depart_date = ""
                    return_date = ""

                else:
                    # print(bro['dictionaries'])

                    airlines = bro['dictionaries']['carriers']
                    planes = bro['dictionaries']['aircraft']

                    # print(airlines)

                    offers = []

                    for data in response.data:  # hepsi bi flight offer
                        offers.append(data)

            except ResponseError as error:
                print(error)

                offers = []
                airlines = ""
                planes = ""
                origin = ""
                destination = ""
                depart_date = ""
                return_date = ""
        else:
            try:
                response = amadeus.shopping.flight_offers_search.get(
                    originLocationCode=origin[:3],
                    destinationLocationCode=destination[:3],
                    departureDate=depart_date,
                    returnDate=return_date,
                    adults=1,
                    currencyCode='USD',
                )

                # print(response) # this outputs an object
                # dir() gives all attributes of an OBJECT like "response", such as response.data, response.body, response.header...
                # response.data only gives "data" part of json
                # response.body gives "meta", "data", "dictionaries" parts as string
                # attribute = dir(response)
                # print(attribute)

                # we convert response.body string to dictionary(json) data
                bro = response.body
                bro = json.loads(bro)
                # print(bro)

                if bro["meta"]["count"] == 0:
                    offers = []
                    airlines = ""
                    planes = ""
                    origin = ""
                    destination = ""
                    depart_date = ""
                    return_date = ""
                else:
                    # print(bro['dictionaries'])

                    airlines = bro['dictionaries']['carriers']
                    planes = bro['dictionaries']['aircraft']

                    # print(airlines)

                    offers = []

                    for data in response.data:  # hepsi bi flight offer
                        offers.append(data)

            except ResponseError as error:

                print(error)
                offers = []
                airlines = ""
                planes = ""
                origin = ""
                destination = ""
                depart_date = ""
                return_date = ""

        request.session['offers'] = offers
        request.session['origin'] = origin
        request.session["destination"] = destination
        request.session["airlines"] = airlines
        request.session["planes"] = planes
        request.session["depart_date"] = depart_date
        request.session["return_date"] = return_date

        return HttpResponseRedirect(reverse('flight'))  # Redirect after POST

    return False


def details(request):
    if request.method == 'POST':

        request.session['booking_flight'] = request.POST['flight']

        request.session['name'] = request.POST['name']
        request.session['last_name'] = request.POST['last-name']
        request.session['date'] = request.POST['date']
        request.session['email'] = request.POST['email']
        request.session['phone'] = request.POST['phone']
        request.session['nationality'] = request.POST['nationality']

        return HttpResponseRedirect(reverse('booked'))


def generate_random_pnr(length=6):
    characters = string.ascii_uppercase + string.digits
    pnr = ''.join(random.choice(characters) for _ in range(length))

    # Keep generating a new PNR number until a unique one is found
    while Booking.objects.filter(pnr_number=pnr).exists():
        pnr = ''.join(random.choice(characters) for _ in range(length))

    return pnr


@ login_required(login_url='/login')
def bookings(request):
    user = request.user

    bookings = Booking.objects.filter(customer=user).distinct()


def bookings(request):
    bookings = Booking.objects.prefetch_related('flights')
    for booking in bookings:
        booking.has_return_flights = booking.flights.filter(
            flight_type='return').exists()

    return render(request, 'travel/bookings.html', {'bookings': bookings})


def booked(request):
    flight = request.session.get('booking_flight')
    name = request.session.get('name')
    last_name = request.session.get('last_name')
    date = request.session.get('date')
    email = request.session.get('email')
    phone = request.session.get('phone')
    nationality = request.session.get('nationality')

    flight = ast.literal_eval(flight)

    oneWay = True
    departure_flight_stops = 0
    return_flight_stops = 0

    if len(flight['itineraries']) == 2:
        oneWay = False  # if 2, it is return

    # Check if the booking already exists
    booking = Booking.objects.filter(
        customer=request.user, booking_time=datetime.now()).first()

    if not booking:
        # Create a new booking if it doesn't exist
        booking = Booking(customer=request.user, booking_time=datetime.now())
        booking.save()

        stops = 0
        if oneWay:
            stops = len(flight['itineraries'][0]['segments']) - 1
            for i in range(stops + 1):  # stops + 1 tane uçuş var
                # Add flight segment logic for one-way journey
                new_airport = Airport.objects.create(
                    iataCode=flight['itineraries'][0]['segments'][i]['departure']['iataCode'])
                new_date = flight['itineraries'][0]['segments'][i]['departure']['at']

                arrival_airport = Airport.objects.create(
                    iataCode=flight['itineraries'][0]['segments'][i]['arrival']['iataCode'])
                arrive_date = flight['itineraries'][0]['segments'][i]['arrival']['at']

                new_flight = Flight.objects.create(
                    origin=new_airport,
                    destination=arrival_airport,
                    departure_date=new_date,
                    arrival_date=arrive_date,
                    duration=flight['itineraries'][0]['segments'][i]['duration'],
                    flight_type="departure"  # Set flight type to "departure"
                )
                new_flight.save()
                booking.flights.add(new_flight)
        else:
            departure_flight_stops = len(
                flight['itineraries'][0]['segments']) - 1
            return_flight_stops = len(flight['itineraries'][1]['segments']) - 1
            # Add flights for the departure journey
            for i in range(departure_flight_stops + 1):
                # Add flight segment logic for departure journey
                new_airport = Airport.objects.create(
                    iataCode=flight['itineraries'][0]['segments'][i]['departure']['iataCode'])
                new_date = flight['itineraries'][0]['segments'][i]['departure']['at']

                arrival_airport = Airport.objects.create(
                    iataCode=flight['itineraries'][0]['segments'][i]['arrival']['iataCode'])
                arrive_date = flight['itineraries'][0]['segments'][i]['arrival']['at']

                new_flight = Flight.objects.create(
                    origin=new_airport,
                    destination=arrival_airport,
                    departure_date=new_date,
                    arrival_date=arrive_date,
                    duration=flight['itineraries'][0]['segments'][i]['duration'],
                    flight_type="departure"  # Set flight type to "departure"
                )
                new_flight.save()
                booking.flights.add(new_flight)
            # Add flights for the return journey
            for i in range(return_flight_stops + 1):
                # Add flight segment logic for return journey
                new_airport = Airport.objects.create(
                    iataCode=flight['itineraries'][1]['segments'][i]['departure']['iataCode'])
                new_date = flight['itineraries'][1]['segments'][i]['departure']['at']

                arrival_airport = Airport.objects.create(
                    iataCode=flight['itineraries'][1]['segments'][i]['arrival']['iataCode'])
                arrive_date = flight['itineraries'][1]['segments'][i]['arrival']['at']

                new_flight = Flight.objects.create(
                    origin=new_airport,
                    destination=arrival_airport,
                    departure_date=new_date,
                    arrival_date=arrive_date,
                    duration=flight['itineraries'][1]['segments'][i]['duration'],
                    flight_type="return"  # Set flight type to "return"
                )
                new_flight.save()
                booking.flights.add(new_flight)

        booking.save()

        # Generate a unique PNR number for the new booking
        pnr = generate_random_pnr()
        booking.pnr_number = pnr
        booking.save()

    passenger_info = {
        'name': name,
        'last_name': last_name,
        'date': date,
        'email': email,
        'phone': phone,
        'nationality': nationality
    }

    return render(request, 'travel/booked.html', {
        "flight": flight,
        "oneWay": oneWay,
        "stops": stops,
        "departure_flight_stops": departure_flight_stops,
        "return_flight_stops": return_flight_stops,
        "passenger_info": passenger_info,
        "pnr_number": booking.pnr_number
    })


def flight(request):

    depart_date = request.session.get('depart_date')
    return_date = request.session.get('return_date')
    offering = request.session.get('offers')
    origin = request.session.get('origin')
    destination = request.session.get('destination')
    airlines = request.session.get('airlines')
    planes = request.session.get('planes')

    paginator = Paginator(offering, 10)  # Show 25 flights per page.
    page_number = request.GET.get('page')
    bro = paginator.get_page(page_number)

    next = False
    if len(offering) > 10:
        next = True

    for flight in offering:

        for itinerary in flight["itineraries"]:
            stops = -1
            for segment in itinerary["segments"]:

                # stops
                stops += 1

                if stops == 0:
                    segment["numberOfStops"] = "Direct"
                else:
                    segment["numberOfStops"] = f'Stops: {stops}'

                # airlines

                carrierCode = segment['carrierCode']
                new_airline = airlines[carrierCode]
                # edit the json, add an 'airline': airline section, use it in template
                segment['airline'] = new_airline

                # planes
                aircraftCode = segment['aircraft']['code']
                new_plane = planes[aircraftCode]
                segment['plane'] = new_plane

    oneWay = True

    if return_date:
        oneWay = False

    thereAreNoFlights = False

    if len(offering) == 0:
        thereAreNoFlights = True

    return render(request, 'travel/flight.html', {
        "offers": bro,
        "origin": origin,
        "destination": destination,
        "depart_date": depart_date,
        "return_date": return_date,
        "oneWay": oneWay,
        "thereAreNoFlights": thereAreNoFlights,
        "next": next,
    })


def get_city_airport_list(data):
    list = []

    for i, val in enumerate(data):

        result = {}

        bro = data[i]['iataCode'] + ", " + data[i]['name']
        bty = data[i]['address']['cityName'] + \
            ', ' + data[i]['address']['countryName']
        result["value"] = bro
        result["label"] = bro
        result["desc"] = bty

        list.append(result)

    return json.dumps(list)


@ csrf_exempt
@ login_required(login_url='/login')
def cs(request):

    if request.method == 'POST':

        # this is string
        flight = request.POST['flight']

        # don't do json.dumps() or json.loads(), nedense bozuyor
        json_data = ast.literal_eval(flight)

        # for flight create orders
        request.session['flight'] = json_data

        # numberOfBookableSeats = json_data['numberOfBookableSeats']

        count = 0

        for i in json_data['itineraries']:
            for segment in i['segments']:
                count += 1

        direct = True
        if count > 1:
            direct = False

        stops1 = False
        if count == 2:
            stops1 = True

        stops2 = False
        if count == 3:
            stops2 = True

        depart_date = request.session.get('depart_date')
        return_date = request.session.get('return_date')

        oneWay = True
        if return_date:
            oneWay = False

        return render(request, 'travel/cs.html', {
            'flight': json_data,
            'direct': direct,
            'count': count,
            'stops1': stops1,
            'stops2': stops2,
            'depart_date': depart_date,
            'return_date': return_date,
            'oneWay': oneWay
        })

    return render(request, 'travel/cs.html')
