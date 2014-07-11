from unittest import TestCase

from mock import patch, Mock
import requests

from newrelic_api.users import Users


class NRUsersTests(TestCase):
    def setUp(self):
        super(NRUsersTests, self).setUp()
        self.user = Users(api_key='dummy_key')

        self.user_list_response = {
            'users': [
                {
                    "id": 333113,
                    "first_name": "Josh",
                    "last_name": "Marlow",
                    "email": "josh.marlow@ambition.com",
                    "role": "user"
                },
                {
                    "id": 333112,
                    "first_name": "Micah",
                    "last_name": "Hausler",
                    "email": "micah.hausler@ambition.com",
                    "role": "admin"
                },
                {
                    "id": 333111,
                    "first_name": "Travis",
                    "last_name": "Truett",
                    "email": "travis.truett@ambition.com",
                    "role": "owner"
                }
            ]
        }
        self.user_show_response = self.user_list_response['users'][1]

    @patch.object(requests, 'get')
    def test_list_success(self, mock_get):
        """
        Test users .list()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.user_list_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.user.list()

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_list_success_with_ids(self, mock_get):
        """
        Test users .list() with filter_ids
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.user_list_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.user.list(filter_ids=[333113, 333112, 333111])

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_list_failure(self, mock_get):
        """
        Test users .list() failure case
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.user.list()

    @patch.object(requests, 'get')
    def test_show_success(self, mock_get):
        """
        Test users .show() success
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.user_show_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.user.show(id=333112)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_show_failure(self, mock_get):
        """
        Test users .show() failure
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.user.show(id=333114)
