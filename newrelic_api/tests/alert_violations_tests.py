from unittest import TestCase

from mock import patch, Mock
import requests
import datetime

from newrelic_api.alert_violations import AlertViolations


class NRAlertViolationsTests(TestCase):
    def setUp(self):
        super(NRAlertViolationsTests, self).setUp()
        self.violation = AlertViolations(api_key='dummy_key')

        self.violations_list_response = {
            "violations": [
                {
                    "id": 12345,
                    "label": "Violation of Default Server Policy",
                    "duration": 100,
                    "policy_name": "Default Server Policy",
                    "condition_name": "CPU usage alert",
                    "priority": "Warning",
                    "opened_at": 123456789012,
                    "entity": {
                        "product": "Apm",
                        "type": "Application",
                        "group_id": 123456,
                        "id": 1234567,
                        "name": "Developer Application"
                    },
                    "links": {
                        "policy_id": 12345,
                        "condition_id": 100
                    }
                }
            ]
        }

    @patch.object(requests, 'get')
    def test_list_success(self, mock_get):
        """
        Test alert violations .list()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.violations_list_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.violation.list()

        self.assertIsInstance(response, dict)
        mock_get.assert_called_once_with(
            url='https://api.newrelic.com/v2/alerts_violations.json',
            headers=self.violation.headers,
            params=''
        )

    @patch.object(requests, 'get')
    def test_list_success_with_filters(self, mock_get):
        """
        Test alert viollations .list() with filters
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.violations_list_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.violation.list(
            filter_start_date=datetime.datetime(2000, 1, 1, 12, 0, 0, 0),
            filter_end_date=datetime.datetime(2010, 1, 1, 12, 0, 0, 0),
            filter_only_open=True,
            page=1
        )

        self.assertIsInstance(response, dict)
        mock_get.assert_called_once_with(
            url='https://api.newrelic.com/v2/alerts_violations.json',
            headers=self.violation.headers,
            params='start_date=2000-01-01T12:00:00+00:00&end_date=2010-01-01T12:00:00+00:00&only_open=true&page=1'
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
            self.violation.list()
