from collections import OrderedDict
from unittest import TestCase

from mock import patch, Mock
import requests

from newrelic_api.servers import Servers


class NRServersTests(TestCase):
    def setUp(self):
        super(NRServersTests, self).setUp()
        self.server = Servers(api_key='dummy_key')

        server_response = {
            "id": 1234567,
            "account_id": 12345,
            "name": "ip-10-0-13-182",
            "host": "ip-10-0-13-182",
            "reporting": True,
            "last_reported_at": "2014-06-24T18:52:09+00:00",
            "summary": {
                "cpu": 14.1,
                "cpu_stolen": 0,
                "disk_io": 0.07,
                "memory": 69,
                "memory_used": 2712666112,
                "memory_total": 3932160000,
                "fullest_disk": 30.7,
                "fullest_disk_free": 5724000000
            }
        }
        self.list_success_response = {
            'servers': [
                server_response,
            ],
        }

        self.show_success_response = {
            'server': server_response,
        }

        self.metric_name_response = {
            "metrics": [
                {
                    "name": "Agent/MetricsReported/count",
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
                    ]
                },
                {
                    "name": "ProcessSamples/messagebus/dbus-daemon",
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
                    ]
                }
            ]
        }

        self.metric_data_response = {
            "metric_data": {
                "from": "2014-06-24T19:41:47+00:00",
                "to": "2014-06-24T20:11:47+00:00",
                "metrics": [
                    {
                        "name": "Agent/MetricsReported/count",
                        "timeslices": [
                            {
                                "from": "2014-06-24T19:40:00+00:00",
                                "to": "2014-06-24T20:09:59+00:00",
                                "values": {
                                    "average_response_time": 76,
                                    "calls_per_minute": 1,
                                    "call_count": 30,
                                    "min_response_time": 76,
                                    "max_response_time": 76,
                                    "average_exclusive_time": 76,
                                    "average_value": 0.076,
                                    "requests_per_minute": 1,
                                    "standard_deviation": 0.0107
                                }
                            }
                        ]
                    }
                ]
            }
        }

    @patch.object(requests, 'get')
    def test_list_success(self, mock_get):
        """
        Test servers .list()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.list_success_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.server.list()

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_list_success_with_filter_ids(self, mock_get):
        """
        Test servers .list() with filter_ids
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.list_success_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.server.list(filter_ids=[1234567])

        self.assertIsInstance(response, dict)
        mock_get.assert_called_once_with(
            url='https://api.newrelic.com/v2/servers.json',
            headers=self.server.headers,
            params='filter[ids]=1234567'
        )

    @patch.object(requests, 'get')
    def test_list_success_with_filter_labels(self, mock_get):
        """
        Test servers .list() with filter_labels
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.list_success_response
        mock_get.return_value = mock_response

        # Call the method
        # Use ordered dict to guarantee ordering of labels in query param
        labels = OrderedDict((('Type1', 'Value1'), ('Type2', 'Value2')))
        response = self.server.list(filter_labels=labels)

        self.assertIsInstance(response, dict)
        mock_get.assert_called_once_with(
            url='https://api.newrelic.com/v2/servers.json',
            headers=self.server.headers,
            params='filter[labels]=Type1:Value1;Type2:Value2'
        )

    @patch.object(requests, 'get')
    def test_list_failure(self, mock_get):
        """
        Test servers .list() failure case
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.server.list()

    @patch.object(requests, 'get')
    def test_show_success(self, mock_get):
        """
        Test servers .show() success
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.show_success_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.server.show(id=1234567)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_show_failure(self, mock_get):
        """
        Test servers .show() failure
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.server.show(id=1234567)

    @patch.object(requests, 'get')
    @patch.object(requests, 'put')
    def test_update_success(self, mock_put, mock_get):
        """
        Test servers .update() success
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.show_success_response
        mock_get.return_value = mock_response
        mock_put.return_value = mock_response

        # Call the method
        response = self.server.update(id=1234568, name='New Name')

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    @patch.object(requests, 'put')
    def test_update_failure(self, mock_put, mock_get):
        """
        Test servers .update() failure
        """
        mock_response1 = Mock(name='response')
        mock_response1.json.return_value = self.show_success_response
        mock_get.return_value = mock_response1

        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_put.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.server.update(id=1234567)

    @patch.object(requests, 'delete')
    def test_delete_success(self, mock_delete):
        """
        Test servers .delete() success
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.show_success_response
        mock_delete.return_value = mock_response

        # Call the method
        response = self.server.delete(id=1234567)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'delete')
    def test_delete_failure(self, mock_delete):
        """
        Test servers .delete() failure
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_delete.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.server.delete(id=1234567)

    @patch.object(requests, 'get')
    def test_metric_names(self, mock_get):
        """
        Test servers .metric_names()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.metric_name_response
        mock_get.return_value = mock_response

        response = self.server.metric_names(id=1234567)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_metric_data_without_values(self, mock_get):
        """
        Test servers .metric_data() without values param
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.metric_data_response
        mock_get.return_value = mock_response

        response = self.server.metric_data(id=1234567, names=['Agent/MetricsReported/count'], summarize=True)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_metric_data_with_values(self, mock_get):
        """
        Test servers .metric_data() with values param
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.metric_data_response
        mock_get.return_value = mock_response

        response = self.server.metric_data(
            id=1234567,
            names=['Agent/MetricsReported/count'],
            values=['call_count'],
            summarize=True
        )

        self.assertIsInstance(response, dict)
