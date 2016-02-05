from unittest import TestCase

from mock import patch, Mock
import requests

from newrelic_api.alert_conditions import AlertConditions


class NRAlertConditionsTests(TestCase):
    def setUp(self):
        super(NRAlertConditionsTests, self).setUp()
        self.conditions = AlertConditions(api_key='dummy_key')

        self.conditions_list_response = {
            "conditions": [
                {
                    "id": "1",
                    "condition_type": "servers_metric",
                    "name": "CPU usage alert",
                    "enabled": True,
                    "entities": [
                        "1234567"
                    ],
                    "metric": "cpu_percentage",
                    "terms": [
                        {
                            "duration": "5",
                            "operator": "above",
                            "priority": "above",
                            "threshold": "90",
                            "time_function": "all"
                        }
                    ]
                }
            ]
        }

    @patch.object(requests, 'get')
    def test_list_success(self, mock_get):
        """
        Test alert conditions .list()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.conditions_list_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.conditions.list(policy_id=1)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_list_failure(self, mock_get):
        """
        Test alert conditions .list() failure case
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.conditions.list(policy_id=1)
