from unittest import TestCase

from mock import patch, Mock
import requests

from newrelic_api.key_transactions import KeyTransactions


class NRKeyTransactionsTests(TestCase):
    def setUp(self):
        super(NRKeyTransactionsTests, self).setUp()
        self.key_transactions = KeyTransactions(api_key='dummy_key')

        self.key_transactions_list_response = {
            "key_transactions": [
                {
                    "id": 333112,
                    "name": "login",
                    "transaction_name": "Login Page",
                    "application_summary": {
                        "response_time": 170,
                        "throughput": 3,
                        "error_rate": 0,
                        "apdex_target": 0,
                        "apdex_score": 1
                    },
                    "end_user_summary": {
                        "response_time": 300.0,
                        "throughput": 4,
                        "apdex_target": 0,
                        "apdex_score": 1
                    },
                    "links": {
                        "application": 123456
                    }
                }
            ]
        }
        self.key_transactions_show_response = {
            'key_transaction': self.key_transactions_list_response['key_transactions'][0]
        }

    @patch.object(requests, 'get')
    def test_list_success(self, mock_get):
        """
        Test key transactions .list()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.key_transactions_list_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.key_transactions.list()

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_list_success_with_filter_ids(self, mock_get):
        """
        Test key transactions .list() with filter_ids
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.key_transactions_list_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.key_transactions.list(filter_ids=[333112])

        self.assertIsInstance(response, dict)

        mock_get.assert_called_once_with(
            url='https://api.newrelic.com/v2/key_transactions.json',
            headers=self.key_transactions.headers,
            params='filter[ids]=333112'
        )

    @patch.object(requests, 'get')
    def test_list_failure(self, mock_get):
        """
        Test key transactions .list() failure case
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.key_transactions.list()

    @patch.object(requests, 'get')
    def test_show_success(self, mock_get):
        """
        Test key transactions .show() success
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.key_transactions_show_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.key_transactions.show(id=333112)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_show_failure(self, mock_get):
        """
        Test key transactions .show() failure
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.key_transactions.show(id=333114)
