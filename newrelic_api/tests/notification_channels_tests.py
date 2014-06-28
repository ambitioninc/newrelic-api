from unittest import TestCase

from mock import patch
import requests

from newrelic_api.notification_channels import NotificationChannels


class NRNotificationChannelsTests(TestCase):
    def setUp(self):
        super(NRNotificationChannelsTests, self).setUp()
        self.channels = NotificationChannels(api_key='dummy_key')

        self.list_response = {
            "notification_channels": [
                {
                    "id": 111222,
                    "type": "user",
                    "downtime_only": False,
                    "mobile_alerts": False,
                    "email_alerts": True,
                    "links": {
                        "user": 222333
                    }
                }
            ]
        }

        self.show_response = {
            'notification_channel': self.list_response['notification_channels'][0]
        }

    @patch.object(requests, 'get')
    def test_list(self, mock_get):
        """
        Test notification channels .list()
        """
        self.channels.list(filter_type=['user'], page=0)

        mock_get.assert_called_once_with(
            url='https://api.newrelic.com/v2/notification_channels.json',
            headers=self.channels.headers,
            params='filter[type]=user'
        )

    @patch.object(requests, 'get')
    def test_show(self, mock_get):
        """
        Test notification channels .show()
        """
        self.channels.show(id=11122)
        mock_get.assert_called_once_with(
            url='https://api.newrelic.com/v2/notification_channels/11122.json',
            headers=self.channels.headers,
        )
