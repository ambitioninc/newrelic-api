from .base import Resource


class AlertConditions(Resource):
    """
    An interface for interacting with the NewRelic Alert Conditions API.
    """
    def list(self, policy_id, page=None):
        """
        This API endpoint returns a paginated list of alert conditions associated with the
        given policy_id.

        This API endpoint returns a paginated list of the alert conditions
        associated with your New Relic account. Alert conditions can be filtered
        by their name, list of IDs, type (application, key_transaction, or
        server) or whether or not policies are archived (defaults to filtering
        archived policies).

        :type policy_id: int
        :param policy_id: Alert policy id

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results

        ::

            {
                "conditions": [
                    {
                        "id": "integer",
                        "condition_type": "string",
                        "name": "string",
                        "enabled": "boolean",
                        "entities": [
                          "integer"
                        ],
                        "metric": "string",
                        "runbook_url": "string",
                        "terms": [
                          {
                            "duration": "string",
                            "operator": "string",
                            "priority": "string",
                            "threshold": "string",
                            "time_function": "string"
                          }
                        ],
                        "user_defined": {
                          "metric": "string",
                          "value_function": "string"
                        }
                    }
                ]
            }

        """
        filters = [
            'policy_id={0}'.format(policy_id),
            'page={0}'.format(page) if page else None
        ]

        return self._get(
            url='{0}alerts_conditions.json'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(filters)
        )
