from unittest import TestCase

from mock import patch, Mock
import requests

from newrelic_api.alert_policies import AlertPolicies


class NRAlertPoliciesTests(TestCase):
    def setUp(self):
        super(NRAlertPoliciesTests, self).setUp()
        self.policies = AlertPolicies(api_key='dummy_key')

        self.policies_list_response = {
            "policies": [
                {
                    "id": 12345,
                    "rollup_strategy": "PER_CONDITION_AND_TARGET",
                    "name": "Default Server Policy",
                    "created_at": 123456789012,
                }
            ]
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
    def test_list_success_with_name(self, mock_get):
        """
        Test alert policies .list() with filter_ids
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.policies_list_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.policies.list(filter_name='Default Server Policy')

        self.assertIsInstance(response, dict)
        mock_get.assert_called_once_with(
            url='https://api.newrelic.com/v2/alerts_policies.json',
            headers=self.policies.headers,
            params='filter[name]=Default Server Policy'
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
