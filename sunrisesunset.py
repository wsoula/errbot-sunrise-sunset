"""Return sunrise or sunset time"""
import urllib.request
import json
import datetime
import pytz
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
    @arg_botcmd('--time', dest='sun_time', type=str, default='sunrise')
    def sun(self, msg, latitude, longitude, sun_time):
        """Return next sun time"""
        return self.sun_send(msg, latitude, longitude, {sun_time: True})

    def sun_send(self, msg, latitude, longitude, parameters):
        """Lookup sun time"""
        if 'sunrise' in parameters:
            sunrise = parameters['sunrise']
        if 'sunset' in parameters:
            sunset = parameters['sunset']
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
        if 'results' in response:
            for requested_time in requested_times:
                if requested_time in response['results']:
                    results[requested_time] = response['results'][requested_time]
            return results
        return 'No results in response: '+str(response)
