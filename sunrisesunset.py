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
        return self.sun_send(msg, coordinates['latitude'], coordinates['longitude'], {'sunrise': True})

    @arg_botcmd('--latitude', dest='latitude', type=str, default='39.7392')
    @arg_botcmd('--longitude', dest='longitude', type=str, default='-104.9903')
    @arg_botcmd('--city', dest='city', type=str, default=None)
    def sunset(self, msg, latitude, longitude, city):
        """Return next sunset"""
        if city is None:
            return self.sun_send(msg, latitude, longitude, {'sunset': True})
        coordinates = self.return_coordinates(city)
        return self.sun_send(msg, coordinates['latitude'], coordinates['longitude'], {'sunset': True})

    @arg_botcmd('--latitude', dest='latitude', type=str, default='39.7392')
    @arg_botcmd('--longitude', dest='longitude', type=str, default='-104.9903')
    @arg_botcmd('--city', dest='city', type=str, default=None)
    @arg_botcmd('--time', dest='sun_time', type=str, default='sunrise')
    def solar(self, msg, latitude, longitude, sun_time, city):
        """Return next sun time"""
        parameters = {sun_time: True}
        if sun_time == 'all':
            parameters = {'astronomical_twilight': True,
                          'nautical_twilight': True,
                          'civil_twilight': True,
                          'sunrise': True,
                          'solar_noon': True,
                          'sunset': True,
                          'day_length': True}
        if city is None:
            return self.sun_send(msg, latitude, longitude, parameters)
        coordinates = self.return_coordinates(city)
        return self.sun_send(msg, coordinates['latitude'], coordinates['longitude'], parameters)

    def return_coordinates(self, city):
        """Return latitude, longitude of a city"""
        if city.upper() == 'DENVER':
            coordinates = {'latitude': '39.7392',
                           'longitude': '-104.9903'}
        if city.upper() == 'AUSTIN':
            coordinates = {'latitude': '30.2672',
                           'longitude': '-97.7431'}
        return coordinates

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
        civil_twilight = False
        if 'civil_twilight' in parameters:
            civil_twilight = parameters['civil_twilight']
        day_length = False
        if 'day_length' in parameters:
            day_length = parameters['day_length']
        nautical_twilight = False
        if 'nautical_twilight' in parameters:
            nautical_twilight = parameters['nautical_twilight']
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
        if nautical_twilight:
            requested_times.append('nautical_twilight_begin')
            requested_times.append('nautical_twilight_end')
        if civil_twilight:
            requested_times.append('civil_twilight_begin')
            requested_times.append('civil_twilight_end')
        if sunrise:
            requested_times.append('sunrise')
        if solar_noon:
            requested_times.append('solar_noon')
        if sunset:
            requested_times.append('sunset')
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
