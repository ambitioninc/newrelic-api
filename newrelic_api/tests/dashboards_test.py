from unittest import TestCase

from mock import patch, Mock
import requests

from newrelic_api.dashboards import Dashboards
from newrelic_api.exceptions import NewRelicAPIServerException


class NRDashboardsTests(TestCase):
    def setUp(self):
        super(NRDashboardsTests, self).setUp()
        self.dashboards = Dashboards(api_key='dummy_key')

        self.list_success_response = {
            'dashboards': [
                {
                    "id": 123456,
                    "title": "test-dashboard",
                    "description": "Test Dashboard",
                    "icon": "line-chart",
                    "created_at": "2018-09-06T12:13:14Z",
                    "updated_at": "2018-09-07T13:14:15Z",
                    "visibility": "owner",
                    "editable": "editable_by_owner",
                    "ui_url": "https://insights.newrelic.com/accounts/234567/dashboards/123456",
                    "api_url": "https://api.newrelic.com/v2/dashboards/123456",
                    "owner_email": "user@company.com",
                    "filter": {
                        "event_types": ["SystemSample"],
                        "attributes": ["environment"]
                    }
                }
            ]
        }

        self.single_success_response = {
            'dashboard': {
                "id": 123456,
                "title": "test-dashboard",
                "description": "Test Dashboard",
                "icon": "line-chart",
                "created_by": "2018-09-06T12:13:14Z",
                "updated_by": "2018-09-07T13:14:15Z",
                "visibility": "owner",
                "editable": "editable_by_owner",
                "ui_url": "https://insights.newrelic.com/accounts/234567/dashboards/123456",
                "api_url": "https://api.newrelic.com/v2/dashboards/123456",
                "owner_email": "user@company.com",
                "metadata": {
                    "version": 1
                },
                "widgets": [
                    {
                        "visualization": "faceted_line_chart",
                        "layout": {
                            "width": 1,
                            "height": 1,
                            "row": 1,
                            "column": 1
                        },
                        "widget_id": 654321,
                        "account_id": 234567,
                        "data": [
                            {
                                "nrql": "SELECT average(cpuPercent) from SystemSample FACET role"
                            }
                        ],
                        "presentation": {
                            "title": "CPU Utilization",
                            "notes": ""
                        }
                    }
                ],
                "filter": {
                    "event_types": ["SystemSample"],
                    "attributes": ["environment"]
                }
            }
        }

        self.delete_success_response = {
            'dashboard': {
                'id': 123456
            }
        }

    @patch.object(requests, 'get')
    def test_list_success(self, mock_get):
        """
        Tests dashboards .list() success
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.list_success_response
        mock_get.return_value = mock_response

        response = self.dashboards.list()

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_list_failure(self, mock_get):
        """
        Tests dashboards .list() failure
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            self.dashboards.list()

    @patch.object(requests, 'get')
    def test_show_success(self, mock_get):
        """
        Tests dashboards .show() success
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.single_success_response
        mock_get.return_value = mock_response

        response = self.dashboards.show(123456)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_show_failure(self, mock_get):
        """
        Tests dashboards .show() failure
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            self.dashboards.show(123456)

    @patch.object(requests, 'delete')
    def test_delete_success(self, mock_delete):
        """
        Tests dashboards .delete() success
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.delete_success_response
        mock_delete.return_value = mock_response

        response = self.dashboards.delete(123456)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'delete')
    def test_delete_failure(self, mock_delete):
        """
        Tests dashboards .delete() failure
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = NewRelicAPIServerException("New Relic API Exception")
        mock_delete.return_value = mock_response

        with self.assertRaises(NewRelicAPIServerException):
            self.dashboards.delete(123456)

    @patch.object(requests, 'post')
    def test_create_success(self, mock_post):
        """
        Test dashboards .create() success
        """
        mock_create_response = Mock(name='response')
        mock_create_response.json.return_value = self.single_success_response
        mock_post.return_value = mock_create_response

        response = self.dashboards.create(
            {
                "dashboard": {
                    "title": "test-dashboard",
                    "description": "Test Dashboard",
                    "icon": "line-chart",
                    "visibility": "owner",
                    "metadata": {
                        "version": 1
                    },
                    "widgets": [
                        {
                            "visualization": "faceted_line_chart",
                            "layout": {
                                "width": 1,
                                "height": 1,
                                "row": 1,
                                "column": 1
                            },
                            "account_id": 234567,
                            "data": [
                                {
                                    "nrql": "SELECT average(cpuPercent) FROM SystemSample FACET role"
                                }
                            ],
                            "presentation": {
                                "title": "CPU Utilization",
                                "notes": ""
                            }
                        }
                    ],
                    "filter": {
                        "event_types": ["SystemSample"],
                        "attributes": ["environment"]
                    }
                }
            }
        )

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'post')
    def test_create_failure(self, mock_post):
        """
        Test dashboards .create() failure
        """

    @patch.object(requests, 'put')
    def test_update_success(self, mock_put):
        """
        Test dashboards .update() success
        """
        mock_update_response = Mock(name='response')
        mock_update_response.json.return_value = self.single_success_response
        mock_put.return_value = mock_update_response

        response = self.dashboards.update(
            123456,
            {
                "dashboard": {
                    "title": "test-dashboard",
                    "description": "Test Dashboard",
                    "icon": "line-chart",
                    "visibility": "owner",
                    "metadata": {
                        "version": 1
                    },
                    "widgets": [
                        {
                            "visualization": "faceted_line_chart",
                            "layout": {
                                "width": 1,
                                "height": 1,
                                "row": 1,
                                "column": 1
                            },
                            "account_id": 234567,
                            "data": [
                                {
                                    "nrql": "SELECT average(cpuPercent) FROM SystemSample FACET role"
                                }
                            ],
                            "presentation": {
                                "title": "CPU Utilization",
                                "notes": ""
                            }
                        }
                    ],
                    "filter": {
                        "event_types": ["SystemSample"],
                        "attributes": ["environment"]
                    }
                }
            }
        )
        self.assertIsInstance(response, dict)

    @patch.object(requests, 'put')
    def test_update_failure(self, mock_put):
        """
        Test dashboards .update() failure
        """
        mock_update_response = Mock(name='response')
        mock_update_response.json.side_effect = NewRelicAPIServerException('No JSON object could be decoded')
        mock_put.return_value = mock_update_response

        with self.assertRaises(NewRelicAPIServerException):
            self.dashboards.update(
                123456,
                {
                    "dashboard": {
                        "title": "test-dashboard",
                        "description": "Test Dashboard",
                        "icon": "line-chart",
                        "visibility": "owner",
                        "metadata": {
                            "version": 1
                        },
                        "widgets": [
                            {
                                "visualization": "faceted_line_chart",
                                "layout": {
                                    "width": 1,
                                    "height": 1,
                                    "row": 1,
                                    "column": 1
                                },
                                "account_id": 234567,
                                "data": [
                                    {
                                        "nrql": "SELECT average(cpuPercent) FROM SystemSample FACET role"
                                    }
                                ],
                                "presentation": {
                                    "title": "CPU Utilization",
                                    "notes": ""
                                }
                            }
                        ],
                        "filter": {
                            "event_types": ["SystemSample"],
                            "attributes": ["environment"]
                        }
                    }
                }
            )
