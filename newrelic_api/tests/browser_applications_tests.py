from unittest import TestCase

from mock import patch, Mock
import requests

from newrelic_api.browser_applications import BrowserApplications


class NRBrowserApplicationsTests(TestCase):
    def setUp(self):
        super(NRBrowserApplicationsTests, self).setUp()
        self.browser_application = BrowserApplications(api_key='dummy_key')

        browser_application = {
            "id": 1234567,
            "name": "Account Global",
            "browser_monitoring_key": "313ed76e08",
            "loader_script": (
                "<script type=\"text/javascript\">"
                "\n</script>\n"
            )
        }
        self.list_success_response = {
            'browser_applications': [
                browser_application,
            ],
        }
        self.create_success_response = {
            'browser_application': browser_application,
        }

    @patch.object(requests, 'get')
    def test_list_success(self, mock_get):
        """
        Test browser_applications .list()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.list_success_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.browser_application.list()

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_list_success_with_filters(self, mock_get):
        """
        Test browser_applications .list()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.list_success_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.browser_application.list(filter_ids=[1234567], filter_name='Account Global', page=1)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_list_failure(self, mock_get):
        """
        Test browser_applications .list() failure case
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.browser_application.list()

    @patch.object(requests, 'post')
    def test_create_success(self, mock_post):
        """
        Test browser_applications .create() success
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.create_success_response
        mock_post.return_value = mock_response

        # Call the method
        response = self.browser_application.create(name='Account Global')

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'post')
    def test_create_failure(self, mock_post):
        """
        Test browser_applications .create() failure
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_post.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.browser_application.create(name='Account Global')
