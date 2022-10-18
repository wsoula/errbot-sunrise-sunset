""" Tests for plugin """
pytest_plugins = ['errbot.backends.test']

extra_plugin_dir = '.'


def test_sunrise(testbot):
    """ Test the command """
    testbot.push_message('!sunrise')
    assert 'sunrise=' in testbot.pop_message()


def test_sunrise_invalid_city(testbot):
    """ Test invalid city """
    testbot.assertInCommand('!sunrise --city Alvin', 'Not a valid city Alvin')


def test_sunset(testbot):
    """ Test the sunset command """
    testbot.push_message('!sunset')
    assert 'sunset=' in testbot.pop_message()


def test_sunset_invalid_city(testbot):
    """ Test invalid city """
    testbot.assertInCommand('!sunset --city Alvin', 'Not a valid city Alvin')


def test_solar(testbot):
    """ Test the solar command """
    testbot.push_message('!solar')
    assert 'sunrise=' in testbot.pop_message()


def test_solar_all(testbot):
    """ Test solar all """
    testbot.push_message('!solar --time all')
    result = testbot.pop_message()
    assert 'astronomical_twilight_begin=' in result
    assert 'nautical_twilight_begin=' in result
    assert 'civil_twilight_begin=' in result
    assert 'sunrise=' in result
    assert 'solar_noon=' in result
    assert 'sunset=' in result
    assert 'civil_twilight_end=' in result
    assert 'nautical_twilight_end=' in result
    assert 'astronomical_twilight_end=' in result
    assert 'day_length=' in result


def test_solar_invalid_city(testbot):
    """ Test invalid city """
    testbot.assertInCommand('!solar --city Alvin', 'Not a valid city Alvin')
