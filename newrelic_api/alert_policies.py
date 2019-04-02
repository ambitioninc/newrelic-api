from .base import Resource


class AlertPolicies(Resource):
    """
    An interface for interacting with the NewRelic Alert Policies API.
    """
    def list(self, filter_name=None, page=None):
        """
        This API endpoint returns a paginated list of the alert policies
        associated with your New Relic account. Alert policies can be filtered
        by their name with exact match.

        :type filter_name: str
        :param filter_name: Filter by name

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results

        ::

            {
                "policies": [
                    {
                        "id": "integer",
                        "incident_preference": "string",
                        "name": "string",
                        "created_at": "integer",
                    },
                ]
            }

        """
        filters = [
            'filter[name]={0}'.format(filter_name) if filter_name else None,
            'page={0}'.format(page) if page else None
        ]

        return self._get(
            url='{0}alerts_policies.json'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(filters)
        )

    def create(self, name, incident_preference):
        """
        This API endpoint allows you to create an alert policy

        :type name: str
        :param name: The name of the policy

        :type incident_preference: str
        :param incident_preference: Can be PER_POLICY, PER_CONDITION or
            PER_CONDITION_AND_TARGET

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "policy": {
                    "created_at": "time",
                    "id": "integer",
                    "incident_preference": "string",
                    "name": "string",
                    "updated_at": "time"
                }
            }

        """

        data = {
            "policy": {
                "name": name,
                "incident_preference": incident_preference
            }
        }

        return self._post(
            url='{0}alerts_policies.json'.format(self.URL),
            headers=self.headers,
            data=data
        )

    def update(self, id, name, incident_preference):
        """
        This API endpoint allows you to update an alert policy

        :type id: integer
        :param id: The id of the policy

        :type name: str
        :param name: The name of the policy

        :type incident_preference: str
        :param incident_preference: Can be PER_POLICY, PER_CONDITION or
            PER_CONDITION_AND_TARGET

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "policy": {
                    "created_at": "time",
                    "id": "integer",
                    "incident_preference": "string",
                    "name": "string",
                    "updated_at": "time"
                }
            }

        """

        data = {
            "policy": {
                "name": name,
                "incident_preference": incident_preference
            }
        }

        return self._put(
            url='{0}alerts_policies/{1}.json'.format(self.URL, id),
            headers=self.headers,
            data=data
        )

    def delete(self, id):
        """
        This API endpoint allows you to delete an alert policy

        :type id: integer
        :param id: The id of the policy

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "policy": {
                    "created_at": "time",
                    "id": "integer",
                    "incident_preference": "string",
                    "name": "string",
                    "updated_at": "time"
                }
            }

        """

        return self._delete(
            url='{0}alerts_policies/{1}.json'.format(self.URL, id),
            headers=self.headers
        )

    def associate_with_notification_channel(self, id, channel_id):
        """
        This API endpoint allows you to associate an alert policy with an
            notification channel

        :type id: integer
        :param id: The id of the policy

        :type channel_id: integer
        :param channel_id: The id of the notification channel

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "policy": {
                    "channel_ids": "list",
                    "id": "integer"
                }
            }

        """

        return self._put(
            url='{0}alerts_policy_channels.json?policy_id={1}&channel_ids={2}'.format(
                self.URL,
                id,
                channel_id
            ),
            headers=self.headers
        )

    def dissociate_from_notification_channel(self, id, channel_id):
        """
        This API endpoint allows you to dissociate an alert policy from an
            notification channel

        :type id: integer
        :param id: The id of the policy

        :type channel_id: integer
        :param channel_id: The id of the notification channel

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
               "channel":{
                  "configuration": "hash",
                  "type": "string",
                  "id": "integer",
                  "links":{
                     "policy_ids": "list"
                  },
                  "name": "string"
               }
            }

        """

        return self._delete(
            url='{0}alerts_policy_channels.json?policy_id={1}&channel_id={2}'.format(
                self.URL,
                id,
                channel_id
            ),
            headers=self.headers
        )
