import requests

from .base import Resource


class Servers(Resource):
    """
    An interface for interacting with the NewRelic server API.
    """

    def __init__(self, *args, **kwargs):
        """
        :type api_key: str
        :param api_key: The API key. If no key is passed, the environment
            variable NEWRELIC_API_KEY is used. If the variable is not present,
            a ConfigurationException is raised.
        """
        super(Servers, self).__init__(*args, **kwargs)
        self.headers = {
            'Content-type': 'application/json',
            'X-Api-Key': self.api_key,
        }

    def list(self, filter_name=None, filter_ids=None, page=None):
        """
        This API endpoint returns a paginated list of the Servers
        associated with your New Relic account. Servers can be filtered
        by their name or by a list of server IDs.

        :type filter_name: str
        :param filter_name: Filter by server name

        :type filter_ids: list of ints
        :param filter_ids: Filter by server ids

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API
        """
        response = requests.get(
            url='{0}servers.json'.format(self.URL),
            headers=self.headers,
            params={
                'filter': {
                    'name': filter_name,
                    'ids': filter_ids,
                },
                'page': page
            }
        )
        return response.json()

    def show(self, id):
        """
        This API endpoint returns a single Server, identified its ID.

        :type id: int
        :param id: Server ID

        :rtype: dict
        :return: The JSON response of the API
        """
        response = requests.get(
            url='{0}servers/{1}.json'.format(self.URL, id),
            headers=self.headers,
        )
        return response.json()

    def update(self, id, name=None):
        """
        Updates any of the optional parameters of the server

        :type id: int
        :param id: Server ID

        :type name: str
        :param name: The name of the server

        :rtype: dict
        :return: The JSON response of the API
        """
        nr_data = self.show(id)['server']

        data = {
            'server': {
                'name': name or nr_data['name'],
            }
        }

        response = requests.put(
            url='{0}servers/{1}.json'.format(self.URL, id),
            headers=self.headers,
            data=data
        )
        return response.json()

    def delete(self, id):
        """
        This API endpoint deletes an server and all of its reported data.

        WARNING: Only servers that have stopped reporting can be deleted.
            This is an irreversible process which will delete all reported
            data for this server.

        :type id: int
        :param id: Server ID

        :rtype: dict
        :return: The JSON response of the API
        """
        response = requests.delete(
            url='{0}servers/{1}.json'.format(
                self.URL,
                id),
            headers=self.headers,
        )
        return response.json()

    def metric_names(self, id, name=None, page=None):
        """
        Return a list of known metrics and their value names for the given resource.

        :type id: int
        :param id: Server ID

        :type name: str
        :param name: Filter metrics by name

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API
        """
        response = requests.get(
            url='{0}servers/{1}/metrics.json'.format(self.URL, id),
            headers=self.headers,
            params={
                'name': name,
                'page': page
            }
        )
        return response.json()

    def metric_data(
            self, id, names, values=None, from_dt=None, to_dt=None,
            summarize=False):
        """
        This API endpoint returns a list of values for each of the requested
        metrics. The list of available metrics can be returned using the Metric
        Name API endpoint. Metric data can be filtered by a number of
        parameters, including multiple names and values, and by time range.
        Metric names and values will be matched intelligently in the
        background. You can also retrieve a summarized data point across the
        entire time range selected by using the summarize parameter.

        **Note** All times sent and received are formatted in UTC. The default
        time range is the last 30 minutes.

        :type id: int
        :param id: Server ID

        :type names: list of str
        :param names: Retrieve specific metrics by name

        :type values: list of str
        :param values: Retrieve specific metric values

        :type from_dt: datetime
        :param from_dt: Retrieve metrics after this time

        :type to_dt: datetime
        :param to_dt: Retrieve metrics before this time

        :type summarize: bool
        :param summarize: Summarize the data

        :rtype: dict
        :return: The JSON response of the API
        """
        response = requests.get(
            url='{0}servers/{1}/metrics/data.json'.format(self.URL, id),
            headers=self.headers,
            params={
                'names': names,
                'values': values,
                'from': from_dt,
                'to': to_dt,
                'summarize': summarize
            }
        )
        return response.json()
