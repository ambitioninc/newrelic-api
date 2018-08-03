from unittest import TestCase

from mock import patch, Mock
import json
import requests

from newrelic_api.notification_channels import NotificationChannels


class NRNotificationChannelsTests(TestCase):
    def setUp(self):
        super(NRNotificationChannelsTests, self).setUp()
        self.channels = NotificationChannels(api_key='dummy_key')

        self.list_response = {
            "channels": [
                {
                    "id": 111222,
                    "type": "user",
                    "name": "Some User",
                    "links": {
                        "policy_ids": []
                    },
                    "configuration": {
                        "user": 222333
                    }
                }
            ]
        }

        self.single_response = {
            'channels': self.list_response['channels'][0]
        }

    @patch.object(requests, 'get')
    def test_list_success(self, mock_get):
        """
        Test notification channels .list()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.list_response
        mock_get.return_value = mock_response

        response = self.channels.list()

        self.assertIsInstance(response, dict)
        mock_get.assert_called_once_with(
            url='https://api.newrelic.com/v2/alerts_channels.json',
            headers=self.channels.headers,
            params=''
        )

    @patch.object(requests, 'get')
    def test_list_success_with_pagination(self, mock_get):
        """
        Test notification channels .list() with page parameter
        """
        self.channels.list(page=2)

        mock_get.assert_called_once_with(
            url='https://api.newrelic.com/v2/alerts_channels.json',
            headers=self.channels.headers,
            params='page=2'
        )

    @patch.object(requests, 'post')
    def test_create_success(self, mock_post):
        """
        Test notification channels .create() calls put with correct parameters
        """
        self.channels.create(
            name=self.single_response['channels']['name'],
            type=self.single_response['channels']['type'],
            configuration=self.single_response['channels']['configuration']
        )

        mock_post.assert_called_once_with(
            url='https://api.newrelic.com/v2/alerts_channels.json',
            headers=self.channels.headers,
            data=json.dumps({
                "channel": {
                    "name": self.single_response['channels']['name'],
                    "type": self.single_response['channels']['type'],
                    "configuration": self.single_response['channels']['configuration']
                }
            })
        )
