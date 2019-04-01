from unittest import TestCase

from mock import patch, Mock
import requests

from newrelic_api.alert_conditions import AlertConditions
from newrelic_api.exceptions import NoEntityException, ConfigurationException


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
                    "condition_scope": "application",
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
                    ],
                    "runbook_url": "http://example.com/"
                }
            ]
        }

        self.single_success_response = {
            "condition": {
                "id": "100",
                "type": "servers_metric",
                "name": "CPU usage alert",
                "condition_scope": "application",
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
                ],
                "runbook_url": "http://example.com/"
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
        mock_update_response.json.return_value = self.single_success_response
        mock_get.return_value = mock_list_response
        mock_put.return_value = mock_update_response

        response = self.alert_conditions.update(
            alert_condition_id=100,
            policy_id=1,
            name='New Name',
            type='servers_metric',
            condition_scope='application',
            entities=['1234567'],
            metric='cpu_percentage',
            runbook_url='http://example.com/',
            terms=[{
                "duration": "5",
                "operator": "above",
                "priority": "above",
                "threshold": "90",
                "time_function": "all"
            }]
        )

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

        with self.assertRaises(NoEntityException):
            self.alert_conditions.update(
                alert_condition_id=1000,
                policy_id=1
            )

        with self.assertRaises(ConfigurationException):
            self.alert_conditions.update(
                alert_condition_id=100,
                policy_id=1,
                metric='user_defined'
            )

        with self.assertRaises(ValueError):
            self.alert_conditions.update(
                alert_condition_id=100,
                policy_id=1
            )

    @patch.object(requests, 'get')
    @patch.object(requests, 'put')
    def test_update_no_alert_condition(self, mock_put, mock_get):
        """
        Test alerts_conditions .update() success
        """
        mock_list_response = Mock(name='response')
        mock_list_response.json.return_value = self.list_success_response
        mock_update_response = Mock(name='response')
        mock_update_response.json.return_value = self.single_success_response
        mock_get.return_value = mock_list_response
        mock_put.return_value = mock_update_response

        with self.assertRaises(NoEntityException):
            # Call the method with non existing alert_condition_id
            self.alert_conditions.update(
                alert_condition_id=9999,
                policy_id=1
            )

    @patch.object(requests, 'post')
    def test_create_success(self, mock_post):
        """
        Test alerts_conditions .update() success
        """
        mock_create_response = Mock(name='response')
        mock_create_response.json.return_value = self.single_success_response
        mock_post.return_value = mock_create_response

        # Call the method
        response = self.alert_conditions.create(
            policy_id=1,
            name='New Name',
            type='servers_metric',
            condition_scope='application',
            entities=['1234567'],
            metric='cpu_percentage',
            runbook_url='http://example.com/',
            terms=[{
                "duration": "5",
                "operator": "above",
                "priority": "above",
                "threshold": "90",
                "time_function": "all"
            }]
        )

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'delete')
    def test_delete_success(self, mock_delete):
        """
        Test alert policies .delete() success
        """

        self.alert_conditions.delete(alert_condition_id=100)

        mock_delete.assert_called_once_with(
            url='https://api.newrelic.com/v2/alerts_conditions/100.json',
            headers=self.alert_conditions.headers
        )
