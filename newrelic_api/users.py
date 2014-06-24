import requests

from .base import Resource


class Users(Resource):
    """
    An interface for interacting with the NewRelic user API.
    """

    def __init__(self, *args, **kwargs):
        """
        :type api_key: str
        :param api_key: The API key. If no key is passed, the environment
            variable NEWRELIC_API_KEY is used. If the variable is not present,
            a ConfigurationException is raised.
        """
        super(Users, self).__init__(*args, **kwargs)
        self.headers = {
            'Content-type': 'application/json',
            'X-Api-Key': self.api_key,
        }

    def list(self, filter_email=None, filter_ids=None, page=None):
        """
        This API endpoint returns a paginated list of the Users
        associated with your New Relic account. Users can be filtered
        by their email or by a list of user IDs.

        :type filter_email: str
        :param filter_email: Filter by user email

        :type filter_ids: list of ints
        :param filter_ids: Filter by user ids

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API
        """
        response = requests.get(
            url='{0}users.json'.format(self.URL),
            headers=self.headers,
            params={
                'filter': {
                    'email': filter_email,
                    'ids': filter_ids,
                },
                'page': page
            }
        )
        return response.json()

    def show(self, id):
        """
        This API endpoint returns a single User, identified its ID.

        :type id: int
        :param id: User ID

        :rtype: dict
        :return: The JSON response of the API
        """
        response = requests.get(
            url='{0}users/{1}.json'.format(self.URL, id),
            headers=self.headers,
        )
        return response.json()
