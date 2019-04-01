from unittest import TestCase

from mock import patch, Mock
import requests

from newrelic_api.alert_conditions_nrql import AlertConditionsNRQL
from newrelic_api.exceptions import NoEntityException


class NRAlertConditionsNRQLTests(TestCase):
    def setUp(self):
        super(NRAlertConditionsNRQLTests, self).setUp()
        self.alert_conditions_nrql = AlertConditionsNRQL(api_key='dummy_key')

        self.list_success_response = {
            "nrql_conditions": [
                {
                    "type": "static",
                    "id": 100,
                    "name": "5xx alert",
                    "enabled": True,
                    "value_function": "single_value",
                    "terms": [
                        {
                            "duration": "15",
                            "operator": "above",
                            "priority": "critical",
                            "threshold": "10",
                            "time_function": "all"
                        }
                    ],
                    "nrql": {
                            "query": "SELECT something WHERE something  = 'somevalue'",
                            "since_value": "3"
                        }
                    }
                ]
            }

        self.single_success_response = {
            "nrql_condition": {
                "type": "static",
                "id": 100,
                "name": "5xx alert",
                "enabled": True,
                "value_function": "single_value",
                "terms": [
                    {
                        "duration": "15",
                        "operator": "above",
                        "priority": "critical",
                        "threshold": "10",
                        "time_function": "all"
                    }
                ],
                "nrql": {
                        "query": "SELECT something WHERE something  = 'somevalue'",
                        "since_value": "3"
                    }
                }
            }

    @patch.object(requests, 'get')
    def test_list_success(self, mock_get):
        """
        Test alert conditions nrql .list()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.list_success_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.alert_conditions_nrql.list(policy_id=1)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_list_failure(self, mock_get):
        """
        Test alert conditions nrql .list() failure case
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.alert_conditions_nrql.list(policy_id=1)

    @patch.object(requests, 'get')
    @patch.object(requests, 'put')
    def test_update_success(self, mock_put, mock_get):
        """
        Test alert_conditions_nrql .update() success
        """
        mock_list_response = Mock(name='response')
        mock_list_response.json.return_value = self.list_success_response
        mock_update_response = Mock(name='response')
        mock_update_response.json.return_value = self.single_success_response
        mock_get.return_value = mock_list_response
        mock_put.return_value = mock_update_response

        # Call the method
        response = self.alert_conditions_nrql.update(
            alert_condition_nrql_id=100,
            policy_id=1,
            name='New Name',
            threshold_type='static',
            query="SELECT something WHERE something  = 'somevalue'",
            since_value='3',
            runbook_url='http://example.com/',
            value_function='single_value',
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
        Test alert_conditions_nrql .update() failure
        """
        mock_list_response = Mock(name='response')
        mock_list_response.json.return_value = self.list_success_response
        mock_update_response = Mock(name='response')
        mock_update_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_list_response
        mock_put.return_value = mock_update_response

        # Call the method
        with self.assertRaises(ValueError):
            self.alert_conditions_nrql.update(
                alert_condition_nrql_id=100,
                policy_id=1
            )

    @patch.object(requests, 'get')
    @patch.object(requests, 'put')
    def test_update_no_alert_condition(self, mock_put, mock_get):
        """
        Test alert_conditions_nrql .update() success
        """
        mock_list_response = Mock(name='response')
        mock_list_response.json.return_value = self.list_success_response
        mock_update_response = Mock(name='response')
        mock_update_response.json.return_value = self.single_success_response
        mock_get.return_value = mock_list_response
        mock_put.return_value = mock_update_response

        with self.assertRaises(NoEntityException):
            # Call the method with non existing alert_condition_nrql_id
            self.alert_conditions_nrql.update(
                alert_condition_nrql_id=9999,
                policy_id=1
            )

    @patch.object(requests, 'post')
    def test_create_success(self, mock_post):
        """
        Test alert_conditions_nrql .update() success
        """
        mock_create_response = Mock(name='response')
        mock_create_response.json.return_value = self.single_success_response
        mock_post.return_value = mock_create_response

        # Call the method
        response = self.alert_conditions_nrql.create(
            policy_id=1,
            name='New Name',
            threshold_type='static',
            query="SELECT something WHERE something  = 'somevalue'",
            since_value='3',
            runbook_url='http://example.com/',
            value_function='single_value',
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

        self.alert_conditions_nrql.delete(alert_condition_nrql_id=100)

        mock_delete.assert_called_once_with(
            url='https://api.newrelic.com/v2/alerts_nrql_conditions/100.json',
            headers=self.alert_conditions_nrql.headers
        )
