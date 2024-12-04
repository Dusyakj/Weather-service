import requests

API_KEY = 'imkYUoZylfEk7lcDNVfGZnzwwEfT5Rgo'

def get_location_key(city_name, api_key):
    url = 'http://dataservice.accuweather.com/locations/v1/cities/search'
    params = {
        'apikey': api_key,
        'q': city_name,
        'language': 'ru-ru',
        'details': 'false',
        'offset': '0',
        'limit': '1'
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data:
            return [True,data[0]['Key']]
        else:
            return [None,'Город не найден.']
    else:
        return [None,f'Ошибка при поиске города: {response.status_code}']

def get_hourly_forecast(location_key, api_key):


    url = f'https://dataservice.accuweather.com/forecasts/v1/hourly/{"1hour"}/{location_key}'
    params = {
        'apikey': api_key,
        'language': 'ru-ru',
        'details': 'true',
        'metric': 'true'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data:
            return [True,data]
        else:
            return [None,'Прогноз погоды недоступен.']
    except Exception as err:
        return [None, err]


def main(city):
    location_key = get_location_key(city, API_KEY)
    if location_key[0]:
        forecast = get_hourly_forecast(location_key[1], API_KEY)
        if forecast[0]:
            current = forecast[1][0]
            temp = current.get('Temperature', {}).get('Value')
            humidity = current.get('RelativeHumidity')
            wind_speed = current.get('Wind', {}).get('Speed', {}).get('Value')
            precipitation_prob = current.get('PrecipitationProbability')

            data = {
                'Город': city,
                'Температура': temp,
                'Влажность': humidity,
                'Скорость ветра': wind_speed,
                'Вероятность дождя': precipitation_prob
            }
            return [True, check_bad_weather(data)]
        else: return forecast
    else:
        return location_key

def check_bad_weather(data):
    if data['Температура'] > 30 or data['Температура'] < 0 \
        or data['Вероятность дождя'] > 80 or data['Скорость ветра'] > 30:
        data['Статус'] = 'Ой-ой, погода плохая'
        return data
    else:
        data['Статус'] = 'Погода — супер'
        return data