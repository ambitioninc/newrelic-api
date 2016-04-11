from unittest import TestCase

from mock import patch, Mock
import requests

from newrelic_api.alert_conditions import AlertConditions
from newrelic_api.exceptions import NoEntityException


class NRAlertConditionsTests(TestCase):
    def setUp(self):
        super(NRAlertConditionsTests, self).setUp()
        self.alert_conditions = AlertConditions(api_key='dummy_key')

        self.list_success_response = {
            "conditions": [
                {
                    "id": "100",
                    "type": "servers_metric",
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

        self.update_success_response = {
            "condition": {
                "id": "100",
                "type": "servers_metric",
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
        }

    @patch.object(requests, 'get')
    def test_list_success(self, mock_get):
        """
        Test alert conditions .list()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.list_success_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.alert_conditions.list(policy_id=1)

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
            self.alert_conditions.list(policy_id=1)

    @patch.object(requests, 'get')
    @patch.object(requests, 'put')
    def test_update_success(self, mock_put, mock_get):
        """
        Test alerts_conditions .update() success
        """
        mock_list_response = Mock(name='response')
        mock_list_response.json.return_value = self.list_success_response
        mock_update_response = Mock(name='response')
        mock_update_response.json.return_value = self.update_success_response
        mock_get.return_value = mock_list_response
        mock_put.return_value = mock_update_response

        # Call the method
        response = self.alert_conditions.update(policy_id=1, alert_condition_id=100, name='New Name')

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    @patch.object(requests, 'put')
    def test_update_failure(self, mock_put, mock_get):
        """
        Test alerts_conditions .update() failure
        """
        mock_list_response = Mock(name='response')
        mock_list_response.json.return_value = self.list_success_response
        mock_update_response = Mock(name='response')
        mock_update_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_list_response
        mock_put.return_value = mock_update_response

        # Call the method
        with self.assertRaises(ValueError):
            self.alert_conditions.update(policy_id=1, alert_condition_id=100, name='New Name')

    @patch.object(requests, 'get')
    @patch.object(requests, 'put')
    def test_update_no_alert_condition(self, mock_put, mock_get):
        """
        Test alerts_conditions .update() success
        """
        mock_list_response = Mock(name='response')
        mock_list_response.json.return_value = self.list_success_response
        mock_update_response = Mock(name='response')
        mock_update_response.json.return_value = self.update_success_response
        mock_get.return_value = mock_list_response
        mock_put.return_value = mock_update_response

        with self.assertRaises(NoEntityException):
            # Call the method with non existing alert_condition_id
            self.alert_conditions.update(policy_id=1, alert_condition_id=9999, name='New Name')
