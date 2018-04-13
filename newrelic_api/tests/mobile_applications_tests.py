from unittest import TestCase

from mock import patch, Mock
import requests

from newrelic_api.mobile_applications import MobileApplications


class NRMobileApplicationsTests(TestCase):
    def setUp(self):
        super(NRMobileApplicationsTests, self).setUp()
        self.app = MobileApplications(api_key='dummy_key')

        app_response = {
            "id": 123456,
            "name": "SampleApp",
            "health_status": "green",
            "reporting": True,
            "mobile_summary": {
                "active_users": 9792,
                "launch_count": 9792,
                "throughput": 71200,
                "response_time": 0.428,
                "calls_per_session": 7.27,
                "interaction_time": 0.298,
                "failed_call_rate": 1.2271918170353238,
                "remote_error_rate": 0.10091960945281904
            },
            "crash_summary": {
                "supports_crash_data": True,
                "unresolved_crash_count": 0,
                "crash_count": 0,
                "crash_rate": 0
            }
        }

        self.list_success_response = {
            'applications': [
                app_response,
            ]
        }

        self.show_success_response = {
            'application': app_response
        }

        self.metric_name_response = {
            "metrics": [
                {
                    "values": [
                        "average_response_time",
                        "calls_per_minute",
                        "call_count",
                        "min_response_time",
                        "max_response_time",
                        "average_exclusive_time",
                        "average_value",
                        "requests_per_minute",
                        "standard_deviation"
                    ],
                    "name": "Agent/MetricsReported/count"
                },
                {
                    "values": [
                        "s",
                        "t",
                        "f",
                        "count",
                        "score",
                        "value",
                        "threshold",
                        "threshold_min"
                    ],
                    "name": "Apdex"
                }
            ]
        }
        self.metric_data_response = {
            "metric_data": {
                "metrics": [
                    {
                        "timeslices": [
                            {
                                "values": {
                                    "total_time": 15700,
                                    "percent": 0.871,
                                    "average_time": 180
                                },
                                "to": "2014-06-24T19:42:59+00:00",
                                "from": "2014-06-24T19:13:00+00:00"
                            }
                        ],
                        "name": "CPU/User Time"
                    }
                ],
                "to": "2014-06-24T19:44:29+00:00",
                "from": "2014-06-24T19:14:29+00:00"
            }
        }

    @patch.object(requests, 'get')
    def test_list_success(self, mock_get):
        """
        Test mobile_applications .list()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.list_success_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.app.list()

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_list_failure(self, mock_get):
        """
        Test applications .list() failure case
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.app.list()

    @patch.object(requests, 'get')
    def test_show_success(self, mock_get):
        """
        Test applications .show() success
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.show_success_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.app.show(id=1234567)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_show_failure(self, mock_get):
        """
        Test applications .show() failure
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.app.show(id=1234567)

    @patch.object(requests, 'get')
    def test_metric_names(self, mock_get):
        """
        Test applications .metric_names()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.metric_name_response
        mock_get.return_value = mock_response

        response = self.app.metric_names(id=1234567)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_metric_data_without_values(self, mock_get):
        """
        Test applications .metric_data() without a values param
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.metric_data_response
        mock_get.return_value = mock_response

        response = self.app.metric_data(id=1234567, names=['CPU/User Time'], summarize=True)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_metric_data_with_values(self, mock_get):
        """
        Test applications .metric_data() with a values param
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.metric_data_response
        mock_get.return_value = mock_response

        response = self.app.metric_data(id=1234567,
                                        names=['CPU/User Time'],
                                        values=['percent'],
                                        summarize=True,
                                        period=60)

        self.assertIsInstance(response, dict)
