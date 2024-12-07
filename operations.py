import requests
from datetime import datetime
from pytz import timezone
import pytz

API_KEY = 'imkYUoZylfEk7lcDNVfGZnzwwEfT5Rgo'
# API_KEY = 'drvtaUgPGgLfbF6ksvDAoWqq2f4xZh4h'
# API_KEY = 'hjDhBWSjUwRI0nGXLXW8e8UgNEEYj6JE'
# API_KEY = 'as2IxOP2D5thgJnMqjngnnVyTSYRTMLw'


def get_location_key(lat, lon, api_key):

    response = requests.get(f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={api_key}&q={lat}%2C%20{lon}")

    if response.status_code == 200:
        data = response.json()
        if data and 'Key' in data:
            return [True, data['Key']]
        else:
            return [None, 'Местоположение не найдено.']
    else:

        return [None, f'Ошибка при поиске местоположения: {response.status_code}']

def get_hourly_forecast(location_key, api_key):
        url = f'https://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{location_key}'
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
                return [True, data]
            else:
                return [None, 'Прогноз погоды недоступен.']
        except Exception as err:
            return [None, err]

def get_weather_at_time(forecast_data, target_time):
        closest_forecast = None
        min_diff = None

        for forecast in forecast_data:
            forecast_time_str = forecast.get('DateTime')
            if not forecast_time_str:
                continue
            try:
                forecast_dt = datetime.fromisoformat(forecast_time_str).replace(tzinfo=pytz.UTC)
            except ValueError:
                continue

            diff = abs((forecast_dt - target_time).total_seconds())
            if min_diff is None or diff < min_diff:
                min_diff = diff
                closest_forecast = forecast

        if closest_forecast:
            return [True, closest_forecast]
        else:
            return [None, 'Нет доступного прогноза на указанное время.']

def main(lat, lon, time_str):
        try:
            if len(time_str) == 16:
                time_str += ":00"
            target_time = datetime.fromisoformat(time_str)
            local_tz = timezone('Europe/Moscow')
            target_time = local_tz.localize(target_time).astimezone(pytz.UTC)
        except ValueError:
            return [None, 'Неверный формат времени.']

        location_key = get_location_key(lat, lon, API_KEY)
        if location_key[0]:
            forecast = get_hourly_forecast(location_key[1], API_KEY)
            if forecast[0]:
                weather_at_time = get_weather_at_time(forecast[1], target_time)
                if weather_at_time[0]:
                    current = weather_at_time[1]
                    temp = current.get('Temperature', {}).get('Value')
                    humidity = current.get('RelativeHumidity')
                    wind_speed = current.get('Wind', {}).get('Speed', {}).get('Value')
                    precipitation_prob = current.get('PrecipitationProbability')

                    data = {
                        'Координаты': f'({lat}, {lon})',
                        'Время': target_time.astimezone(local_tz).strftime('%Y-%m-%d %H:%M'),
                        'Температура': temp,
                        'Влажность': humidity,
                        'Скоростьветра': wind_speed,
                        'Вероятностьдождя': precipitation_prob
                    }
                    return [True, check_bad_weather(data)]
                else:
                    return weather_at_time
            else:
                return forecast
        else:
            return location_key

def check_bad_weather(data):
        if (data['Температура'] > 30 or data['Температура'] < 0
                or data['Вероятностьдождя'] > 80 or data['Скоростьветра'] > 30):
            data['Статус'] = 'Ой-ой, погода плохая'
        else:
            data['Статус'] = 'Погода — супер'
        return data

