import requests as reqs


def get_weather(opemweatherapp_api_key, city, units='standard'):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city.lower()}&appid={opemweatherapp_api_key}&units={units}"

    response = reqs.get(url)

    if response.status_code == 200:

        data = response.json()

        return {
            'success': True,
            'weather': {
                'weather': ', '.join([weather['main'] for weather in data['weather']]),
                'temperature': data['main']['temp'],
                'pressure': data['main']['pressure'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
        }

    if response.status_code == 401:

        return {
            'success': False,
            'error': "Invalid API key for OpenWeatherApp"
        }

    if response.status_code == 404:

        return {
            'success': False,
            'error': f"Invalid city name \"{city.title()}\""
        }

    return {
        'success': False,
        'error': "unknown error"
    }
