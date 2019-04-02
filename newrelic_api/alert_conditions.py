from .base import Resource
from newrelic_api.exceptions import NoEntityException, ConfigurationException


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
                        "type": "string",
                        "condition_scope":  "string",
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
            self, alert_condition_id, policy_id,
            type=None,
            condition_scope=None,
            name=None,
            entities=None,
            metric=None,
            runbook_url=None,
            terms=None,
            user_defined=None,
            enabled=None):
        """
        Updates any of the optional parameters of the alert condition

        :type alert_condition_id: int
        :param alert_condition_id: Alerts condition id to update

        :type policy_id: int
        :param policy_id: Alert policy id where target alert condition belongs to

        :type type: str
        :param type: The type of the condition, can be apm_app_metric,
            apm_kt_metric, servers_metric, browser_metric, mobile_metric

        :type condition_scope: str
        :param condition_scope: The scope of the condition, can be instance or application

        :type name: str
        :param name: The name of the server

        :type entities: list[str]
        :param name: entity ids to which the alert condition is applied

        :type : str
        :param metric: The target metric

        :type : str
        :param runbook_url: The url of the runbook

        :type terms: list[hash]
        :param terms: list of hashes containing threshold config for the alert

        :type user_defined: hash
        :param user_defined: hash containing threshold user_defined for the alert
            required if metric is set to user_defined

        :type enabled: bool
        :param enabled: Whether to enable that alert condition

        :rtype: dict
        :return: The JSON response of the API

        :raises: This will raise a
            :class:`NewRelicAPIServerException<newrelic_api.exceptions.NoEntityException>`
            if target alert condition is not included in target policy

        :raises: This will raise a
            :class:`ConfigurationException<newrelic_api.exceptions.ConfigurationException>`
            if metric is set as user_defined but user_defined config is not passed

        ::

            {
                "condition": {
                    "id": "integer",
                    "type": "string",
                    "condition_scope":  "string",
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
                'policy_id: {}, alert_condition_id {}'.format(policy_id, alert_condition_id)
            )

        data = {
            'condition': {
                'type': type or target_condition['type'],
                'name': name or target_condition['name'],
                'entities': entities or target_condition['entities'],
                'condition_scope': condition_scope or target_condition['condition_scope'],
                'terms': terms or target_condition['terms'],
                'metric': metric or target_condition['metric'],
                'runbook_url': runbook_url or target_condition['runbook_url'],
            }
        }

        if enabled is not None:
            data['condition']['enabled'] = str(enabled).lower()

        if data['condition']['metric'] == 'user_defined':
            if user_defined:
                data['condition']['user_defined'] = user_defined
            elif 'user_defined' in target_condition:
                data['condition']['user_defined'] = target_condition['user_defined']
            else:
                raise ConfigurationException(
                    'Metric is set as user_defined but no user_defined config specified'
                )

        return self._put(
            url='{0}alerts_conditions/{1}.json'.format(self.URL, alert_condition_id),
            headers=self.headers,
            data=data
        )

    def create(
            self, policy_id,
            type,
            condition_scope,
            name,
            entities,
            metric,
            terms,
            runbook_url=None,
            user_defined=None,
            enabled=True):
        """
        Creates an alert condition

        :type policy_id: int
        :param policy_id: Alert policy id where target alert condition belongs to

        :type type: str
        :param type: The type of the condition, can be apm_app_metric,
            apm_kt_metric, servers_metric, browser_metric, mobile_metric

        :type condition_scope: str
        :param condition_scope: The scope of the condition, can be instance or application

        :type name: str
        :param name: The name of the server

        :type entities: list[str]
        :param name: entity ids to which the alert condition is applied

        :type : str
        :param metric: The target metric

        :type : str
        :param runbook_url: The url of the runbook

        :type terms: list[hash]
        :param terms: list of hashes containing threshold config for the alert

        :type user_defined: hash
        :param user_defined: hash containing threshold user_defined for the alert
            required if metric is set to user_defined

        :type enabled: bool
        :param enabled: Whether to enable that alert condition

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "condition": {
                    "id": "integer",
                    "type": "string",
                    "condition_scope":  "string",
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

        data = {
            'condition': {
                'type': type,
                'name': name,
                'enabled': enabled,
                'entities': entities,
                'condition_scope': condition_scope,
                'terms': terms,
                'metric': metric,
                'runbook_url': runbook_url,
            }
        }

        if metric == 'user_defined':
            if user_defined:
                data['condition']['user_defined'] = user_defined
            else:
                raise ConfigurationException(
                    'Metric is set as user_defined but no user_defined config specified'
                )

        return self._post(
            url='{0}alerts_conditions/policies/{1}.json'.format(self.URL, policy_id),
            headers=self.headers,
            data=data
        )

    def delete(self, alert_condition_id):
        """
        This API endpoint allows you to delete an alert condition

        :type alert_condition_id: integer
        :param alert_condition_id: Alert Condition ID

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "condition": {
                    "id": "integer",
                    "type": "string",
                    "condition_scope":  "string",
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

        return self._delete(
            url='{0}alerts_conditions/{1}.json'.format(self.URL, alert_condition_id),
            headers=self.headers
        )
