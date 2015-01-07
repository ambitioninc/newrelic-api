import json
from unittest import TestCase

from mock import patch, Mock
import requests

from newrelic_api.alert_policies import AlertPolicies


class NRAlertPoliciesTests(TestCase):
    def setUp(self):
        super(NRAlertPoliciesTests, self).setUp()
        self.policies = AlertPolicies(api_key='dummy_key')

        self.policies_list_response = {
            "alert_policies": [
                {
                    "id": 12345,
                    "type": "server",
                    "name": "Default Server Policy",
                    "enabled": True,
                    "conditions": [
                        {
                            "id": 347535,
                            "type": "disk_io",
                            "severity": "caution",
                            "threshold": 70,
                            "trigger_minutes": 20,
                            "enabled": True
                        },
                        {
                            "id": 347536,
                            "type": "disk_io",
                            "severity": "critical",
                            "threshold": 90,
                            "trigger_minutes": 15,
                            "enabled": True
                        },
                        {
                            "id": 347537,
                            "type": "fullest_disk",
                            "severity": "caution",
                            "threshold": 70,
                            "trigger_minutes": 10,
                            "enabled": True
                        },
                        {
                            "id": 347538,
                            "type": "fullest_disk",
                            "severity": "critical",
                            "threshold": 90,
                            "trigger_minutes": 5,
                            "enabled": True
                        },
                        {
                            "id": 347539,
                            "type": "memory",
                            "severity": "caution",
                            "threshold": 80,
                            "trigger_minutes": 10,
                            "enabled": True
                        },
                        {
                            "id": 347540,
                            "type": "memory",
                            "severity": "critical",
                            "threshold": 95,
                            "trigger_minutes": 5,
                            "enabled": True
                        },
                        {
                            "id": 347541,
                            "type": "cpu",
                            "severity": "caution",
                            "threshold": 60,
                            "trigger_minutes": 20,
                            "enabled": True
                        },
                        {
                            "id": 347542,
                            "type": "cpu",
                            "severity": "critical",
                            "threshold": 90,
                            "trigger_minutes": 15,
                            "enabled": True
                        },
                        {
                            "id": 347543,
                            "type": "server_downtime",
                            "severity": "downtime",
                            "trigger_minutes": 5,
                            "enabled": True
                        }
                    ],
                    "links": {
                        "notification_channels": [
                            333444
                        ],
                        "servers": [
                            1234567,
                            2345678,
                            3456789,
                            4567890,
                            5678901,
                            6789012
                        ]
                    }
                }
            ]
        }
        self.policy_show_response = {
            'alert_policy': self.policies_list_response['alert_policies'][0]
        }

    @patch.object(requests, 'get')
    def test_list_success(self, mock_get):
        """
        Test alert policies .list()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.policies_list_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.policies.list()

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_list_success_with_ids(self, mock_get):
        """
        Test alert policies .list() with filter_ids
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.policies_list_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.policies.list(filter_ids=[12345])

        self.assertIsInstance(response, dict)
        mock_get.assert_called_once_with(
            url='https://api.newrelic.com/v2/alert_policies.json',
            headers=self.policies.headers,
            params='filter[ids]=12345'
        )

    @patch.object(requests, 'get')
    def test_list_failure(self, mock_get):
        """
        Test alert policies .list() failure case
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.policies.list()

    @patch.object(requests, 'get')
    def test_show_success(self, mock_get):
        """
        Test alert policies .show() success
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.policy_show_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.policies.show(id=333112)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_show_failure(self, mock_get):
        """
        Test alert policies .show() failure
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.policies.show(id=333114)

    @patch.object(requests, 'put')
    def test_update(self, mock_put):
        """
        Test alert policies .update() calls put with correct parameters
        """
        self.policies.update(id=333114, policy_update=self.policy_show_response)

        mock_put.assert_called_once_with(
            url='https://api.newrelic.com/v2/alert_policies/333114.json',
            headers=self.policies.headers,
            data=json.dumps(self.policy_show_response)
        )
