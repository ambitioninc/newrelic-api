import requests

from .base import Resource


class AlertPolicies(Resource):
    """
    An interface for interacting with the NewRelic Alert Policies API.
    """
    def list(
            self, filter_name=None, filter_type=None, filter_ids=None,
            filter_enabled=None, page=None):
        """
        This API endpoint returns a paginated list of the alert policies
        associated with your New Relic account. Alert policies can be filtered
        by their name, list of IDs, type (application, key_transaction, or
        server) or whether or not policies are archived (defaults to filtering
        archived policies).

        :type filter_name: str
        :param filter_name: Filter by name

        :type filter_type: list of str
        :param filter_type: Filter by policy types.

        :type filter_ids: list of int
        :param filter_ids: Filter by policy IDs

        :type filter_enabled: bool
        :param filter_enabled: Select only enabled/disabled policies (default: both)

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "alert_policies": [
                    {
                        "id": "integer",
                        "type": "string",
                        "name": "string",
                        "enabled": "boolean",
                        "conditions": [
                            {
                                "id": "integer",
                                "type": "string",
                                "severity": "string",
                                "threshold": "float",
                                "trigger_minutes": "integer",
                                "enabled": "boolean"
                            }
                        ],
                        "links": {
                            "notification_channels": [
                                "integer"
                            ],
                            "applications": [
                                "integer"
                            ],
                            "key_transactions": [
                                "integer"
                            ],
                            "servers": [
                                "integer"
                            ]
                        }
                    }
                ]
            }

        """
        filters = [
            'filter[name]={0}'.format(filter_name) if filter_name else None,
            'filter[type]={0}'.format(','.join(filter_type)) if filter_type else None,
            'filter[ids]={0}'.format(','.join([str(app_id) for app_id in filter_ids])) if filter_ids else None,
            'filter[enabled]={0}'.format(filter_enabled) if filter_enabled in [True, False] else None,
            'page={0}'.format(page) if page else None
        ]

        response = requests.get(
            url='{0}alert_policies.json'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(filters)
        )
        return response.json()

    def show(self, id):
        """
        This API endpoint returns a single alert policy, identified by ID.

        :type id: int
        :param id: Alert policy ID

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "alert_policy": {
                    "id": "integer",
                    "type": "string",
                    "name": "string",
                    "enabled": "boolean",
                    "conditions": [
                        {
                            "id": "integer",
                            "type": "string",
                            "severity": "string",
                            "threshold": "float",
                            "trigger_minutes": "integer",
                            "enabled": "boolean"
                        }
                    ],
                    "links": {
                        "notification_channels": [
                            "integer"
                        ],
                        "applications": [
                            "integer"
                        ],
                        "key_transactions": [
                            "integer"
                        ],
                        "servers": [
                            "integer"
                        ]
                    }
                }
            }

        """
        response = requests.get(
            url='{0}alert_policies/{1}.json'.format(self.URL, id),
            headers=self.headers,
        )
        return response.json()

    def update(self, id, policy_update):
        """
        This API endpoint allows you to update your alert policies.

        The input is expected to be in **JSON** format in the body
        parameters of the PUT request. The exact schema is defined below. Any
        extra parameters passed in the body **will be ignored** .::

            {
                "alert_policy": {
                    "name": str,
                    "enabled": bool,
                    "conditions": [
                        {
                            "id": int,
                            "threshold": float,
                            "trigger_minutes": int,
                            "enabled": bool
                        }
                    ],
                    "links": {
                        "notification_channels": [
                            int
                        ],
                        "applications": [
                            int
                        ],
                        "key_transactions": [
                            "int
                        ],
                        "servers": [
                            int
                        ]
                    }
                }
            }

        **NOTE:** When updating alertable and notification channel links, the
        list sent replaces the existing list. Invalid values will be ignored
        but an empty array will result in alertables/channels being reset.

        :type id: int
        :param id: Alert policy ID

        :type policy_update: dict
        :param policy_update: The json of the policy to update

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "alert_policy": {
                    "id": "integer",
                    "type": "string",
                    "name": "string",
                    "enabled": "boolean",
                    "conditions": [
                        {
                            "id": "integer",
                            "type": "string",
                            "severity": "string",
                            "threshold": "float",
                            "trigger_minutes": "integer",
                            "enabled": "boolean"
                        }
                    ],
                    "links": {
                        "notification_channels": [
                            "integer"
                        ],
                        "applications": [
                            "integer"
                        ],
                        "key_transactions": [
                            "integer"
                        ],
                        "servers": [
                            "integer"
                        ]
                    }
                }
            }

        """
        response = requests.put(
            url='{0}alert_policies/{1}.json'.format(self.URL, id),
            headers=self.headers,
            data=policy_update
        )
        return response.json()
