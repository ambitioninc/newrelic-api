from .base import Resource


class AlertConditionsInfra(Resource):
    """
    Point to the NR Infra API
    """
    URL = 'https://infra-api.newrelic.com/v2/'

    """
    An interface for interacting with the NewRelic Alert Conditions Infra API.
    """
    def list(self, policy_id, limit=None, offset=None):
        """
        This API endpoint returns a paginated list of alert conditions for infrastucture
        metrics associated with the given policy_id.

        :type policy_id: int
        :param policy_id: Alert policy id

        :type limit: string
        :param limit: Max amount of results to return

        :type offset: string
        :param offset: Starting record to return

        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results

        ::

            {
                "data": [
                    {
                        "id": "integer",
                        "policy_id": "integer",
                        "type": "string",
                        "name": "string",
                        "enabled": "boolean",
                        "where_clause": "string",
                        "comparison": "string",
                        "filter": "hash",
                        "critical_threshold": "hash",
                        "process_where_clause": "string",
                        "created_at_epoch_millis": "time",
                        "updated_at_epoch_millis": "time"
                    }
                ],
                "meta": {
                    "limit": "integer",
                    "offset": "integer",
                    "total": "integer"
                }
            }

        """

        filters = [
            'policy_id={0}'.format(policy_id),
            'limit={0}'.format(limit) if limit else '50',
            'offset={0}'.format(offset) if offset else '0'
        ]

        return self._get(
            url='{0}alerts/conditions'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(filters)
        )

    def show(self, alert_condition_infra_id):
        """
        This API endpoint returns an alert condition for infrastucture, identified by its
        ID.

        :type alert_condition_infra_id: int
        :param alert_condition_infra_id: Alert Condition Infra ID

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "data": {
                    "id": "integer",
                    "policy_id": "integer",
                    "type": "string",
                    "name": "string",
                    "enabled": "boolean",
                    "where_clause": "string",
                    "comparison": "string",
                    "filter": "hash",
                    "critical_threshold": "hash",
                    "event_type": "string",
                    "process_where_clause": "string",
                    "created_at_epoch_millis": "time",
                    "updated_at_epoch_millis": "time"
                }
            }

        """
        return self._get(
            url='{0}alerts/conditions/{1}'.format(self.URL, alert_condition_infra_id),
            headers=self.headers,
        )

    def create(self, policy_id, name, condition_type, alert_condition_configuration, enabled=True):
        """
        This API endpoint allows you to create an alert condition for infrastucture

        :type policy_id: int
        :param policy_id: Alert policy id

        :type name: str
        :param name: The name of the alert condition

        :type condition_type: str
        :param condition_type: The type of the alert condition can be
            infra_process_running, infra_metric or infra_host_not_reporting

        :type alert_condition_configuration: hash
        :param alert_condition_configuration: hash containing config for the alert

        :type enabled: bool
        :param enabled: Whether to enable that alert condition

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "data": {
                    "id": "integer",
                    "policy_id": "integer",
                    "type": "string",
                    "name": "string",
                    "enabled": "boolean",
                    "where_clause": "string",
                    "comparison": "string",
                    "filter": "hash",
                    "critical_threshold": "hash",
                    "event_type": "string",
                    "process_where_clause": "string",
                    "created_at_epoch_millis": "time",
                    "updated_at_epoch_millis": "time"
                }
            }

        """

        data = {
            "data": alert_condition_configuration
        }

        data['data']['type'] = condition_type
        data['data']['policy_id'] = policy_id
        data['data']['name'] = name
        data['data']['enabled'] = enabled

        return self._post(
            url='{0}alerts/conditions'.format(self.URL),
            headers=self.headers,
            data=data
        )

    def update(self, alert_condition_infra_id, policy_id,
               name, condition_type, alert_condition_configuration, enabled=True):
        """
        This API endpoint allows you to update an alert condition for infrastucture

        :type alert_condition_infra_id: int
        :param alert_condition_infra_id: Alert Condition Infra ID

        :type policy_id: int
        :param policy_id: Alert policy id

        :type name: str
        :param name: The name of the alert condition

        :type condition_type: str
        :param condition_type: The type of the alert condition can be
            infra_process_running, infra_metric or infra_host_not_reporting

        :type alert_condition_configuration: hash
        :param alert_condition_configuration: hash containing config for the alert

        :type enabled: bool
        :param enabled: Whether to enable that alert condition

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "data": {
                    "id": "integer",
                    "policy_id": "integer",
                    "type": "string",
                    "name": "string",
                    "enabled": "boolean",
                    "where_clause": "string",
                    "comparison": "string",
                    "filter": "hash",
                    "critical_threshold": "hash",
                    "event_type": "string",
                    "process_where_clause": "string",
                    "created_at_epoch_millis": "time",
                    "updated_at_epoch_millis": "time"
                }
            }

        """

        data = {
            "data": alert_condition_configuration
        }

        data['data']['type'] = condition_type
        data['data']['policy_id'] = policy_id
        data['data']['name'] = name
        data['data']['enabled'] = enabled

        return self._put(
            url='{0}alerts/conditions/{1}'.format(self.URL, alert_condition_infra_id),
            headers=self.headers,
            data=data
        )

    def delete(self, alert_condition_infra_id):
        """
        This API endpoint allows you to delete an alert condition for infrastucture

        :type alert_condition_infra_id: integer
        :param alert_condition_infra_id: Alert Condition Infra ID

        :rtype: dict
        :return: The JSON response of the API

        ::

            {}

        """

        return self._delete(
            url='{0}alerts/conditions/{1}'.format(self.URL, alert_condition_infra_id),
            headers=self.headers
        )
