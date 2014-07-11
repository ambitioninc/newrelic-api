from unittest import TestCase

from mock import patch, Mock
import requests

from newrelic_api.plugins import Plugins


class NRPluginsTests(TestCase):
    def setUp(self):
        super(NRPluginsTests, self).setUp()
        self.plugins = Plugins(api_key='dummy_key')

        self.plugins_list_response = {
            'plugins': [
                {
                    "id": 2227,
                    "name": "SendGrid",
                    "guid": "com.SendGrid",
                    "publisher": "SendGrid",
                    "details": {
                        "description": "Email Delivery. Simplified.\r\n\r\n"
                                       "SendGrid is a simple email infrastructure in the cloud.Our platform allows "
                                       "developers to easily integrate email functionality into their web and mobile "
                                       "applications. Through APIs or SMTP relay, you can send and receive emails "
                                       "while retrieving detailed email statistics. Our users enjoy increased "
                                       "deliverability of email, on demand scalability and more time to focus on their "
                                       "product instead of taking care of email servers.  \r\n\r\n"
                                       "New Relic's SendGrid plugin provides statistical monitoring and a simple 'at a "
                                       "glance' health check of ones email traffic. The plugin includes real time "
                                       "information on email performance including deliverability, engagement, and "
                                       "compliance factors.  \r\n\r\n"
                                       "### Requirements\r\n\r\n"
                                       "* a SendGrid account\r\n"
                                       "* a New Relic account",
                        "is_public": None,
                        "created_at": "2013-09-19T10:55:06-07:00",
                        "updated_at": "2014-01-27T14:15:35-08:00",
                        "last_published_at": None,
                        "has_unpublished_changes": True,
                        "branding_image_url": "http://static.sendgrid.com.s3.amazonaws.com/images/64X64.png",
                        "upgraded_at": "2013-06-19T10:55:06-07:00",
                        "short_name": "SendGrid",
                        "publisher_about_url": "http://sendgrid.com/",
                        "publisher_support_url": "http://support.sendgrid.com/home",
                        "download_url": "http://sendgrid.com/app/appSettings/type/newrelic/id/22",
                        "first_edited_at": None,
                        "last_edited_at": None,
                        "first_published_at": None,
                        "published_version": None
                    },
                    "summary_metrics": []
                }
            ]
        }
        self.plugins_show_response = {
            'plugin': self.plugins_list_response['plugins'][0]
        }

    @patch.object(requests, 'get')
    def test_list_success(self, mock_get):
        """
        Test plugins .list()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.plugins_list_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.plugins.list()

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_list_success_with_filter_ids(self, mock_get):
        """
        Test plugins .list() with filter_ids
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.plugins_list_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.plugins.list(filter_ids=[2227])

        self.assertIsInstance(response, dict)

        mock_get.assert_called_once_with(
            url='https://api.newrelic.com/v2/plugins.json',
            headers=self.plugins.headers,
            params='filter[ids]=2227'
        )

    @patch.object(requests, 'get')
    def test_list_failure(self, mock_get):
        """
        Test plugins .list() failure case
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.plugins.list()

    @patch.object(requests, 'get')
    def test_show_success(self, mock_get):
        """
        Test plugins .show() success
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.plugins_show_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.plugins.show(id=2227)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_show_failure(self, mock_get):
        """
        Test plugins .show() failure
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.plugins.show(id=2227)
