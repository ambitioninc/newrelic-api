import requests

from .base import Resource


class NotificationChannels(Resource):
    """
    An interface for interacting with the NewRelic Notification Channels API.
    """
    def list(self, filter_type=None, filter_ids=None, page=None):
        """
        This API endpoint returns a paginated list of the notification channels
        associated with your New Relic account.

        Notification channels can be filtered by their type or a list of IDs.

        :type filter_type: list of str
        :param filter_type: Filter by notification channel types

        :type filter_ids: list of int
        :param filter_ids: Filter by notification channel ids

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API
        """
        response = requests.get(
            url='{0}notification_channels.json'.format(self.URL),
            headers=self.headers,
            params={
                'filter': {
                    'type': filter_type,
                    'ids': filter_ids,
                },
                'page': page
            }
        )
        return response.json()

    def show(self, id):
        """
        This API endpoint returns a single notification channel, identified by
        ID.

        :type id: int
        :param id: notification channel ID

        :rtype: dict
        :return: The JSON response of the API
        """
        response = requests.get(
            url='{0}notification_channels/{1}.json'.format(self.URL, id),
            headers=self.headers,
        )
        return response.json()
