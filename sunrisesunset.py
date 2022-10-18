"""Return sunrise or sunset time"""
import urllib.request
import json
import datetime
import pytz
from dateutil import tz
from errbot import BotPlugin, botcmd, arg_botcmd, re_botcmd


class SunriseSunset(BotPlugin):
    """Return sunrise or sunset time"""

    @arg_botcmd('--latitude', dest='latitude', type=str, default='39.7392')
    @arg_botcmd('--longitude', dest='longitude', type=str, default='-104.9903')
    @arg_botcmd('--city', dest='city', type=str, default=None)
    def sunrise(self, msg, latitude, longitude, city):
        """Return next sunrise"""
        if city is None:
            return self.sun_send(msg, latitude, longitude, {'sunrise': True})
        coordinates = self.return_coordinates(city)
        if 'latitude' in coordinates:
            return self.sun_send(msg, coordinates['latitude'], coordinates['longitude'], {'sunrise': True})
        return 'Not a valid city '+str(city)

    @arg_botcmd('--latitude', dest='latitude', type=str, default='39.7392')
    @arg_botcmd('--longitude', dest='longitude', type=str, default='-104.9903')
    @arg_botcmd('--city', dest='city', type=str, default=None)
    def sunset(self, msg, latitude, longitude, city):
        """Return next sunset"""
        if city is None:
            return self.sun_send(msg, latitude, longitude, {'sunset': True})
        coordinates = self.return_coordinates(city)
        if 'latitude' in coordinates:
            return self.sun_send(msg, coordinates['latitude'], coordinates['longitude'], {'sunset': True})
        return 'Not a valid city '+str(city)

    @arg_botcmd('--latitude', dest='latitude', type=str, default='39.7392')
    @arg_botcmd('--longitude', dest='longitude', type=str, default='-104.9903')
    @arg_botcmd('--city', dest='city', type=str, default=None)
    @arg_botcmd('--time', dest='sun_time', type=str, default='sunrise')
    def solar(self, msg, latitude, longitude, sun_time, city):
        """Return next sun time"""
        parameters = {sun_time: True}
        if sun_time == 'all':
            parameters = {'astronomical_twilight_begin': True,
                          'nautical_twilight_begin': True,
                          'civil_twilight_begin': True,
                          'sunrise': True,
                          'solar_noon': True,
                          'sunset': True,
                          'astronomical_twilight_end': True,
                          'nautical_twilight_end': True,
                          'civil_twilight_end': True,
                          'day_length': True}
        if city is None:
            return self.sun_send(msg, latitude, longitude, parameters)
        coordinates = self.return_coordinates(city)
        if 'latitude' in coordinates:
            return self.sun_send(msg, coordinates['latitude'], coordinates['longitude'], parameters)
        return 'Not a valid city '+str(city)

    def return_coordinates(self, city):
        """Return latitude, longitude of a city"""
        cities = {'DENVER': {'latitude': '39.7392', 'longitude': '-104.9903'},
                  'AUSTIN': {'latitude': '30.2672', 'longitude': '-97.7431'},
                  'SEATTLE': {'latitude': '47.6062', 'longitude': '-122.3321'},
                  'MIAMI': {'latitude': '25.7617', 'longitude': '-80.1918'},
                  'LONDON': {'latitude': '51.5074', 'longitude': '-0.1278'},
                  'TOKYO': {'latitude': '35.6762', 'longitude': '139.6503'},
                  'BEIJING': {'latitude': '39.9042', 'longitude': '116.4074'},
                  'SYDNEY': {'latitude': '-33.8688', 'longitude': '151.2093'},
                  'NEW YORK': {'latitude': '40.7128', 'longitude': '-74.0060'},
                  'DALLAS': {'latitude': '32.7767', 'longitude': '-96.7970'},
                  'HOUSTON': {'latitude': '29.7604', 'longitude': '-95.3698'},
                  'CHICAGO': {'latitude': '41.8781', 'longitude': '-87.6298'}}
        if city.upper() in cities:
            coordinates = {'latitude': cities[city.upper()]['latitude'],
                           'longitude': cities[city.upper()]['longitude']}
            return coordinates
        return {}

    def sun_send(self, msg, latitude, longitude, parameters):
        """Lookup sun time"""
        sunrise = False
        if 'sunrise' in parameters:
            sunrise = parameters['sunrise']
        sunset = False
        if 'sunset' in parameters:
            sunset = parameters['sunset']
        astronomical_twilight = False
        if 'astronomical_twilight' in parameters:
            astronomical_twilight = parameters['astronomical_twilight']
        astronomical_twilight_begin = False
        if 'astronomical_twilight_begin' in parameters:
            astronomical_twilight_begin = parameters['astronomical_twilight_begin']
        astronomical_twilight_end = False
        if 'astronomical_twilight_end' in parameters:
            astronomical_twilight_end = parameters['astronomical_twilight_end']
        civil_twilight = False
        if 'civil_twilight' in parameters:
            civil_twilight = parameters['civil_twilight']
        civil_twilight_begin = False
        if 'civil_twilight_begin' in parameters:
            civil_twilight_begin = parameters['civil_twilight_begin']
        civil_twilight_end = False
        if 'civil_twilight_end' in parameters:
            civil_twilight_end = parameters['civil_twilight_end']
        day_length = False
        if 'day_length' in parameters:
            day_length = parameters['day_length']
        nautical_twilight = False
        if 'nautical_twilight' in parameters:
            nautical_twilight = parameters['nautical_twilight']
        nautical_twilight_begin = False
        if 'nautical_twilight_begin' in parameters:
            nautical_twilight_begin = parameters['nautical_twilight_begin']
        nautical_twilight_end = False
        if 'nautical_twilight_end' in parameters:
            nautical_twilight_end = parameters['nautical_twilight_end']
        solar_noon = False
        if 'solar_noon' in parameters:
            solar_noon = parameters['solar_noon']
        # https://api.sunrise-sunset.org/json?lat=36.7201600&lng=-4.4203400&date=today
        url = 'https://api.sunrise-sunset.org/json?lat='+latitude+'&lng='+longitude+'&date=today'
        page = urllib.request.Request(url)
        response = json.loads(urllib.request.urlopen(page).read().decode('utf-8'))
        requested_times = []
        results = {}
        if astronomical_twilight:
            requested_times.append('astronomical_twilight_begin')
            requested_times.append('astronomical_twilight_end')
        if astronomical_twilight_begin:
            requested_times.append('astronomical_twilight_begin')
        if nautical_twilight:
            requested_times.append('nautical_twilight_begin')
            requested_times.append('nautical_twilight_end')
        if nautical_twilight_begin:
            requested_times.append('nautical_twilight_begin')
        if civil_twilight:
            requested_times.append('civil_twilight_begin')
            requested_times.append('civil_twilight_end')
        if civil_twilight_begin:
            requested_times.append('civil_twilight_begin')
        if sunrise:
            requested_times.append('sunrise')
        if solar_noon:
            requested_times.append('solar_noon')
        if sunset:
            requested_times.append('sunset')
        if civil_twilight_end:
            requested_times.append('civil_twilight_end')
        if nautical_twilight_end:
            requested_times.append('nautical_twilight_end')
        if astronomical_twilight_end:
            requested_times.append('astronomical_twilight_end')
        if day_length:
            requested_times.append('day_length')
        if 'results' in response:
            for requested_time in requested_times:
                if requested_time in response['results'] and requested_time != 'day_length':
                    time = datetime.datetime.strptime(response['results'][requested_time], '%H:%M:%S %p')
                    today = datetime.datetime.today()
                    combined = datetime.datetime.combine(today.date(), time.time())
                    combined_utc = pytz.timezone('UTC').localize(combined)
                    combined_local = combined_utc.astimezone(tz=tz.gettz('America/Denver'))
                    results[requested_time] = str(combined_local.strftime('%H:%M:%S'))
                if requested_time == 'day_length':
                    results[requested_time] = str(response['results'][requested_time])
            result_string = ''
            for key in results:
                result_string = result_string + key + '=' + results[key] + '\n'
            return result_string
        return 'No results in response: '+str(response)
