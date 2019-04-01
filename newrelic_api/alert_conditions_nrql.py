from .base import Resource
from newrelic_api.exceptions import NoEntityException, ConfigurationException


class AlertConditionsNRQL(Resource):
    """
    An interface for interacting with the NewRelic Alert Conditions NRQL API.
    """
    def list(self, policy_id, page=None):
        """
        This API endpoint returns a paginated list of alert conditions NRQL associated with the
        given policy_id.

        This API endpoint returns a paginated list of the alert conditions NRQL
        associated with your New Relic account.

        :type policy_id: int
        :param policy_id: Alert policy id

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results

        ::
            {
            "nrql_conditions": [
                    {
                        "type": "string",
                        "id": "integer",
                        "name": "string",
                        "runbook_url": "string",
                        "enabled": "boolean",
                        "expected_groups": "integer",
                        "ignore_overlap": "boolean",
                        "value_function": "string",
                        "terms": [
                            {
                                "duration": "string",
                                "operator": "string",
                                "priority": "string",
                                "threshold": "string",
                                "time_function": "string"
                            }
                        ],
                        "nrql": {
                            "query": "string",
                            "since_value": "string"
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
            url='{0}alerts_nrql_conditions.json'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(filters)
        )

    def update(  # noqa: C901
            self, alert_condition_nrql_id, policy_id, name=None, threshold_type=None, query=None,
            since_value=None, terms=None, expected_groups=None, value_function=None,
            runbook_url=None, ignore_overlap=None, enabled=True):
        """
        Updates any of the optional parameters of the alert condition nrql

        :type alert_condition_nrql_id: int
        :param alert_condition_nrql_id: Alerts condition NRQL id to update

        :type policy_id: int
        :param policy_id: Alert policy id where target alert condition belongs to

        :type condition_scope: str
        :param condition_scope: The scope of the condition, can be instance or application

        :type name: str
        :param name: The name of the alert

        :type threshold_type: str
        :param threshold_type: The tthreshold_typeype of the condition, can be static or outlier

        :type query: str
        :param query: nrql query for the alerts

        :type since_value: str
        :param since_value: since value for the alert

        :type terms: list[hash]
        :param terms: list of hashes containing threshold config for the alert

        :type expected_groups: int
        :param expected_groups: expected groups setting for outlier alerts

        :type value_function: str
        :param type: value function for static alerts

        :type runbook_url: str
        :param runbook_url: The url of the runbook

        :type ignore_overlap: bool
        :param ignore_overlap: Whether to ignore overlaps for outlier alerts

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
            "nrql_condition": {
                "name": "string",
                "runbook_url": "string",
                "enabled": "boolean",
                "expected_groups": "integer",
                "ignore_overlap": "boolean",
                "value_function": "string",
                "terms": [
                    {
                        "duration": "string",
                        "operator": "string",
                        "priority": "string",
                        "threshold": "string",
                        "time_function": "string"
                    }
                ],
                "nrql": {
                    "query": "string",
                    "since_value": "string"
                }
            }
        }
        """

        conditions_nrql_dict = self.list(policy_id)
        target_condition_nrql = None
        for condition in conditions_nrql_dict['nrql_conditions']:
            if int(condition['id']) == alert_condition_nrql_id:
                target_condition_nrql = condition
                break

        if target_condition_nrql is None:
            raise NoEntityException(
                'Target alert condition nrql is not included in that policy.'
                'policy_id: {}, alert_condition_nrql_id {}'.format(
                    policy_id,
                    alert_condition_nrql_id
                )
            )

        data = {
            'nrql_condition': {
                'type': threshold_type or target_condition_nrql['type'],
                'enabled': target_condition_nrql['enabled'],
                'name': name or target_condition_nrql['name'],
                'terms': terms or target_condition_nrql['terms'],
                'nrql': {
                    'query': query or target_condition_nrql['nrql']['query'],
                    'since_value': since_value or target_condition_nrql['nrql']['since_value'],
                }
            }
        }

        if enabled is not None:
            data['nrql_condition']['enabled'] = str(enabled).lower()

        if runbook_url is not None:
            data['nrql_condition']['runbook_url'] = runbook_url
        elif 'runbook_url' in target_condition_nrql:
            data['nrql_condition']['runbook_url'] = target_condition_nrql['runbook_url']

        if expected_groups is not None:
            data['nrql_condition']['expected_groups'] = expected_groups
        elif 'expected_groups' in target_condition_nrql:
            data['nrql_condition']['expected_groups'] = target_condition_nrql['expected_groups']

        if ignore_overlap is not None:
            data['nrql_condition']['ignore_overlap'] = ignore_overlap
        elif 'ignore_overlap' in target_condition_nrql:
            data['nrql_condition']['ignore_overlap'] = target_condition_nrql['ignore_overlap']

        if value_function is not None:
            data['nrql_condition']['value_function'] = value_function
        elif 'value_function' in target_condition_nrql:
            data['nrql_condition']['value_function'] = target_condition_nrql['value_function']

        if data['nrql_condition']['type'] == 'static':
            if 'value_function' not in data['nrql_condition']:
                raise ConfigurationException(
                    'Alert is set as static but no value_function config specified'
                )
            data['nrql_condition'].pop('expected_groups', None)
            data['nrql_condition'].pop('ignore_overlap', None)

        elif data['nrql_condition']['type'] == 'outlier':
            if 'expected_groups' not in data['nrql_condition']:
                raise ConfigurationException(
                    'Alert is set as outlier but expected_groups config is not specified'
                )
            if 'ignore_overlap' not in data['nrql_condition']:
                raise ConfigurationException(
                    'Alert is set as outlier but ignore_overlap config is not  specified'
                )
            data['nrql_condition'].pop('value_function', None)

        return self._put(
            url='{0}alerts_nrql_conditions/{1}.json'.format(self.URL, alert_condition_nrql_id),
            headers=self.headers,
            data=data
        )

    def create(
            self, policy_id, name, threshold_type, query, since_value, terms,
            expected_groups=None, value_function=None, runbook_url=None,
            ignore_overlap=None, enabled=True):
        """
        Creates an alert condition nrql

        :type policy_id: int
        :param policy_id: Alert policy id where target alert condition nrql belongs to

        :type name: str
        :param name: The name of the alert

        :type threshold_type: str
        :param type: The threshold_type of the condition, can be static or outlier

        :type query: str
        :param query: nrql query for the alerts

        :type since_value: str
        :param since_value: since value for the alert

        :type terms: list[hash]
        :param terms: list of hashes containing threshold config for the alert

        :type expected_groups: int
        :param expected_groups: expected groups setting for outlier alerts

        :type value_function: str
        :param type: value function for static alerts

        :type runbook_url: str
        :param runbook_url: The url of the runbook

        :type ignore_overlap: bool
        :param ignore_overlap: Whether to ignore overlaps for outlier alerts

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
            "nrql_condition": {
                "name": "string",
                "runbook_url": "string",
                "enabled": "boolean",
                "expected_groups": "integer",
                "ignore_overlap": "boolean",
                "value_function": "string",
                "terms": [
                    {
                        "duration": "string",
                        "operator": "string",
                        "priority": "string",
                        "threshold": "string",
                        "time_function": "string"
                    }
                ],
                "nrql": {
                    "query": "string",
                    "since_value": "string"
                }
            }
        }
        """

        data = {
            'nrql_condition': {
                'type': threshold_type,
                'name': name,
                'enabled': enabled,
                'terms': terms,
                'nrql': {
                    'query': query,
                    'since_value': since_value
                }
            }
        }

        if runbook_url is not None:
            data['nrql_condition']['runbook_url'] = runbook_url

        if expected_groups is not None:
            data['nrql_condition']['expected_groups'] = expected_groups

        if ignore_overlap is not None:
            data['nrql_condition']['ignore_overlap'] = ignore_overlap

        if value_function is not None:
            data['nrql_condition']['value_function'] = value_function

        if data['nrql_condition']['type'] == 'static':
            if 'value_function' not in data['nrql_condition']:
                raise ConfigurationException(
                    'Alert is set as static but no value_function config specified'
                )
            data['nrql_condition'].pop('expected_groups', None)
            data['nrql_condition'].pop('ignore_overlap', None)

        elif data['nrql_condition']['type'] == 'outlier':
            if 'expected_groups' not in data['nrql_condition']:
                raise ConfigurationException(
                    'Alert is set as outlier but expected_groups config is not specified'
                )
            if 'ignore_overlap' not in data['nrql_condition']:
                raise ConfigurationException(
                    'Alert is set as outlier but ignore_overlap config is not  specified'
                )
            data['nrql_condition'].pop('value_function', None)

        return self._post(
            url='{0}alerts_nrql_conditions/policies/{1}.json'.format(self.URL, policy_id),
            headers=self.headers,
            data=data
        )

    def delete(self, alert_condition_nrql_id):
        """
        This API endpoint allows you to delete an alert condition nrql

        :type alert_condition_nrql_id: integer
        :param alert_condition_nrql_id: Alert Condition ID

        :rtype: dict
        :return: The JSON response of the API

        ::
        {
            "nrql_condition": {
                "type": "string",
                "id": "integer",
                "name": "string",
                "runbook_url": "string",
                "enabled": "boolean",
                "expected_groups": "integer",
                "ignore_overlap": "boolean",
                "value_function": "string",
                "terms": [
                    {
                        "duration": "string",
                        "operator": "string",
                        "priority": "string",
                        "threshold": "string",
                        "time_function": "string"
                    }
                ],
                "nrql": {
                    "query": "string",
                    "since_value": "string"
                }
            }
        }

        """

        return self._delete(
            url='{0}alerts_nrql_conditions/{1}.json'.format(self.URL, alert_condition_nrql_id),
            headers=self.headers
        )
