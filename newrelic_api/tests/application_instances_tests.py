from unittest import TestCase

from mock import patch, Mock
import requests

from newrelic_api.application_instances import ApplicationInstances


class NRApplicationInstancesTests(TestCase):
    def setUp(self):
        super(NRApplicationInstancesTests, self).setUp()
        self.app_instances = ApplicationInstances(api_key='dummy_key')

        app_response = {
            "id": 1234567,
            "application_name": "Developer Application",
            "host": "ip-10-1-19-12",
            "port": 0,
            "language": "python",
            "health_status": "green",
            "application_summary": {
                "response_time": 195,
                "throughput": 22.2,
                "error_rate": 0,
                "apdex_score": 0.98
            },
            "links": {
                "application": 2345678,
                "application_host": 3456789,
                "server": 4567890
            }
        }
        links = {
            "application_instance.application": "/v2/applications/{application_id}",
            "application_instance.application_host": "/v2/application/{application_id}/hosts/{instance_id}",
            "application_instance.server": "/v2/servers/{server_id}"
        }
        self.list_success_response = {
            'application_instances': [
                app_response,
            ],
            'links': links
        }

        self.show_success_response = {
            'application_instance': app_response,
            'links': links
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

        self.application_id = 1234567

    @patch.object(requests, 'get')
    def test_list_success(self, mock_get):
        """
        Test application instances .list()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.list_success_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.app_instances.list(application_id=2345678)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_list_success_with_filter_ids(self, mock_get):
        """
        Test application instances .list() with_filter_ids
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.list_success_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.app_instances.list(application_id=2345678, filter_ids=[1234567])

        self.assertIsInstance(response, dict)

        mock_get.assert_called_once_with(
            url='https://api.newrelic.com/v2/applications/2345678/instances.json',
            headers=self.app_instances.headers,
            params='filter[ids]=1234567'
        )

    @patch.object(requests, 'get')
    def test_list_failure(self, mock_get):
        """
        Test application instances .list() failure case
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.app_instances.list(application_id=1234567)

    @patch.object(requests, 'get')
    def test_show_success(self, mock_get):
        """
        Test application instances .show() success
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.show_success_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.app_instances.show(application_id=1234567, instance_id=2345678)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_show_failure(self, mock_get):
        """
        Test application instances .show() failure
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.app_instances.show(application_id=1234567, instance_id=2345678)

    @patch.object(requests, 'get')
    def test_metric_names(self, mock_get):
        """
        Test application instances .metric_names()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.metric_name_response
        mock_get.return_value = mock_response

        response = self.app_instances.metric_names(
            application_id=1234567,
            instance_id=2345678
        )

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_metric_data_without_values(self, mock_get):
        """
        Test application instances .metric_data() without a values param
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.metric_data_response
        mock_get.return_value = mock_response

        response = self.app_instances.metric_data(
            application_id=1234567,
            instance_id=2345678,
            names=['CPU/User Time'],
            summarize=True
        )

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_metric_data_with_values(self, mock_get):
        """
        Test application instances .metric_data() with a values param
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.metric_data_response
        mock_get.return_value = mock_response

        response = self.app_instances.metric_data(
            application_id=1234567,
            instance_id=2345678,
            names=['CPU/User Time'],
            values=['percent'],
            summarize=True
        )

        self.assertIsInstance(response, dict)
