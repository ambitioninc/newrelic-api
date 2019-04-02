from .base import Resource


class NotificationChannels(Resource):
    """
    An interface for interacting with the NewRelic Notification Channels API.
    """
    def list(self, page=None):
        """
        This API endpoint returns a paginated list of the notification channels
        associated with your New Relic account.

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results
        """
        filters = [
            'page={0}'.format(page) if page else None
        ]
        return self._get(
            url='{0}alerts_channels.json'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(filters)
        )

    def create(self, name, type, configuration):
        """
        This API endpoint allows you to create a notification channel, see
            New Relic API docs for details of types and configuration

        :type name: str
        :param name: The name of the channel

        :type type: str
        :param type: Type of notification, eg. email, user, webhook

        :type configuration: hash
        :param configuration: Configuration for notification

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "channels": {
                     "id": "integer",
                     "name": "string",
                     "type": "string",
                     "configuration": { },
                     "links": {
                        "policy_ids": []
                    }
                }
            }

        """

        data = {
            "channel": {
                "name": name,
                "type": type,
                "configuration": configuration
            }
        }

        return self._post(
            url='{0}alerts_channels.json'.format(self.URL),
            headers=self.headers,
            data=data
        )

    def delete(self, id):
        """
        This API endpoint allows you to delete a notification channel

        :type id: integer
        :param id: The id of the channel

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "channels": {
                     "id": "integer",
                     "name": "string",
                     "type": "string",
                     "configuration": { },
                     "links": {
                        "policy_ids": []
                    }
                }
            }

        """

        return self._delete(
            url='{0}alerts_channels/{1}.json'.format(self.URL, id),
            headers=self.headers
        )
