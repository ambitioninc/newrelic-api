from unittest import TestCase

from mock import patch, Mock
import requests

from newrelic_api.components import Components


class NRComponentsTests(TestCase):
    def setUp(self):
        super(NRComponentsTests, self).setUp()
        self.components = Components(api_key='dummy_key')

        self.list_response = {
            "components": [
                {
                    "id": 2223333,
                    "name": "SendGrid",
                    "summary_metrics": []
                }
            ]
        }

        self.show_response = {
            'component': self.list_response['components'][0]
        }

        self.metric_name_response = {
            "metrics": [
                {
                    "name": "Component/Numeric/Compliance/Blocked[Emails/Day]",
                    "values": [
                        "average_value",
                        "min_value",
                        "max_value",
                        "sample_count",
                        "total_value"
                    ]
                },
            ]
        }

        self.metric_data_response = {
            "metric_data": {
                "from": "2014-06-28T16:15:30+00:00",
                "to": "2014-06-28T16:45:30+00:00",
                "metrics": [
                    {
                        "name": "Component/Numeric/Compliance/Blocked[Emails/Day]",
                        "timeslices": [
                            {
                                "from": "2014-06-28T16:14:00+00:00",
                                "to": "2014-06-28T16:43:59+00:00",
                                "values": {
                                    "average_value": 0,
                                    "min_value": 0,
                                    "max_value": 0,
                                    "sample_count": 5,
                                    "total_value": 0
                                }
                            }
                        ]
                    }
                ]
            }
        }

    @patch.object(requests, 'get')
    def test_list(self, mock_get):
        """
        Test components .list()
        """
        self.components.list(filter_name='SendGrid', page=0)

        mock_get.assert_called_once_with(
            url='https://api.newrelic.com/v2/components.json',
            headers=self.components.headers,
            params='filter[name]=SendGrid'
        )

    @patch.object(requests, 'get')
    def test_list_with_filter_ids(self, mock_get):
        """
        Test components .list() with filter_ids
        """
        self.components.list(filter_name='SendGrid', filter_ids=[2223333], page=0)

        mock_get.assert_called_once_with(
            url='https://api.newrelic.com/v2/components.json',
            headers=self.components.headers,
            params='filter[name]=SendGrid&filter[ids]=2223333'
        )

    @patch.object(requests, 'get')
    def test_show(self, mock_get):
        """
        Test components .show()
        """
        self.components.show(id=2223333)

        mock_get.assert_called_once_with(
            url='https://api.newrelic.com/v2/components/2223333.json',
            headers=self.components.headers,
        )

    @patch.object(requests, 'get')
    def test_metric_names(self, mock_get):
        """
        Test components .metric_names()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.metric_name_response
        mock_get.return_value = mock_response

        response = self.components.metric_names(id=2223333)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_metric_data_without_values(self, mock_get):
        """
        Test components .metric_data() without values param
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.metric_data_response
        mock_get.return_value = mock_response

        response = self.components.metric_data(
            id=2223333,
            names=['Component/Numeric/Compliance/Blocked[Emails/Day]'],
            summarize=True
        )

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_metric_data_with_values(self, mock_get):
        """
        Test components .metric_data() with values param
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.metric_data_response
        mock_get.return_value = mock_response

        response = self.components.metric_data(
            id=2223333,
            names=['Component/Numeric/Compliance/Blocked[Emails/Day]'],
            values=['average_value'],
            summarize=True
        )

        self.assertIsInstance(response, dict)
