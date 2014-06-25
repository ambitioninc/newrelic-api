import os

from newrelic_api.exceptions import ConfigurationException


class Resource(object):
    URL = 'https://api.newrelic.com/v2/'

    def __init__(self, api_key=None):
        """
        :type api_key: str
        :param api_key: The API key. If no key is passed, the environment
            variable NEWRELIC_API_KEY is used. If the variable is not present,
            a ConfigurationException is raised.
        """
        self.api_key = api_key or os.environ.get('NEWRELIC_API_KEY')

        if not self.api_key:
            raise ConfigurationException('NEWRELIC_API_KEY not present in environment!')

        self.headers = {
            'Content-type': 'application/json',
            'X-Api-Key': self.api_key,
        }
