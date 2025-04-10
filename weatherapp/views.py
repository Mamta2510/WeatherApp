from django.shortcuts import render
from django.contrib import messages
import requests
import datetime
import pytz

def home(request):
    API_Key_Weather = 'c9147186ddffffdad6f50f674ef31d4f'
    API_Key_Image = 'AIzaSyC6FC2fiKj9GRI8YUCb_a1-d51zfuTh3qo'
    SEARCH_ENGINE_ID = '26ed904f7f97b4926'
    
    city = request.POST.get('city', 'delhi')  # Default to 'delhi' if no city input
    
    # Weather API
    weather_url = f'https://api.openweathermap.org/data/2.5/weather'
    weather_params = {
        'q': city,
        'appid': API_Key_Weather,
        'units': 'metric'
    }

    # Image API
    query = f'{city} 1920x1080'
    search_url = 'https://www.googleapis.com/customsearch/v1'
    search_params = {
        'key': API_Key_Image,
        'cx': SEARCH_ENGINE_ID,
        'q': query,
        'searchType': 'image',
        'imgSize': 'xlarge',
        'num': 1,
        'start': 1
    }

    try:
        weather_data = requests.get(weather_url, params=weather_params).json()
        image_data = requests.get(search_url, params=search_params).json()

        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']

        tz = pytz.timezone('Asia/Kolkata')
        now = datetime.datetime.now(tz)
        day = now.strftime('%A, %B %d %Y | %I:%M %p')

        image_url = image_data.get("items", [{}])[0].get("link", "")

        context = {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'image_url': image_url,
            'exception_occured': False
        }

    except Exception as e:
        messages.error(request, 'Weather or image data could not be retrieved.')
        context = {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 40,
            'day': datetime.date.today(),
            'city': 'delhi',
            'image_url': '',
            'exception_occured': True
        }

    return render(request, 'index.html', context)
