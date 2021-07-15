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
    def sunrise(self, msg, latitude, longitude):
        """Return next sunrise"""
        return self.sun_send(msg, latitude, longitude, {'sunrise': True})

    @arg_botcmd('--latitude', dest='latitude', type=str, default='39.7392')
    @arg_botcmd('--longitude', dest='longitude', type=str, default='-104.9903')
    def sunset(self, msg, latitude, longitude):
        """Return next sunrise"""
        return self.sun_send(msg, latitude, longitude, {'sunset': True})

    @arg_botcmd('--latitude', dest='latitude', type=str, default='39.7392')
    @arg_botcmd('--longitude', dest='longitude', type=str, default='-104.9903')
    @arg_botcmd('--time', dest='sun_time', type=str, default='sunrise')
    def solar(self, msg, latitude, longitude, sun_time):
        """Return next sun time"""
        return self.sun_send(msg, latitude, longitude, {sun_time: True})

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
        url = 'https://api.sunrise-sunset.org/json?lat='+latitude+'&lng='+longitude
        page = urllib.request.Request(url)
        response = json.loads(urllib.request.urlopen(page).read().decode('utf-8'))
        requested_times = []
        results = {}
        if sunrise:
            requested_times.append('sunrise')
        if sunset:
            requested_times.append('sunset')
        if astronomical_twilight:
            requested_times.append('astronomical_twilight_begin')
            requested_times.append('astronomical_twilight_end')
        if civil_twilight:
            requested_times.append('civil_twilight_begin')
            requested_times.append('civil_twilight_end')
        if day_length:
            requested_times.append('day_length')
        if nautical_twilight:
            requested_times.append('nautical_twilight_begin')
            requested_times.append('nautical_twilight_end')
        if solar_noon:
            requested_times.append('solar_noon')
        if 'results' in response:
            for requested_time in requested_times:
                if requested_time in response['results']:
                    time = datetime.datetime.strptime(response['results'][requested_time], '%H:%M:%S %p')
                    today = datetime.datetime.today()
                    combined = datetime.datetime.combine(today.date(), time.time())
                    combined_utc = pytz.timezone('UTC').localize(combined)
                    combined_local = combined_utc.astimezone(tz=tz.gettz('America/Denver'))
                    results[requested_time] = str(combined_local)
            return results
        return 'No results in response: '+str(response)
