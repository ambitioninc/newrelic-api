from .base import Resource
from newrelic_api.exceptions import NoEntityException


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

    def update(
            self, policy_id, alert_condition_id,
            condition_type=None,
            name=None,
            enabled=None,
            entities=None,
            metric=None,
            terms=None):
        """
        Updates any of the optional parameters of the alert condition

        :type policy_id: int
        :param policy_id: Alert policy id where target alert condition belongs to

        :type alert_condition_id: int
        :param alert_condition_id: Alerts condition id to update

        :type name: str
        :param name: The name of the server

        :type enabled: bool
        :param enabled: Whether to enable that alert condition

        :type entities: list[str]
        :param name: entity ids to which the alert condition is applied

        :rtype: dict
        :return: The JSON response of the API

        :raises: This will raise a
            :class:`NewRelicAPIServerException<newrelic_api.exceptions.NoEntityException>`
            if target alert condition is not included in target policy

        ::

            {
                "condition": {
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
            }

        """
        conditions_dict = self.list(policy_id)
        target_condition = None
        for condition in conditions_dict['conditions']:
            if int(condition['id']) == alert_condition_id:
                target_condition = condition
                break

        if target_condition is None:
            raise NoEntityException(
                'Target alert condition is not included in that policy.'
                'policy_id: {}, alert_condition_id {}'.format(policy_id, alert_condition_id))

        data = {
            'condition': {
                'condition_type': condition_type or target_condition['condition_type'],
                'name': name or target_condition['name'],
                'enabled': enabled or target_condition['enabled'],
                'entities': entities or target_condition['entities'],
                'metric': metric or target_condition['metric'],
                'terms': terms or target_condition['terms'],
            }
        }

        return self._put(
            url='{0}alerts_conditions/{1}.json'.format(self.URL, alert_condition_id),
            headers=self.headers,
            data=data
        )

    # TODO: implement create and delete
    # See https://docs.newrelic.com/docs/alerts/new-relic-alerts-beta/getting-started/rest-api-calls-new-relic-alerts
