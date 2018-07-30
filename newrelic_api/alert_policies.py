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
                        "rollup_strategy": "string",
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

    # TODO: implement create and delete
    # See https://docs.newrelic.com/docs/alerts/new-relic-alerts-beta/getting-started/rest-api-calls-new-relic-alerts
