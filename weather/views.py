from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm


def index(request):
    cities = City.objects.all()  # return all the cities in the database

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=e9ef56cf045664e04b0ca1b4b35a396e'

    weather_data = []

    for city in cities:
        city_weather = requests.get(url.format(city)).json()

        weather = {
            'city': city.name,
            'temperature': city_weather['main']['temp'],
            'humidity': city_weather['main']['humidity'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon'],
            'longitude': city_weather['coord']['lon'],
            'latitude': city_weather['coord']['lat'],
        }

        weather_data.append(weather)  # add the data for the current city into our list

    context = {'weather_data': weather_data}

    return render(request, 'weather/index.html', context)  # returns the index.html template


def add_city(request):

    err_msg = ''

    if request.method == 'POST':
        form = CityForm(request.POST)
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=e9ef56cf045664e04b0ca1b4b35a396e'

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city = City.objects.filter(name=new_city).count()

            if existing_city == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] != 200:
                    err_msg = 'City does not exist in the world.'
                else:
                    err_msg = 'City added successfully'
                    form.save()
            else:
                err_msg = 'City already exists in the database!'

    else:
        form = CityForm()

    context = {'form': form, 'err_msg': err_msg}
    return render(request, 'weather/add_city.html', context)



def remove_city(request):
    err_msg = ''
    if request.method == 'POST':
        form = request.POST['weather']
        City.objects.filter(name=form).delete()
        err_msg = 'City deleted successfully!!'
    else:
        err_msg = 'Please fill the form!!'

    cities = City.objects.all()  # return all the cities in the database
    weather_data = []

    for city in cities:
        c_n = city.name
        weather_data.append(c_n)  # add the data for the current city into our list

    context = {'weather_data': weather_data, 'err_msg': err_msg}

    return render(request, 'weather/remove_city.html', context)



