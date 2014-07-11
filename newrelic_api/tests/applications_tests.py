from unittest import TestCase

from mock import patch, Mock
import requests

from newrelic_api.applications import Applications


class NRApplicationsTests(TestCase):
    def setUp(self):
        super(NRApplicationsTests, self).setUp()
        self.app = Applications(api_key='dummy_key')

        app_response = {
            "id": 1234567,
            "name": "demo_site",
            "language": "python",
            "health_status": "green",
            "reporting": True,
            "last_reported_at": "2014-06-23T20:16:27+00:00",
            "application_summary": {
                "response_time": 170,
                "throughput": 3,
                "error_rate": 0,
                "apdex_target": 0,
                "apdex_score": 1
            },
            "settings": {
                "app_apdex_threshold": 0.5,
                "end_user_apdex_threshold": 7,
                "enable_real_user_monitoring": True,
                "use_server_side_config": False
            },
            "links": {
                "application_instances": [
                    2345678,
                    2345679
                ],
                "servers": [
                    4567890,
                    4567891
                ],
                "application_hosts": [
                    5678901,
                    5678902
                ]
            }
        }
        links = {
            "application.servers": "/v2/servers?ids={server_ids}",
            "application.server": "/v2/servers/{server_id}",
            "application.application_hosts": "/v2/application/{application_id}/hosts?ids={host_ids}",
            "application.application_host": "/v2/application/{application_id}/hosts/{host_id}",
            "application.application_instances": "/v2/application/{application_id}/instances?ids={instance_ids}",
            "application.application_instance": "/v2/application/{application_id}/instances/{instance_id}"
        }
        self.list_success_response = {
            'applications': [
                app_response,
            ],
            'links': links
        }

        self.show_success_response = {
            'application': app_response,
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

    @patch.object(requests, 'get')
    def test_list_success(self, mock_get):
        """
        Test applications .list()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.list_success_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.app.list()

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_list_success_with_filter_ids(self, mock_get):
        """
        Test applications .list()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.list_success_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.app.list(filter_ids=[1234567])

        self.assertIsInstance(response, dict)
        mock_get.assert_called_once_with(
            url='https://api.newrelic.com/v2/applications.json',
            headers=self.app.headers,
            params='filter[ids]=1234567'
        )

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
    @patch.object(requests, 'put')
    def test_update_success(self, mock_put, mock_get):
        """
        Test applications .update() success
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.show_success_response
        mock_get.return_value = mock_response
        mock_put.return_value = mock_response

        # Call the method
        response = self.app.update(id=1234567, name='New Name')

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    @patch.object(requests, 'put')
    def test_update_failure(self, mock_put, mock_get):
        """
        Test applications .update() failure
        """
        mock_response1 = Mock(name='response')
        mock_response1.json.return_value = self.show_success_response
        mock_get.return_value = mock_response1

        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_put.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.app.update(id=1234567)

    @patch.object(requests, 'delete')
    def test_delete_success(self, mock_delete):
        """
        Test applications .delete() success
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.show_success_response
        mock_delete.return_value = mock_response

        # Call the method
        response = self.app.delete(id=1234567)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'delete')
    def test_delete_failure(self, mock_delete):
        """
        Test applications .delete() failure
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_delete.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.app.delete(id=1234567)

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

        response = self.app.metric_data(id=1234567, names=['CPU/User Time'], values=['percent'], summarize=True)

        self.assertIsInstance(response, dict)
