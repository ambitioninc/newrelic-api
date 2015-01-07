class ConfigurationException(Exception):
    """
    An exception for Configuration errors
    """
    message = 'There was an error in the configuration'


class NewRelicAPIServerException(Exception):
    """
    An exception for New Relic server errors
    """
    message = 'There was an error from New Relic'
