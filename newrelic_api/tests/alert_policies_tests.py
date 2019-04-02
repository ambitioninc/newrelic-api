from unittest import TestCase

from mock import patch, Mock
import json
import requests

from newrelic_api.alert_policies import AlertPolicies


class NRAlertPoliciesTests(TestCase):
    def setUp(self):
        super(NRAlertPoliciesTests, self).setUp()
        self.policies = AlertPolicies(api_key='dummy_key')

        self.policies_list_response = {
            "policies": [
                {
                    "id": 12345,
                    "incident_preference": "PER_CONDITION_AND_TARGET",
                    "name": "Default Server Policy",
                    "created_at": 123456789012,
                }
            ]
        }
        self.policy_single_response = {
            "policy": self.policies_list_response['policies'][0]
        }
        self.channel_single_response = {
            "channel": {
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
        }

    @patch.object(requests, 'get')
    def test_list_success(self, mock_get):
        """
        Test alert policies .list()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.policies_list_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.policies.list()

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_list_success_with_name(self, mock_get):
        """
        Test alert policies .list() with filter_ids
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.policies_list_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.policies.list(filter_name='Default Server Policy')

        self.assertIsInstance(response, dict)
        mock_get.assert_called_once_with(
            url='https://api.newrelic.com/v2/alerts_policies.json',
            headers=self.policies.headers,
            params='filter[name]=Default Server Policy'
        )

    @patch.object(requests, 'get')
    def test_list_failure(self, mock_get):
        """
        Test alert policies .list() failure case
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.policies.list()

    @patch.object(requests, 'post')
    def test_create_success(self, mock_post):
        """
        Test alert policies .create() calls put with correct parameters
        """
        self.policies.create(
            name=self.policy_single_response['policy']['name'],
            incident_preference=self.policy_single_response['policy']['incident_preference']
        )

        mock_post.assert_called_once_with(
            url='https://api.newrelic.com/v2/alerts_policies.json',
            headers=self.policies.headers,
            data=json.dumps({
                "policy": {
                    "name": self.policy_single_response['policy']['name'],
                    "incident_preference": self.policy_single_response['policy']['incident_preference']
                }
            })
        )

    @patch.object(requests, 'put')
    def test_update_success(self, mock_put):
        """
        Test alert policies .update() calls put with correct parameters
        """
        self.policies.update(
            id=self.policy_single_response['policy']['id'],
            name=self.policy_single_response['policy']['name'],
            incident_preference=self.policy_single_response['policy']['incident_preference']
        )

        mock_put.assert_called_once_with(
            url='https://api.newrelic.com/v2/alerts_policies/{0}.json'.format(
                self.policy_single_response['policy']['id']
            ),
            headers=self.policies.headers,
            data=json.dumps({
                "policy": {
                    "name": self.policy_single_response['policy']['name'],
                    "incident_preference": self.policy_single_response['policy']['incident_preference']
                }
            })
        )

    @patch.object(requests, 'delete')
    def test_delete_success(self, mock_delete):
        """
        Test alert policies .delete() success
        """

        self.policies.delete(id=self.policy_single_response['policy']['id'])

        mock_delete.assert_called_once_with(
            url='https://api.newrelic.com/v2/alerts_policies/{0}.json'.format(
                self.policy_single_response['policy']['id']
            ),
            headers=self.policies.headers
        )

    @patch.object(requests, 'put')
    def test_associate_with_notification_channel_success(self, mock_put):
        """
        Test alert policies .associate_with_notification_channel() calls put with correct parameters
        """
        self.policies.associate_with_notification_channel(
            id=self.policy_single_response['policy']['id'],
            channel_id=self.channel_single_response['channel']['id'],
        )

        mock_put.assert_called_once_with(
            url='https://api.newrelic.com/v2/alerts_policy_channels.json?policy_id={0}&channel_ids={1}'.format(
                self.policy_single_response['policy']['id'],
                self.channel_single_response['channel']['id']
            ),
            headers=self.policies.headers
        )

    @patch.object(requests, 'put')
    def test_dissociate_from_notification_channel(self, mock_put):
        """
        Test alert policies .associate_with_notification_channel() calls put with correct parameters
        """
        self.policies.associate_with_notification_channel(
            id=self.policy_single_response['policy']['id'],
            channel_id=self.channel_single_response['channel']['id'],
        )

        mock_put.assert_called_once_with(
            url='https://api.newrelic.com/v2/alerts_policy_channels.json?policy_id={0}&channel_ids={1}'.format(
                self.policy_single_response['policy']['id'],
                self.channel_single_response['channel']['id']
            ),
            headers=self.policies.headers
        )
