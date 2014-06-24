import os

from newrelic_api.exceptions import ConfigurationException


class Resource(object):
    URL = 'https://api.newrelic.com/v2/'

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('NEWRELIC_API_KEY')

        if not self.api_key:
            raise ConfigurationException('NEWRELIC_API_KEY not present in environment!')
