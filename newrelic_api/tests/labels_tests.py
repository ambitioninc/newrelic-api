from unittest import TestCase

from mock import patch, Mock
import requests

from newrelic_api.labels import Labels


class NRLabelsTests(TestCase):
    def setUp(self):
        super(NRLabelsTests, self).setUp()
        self.label = Labels(api_key='dummy_key')

        label = {
            "key": "Ambition:Production",
            "category": "Ambition",
            "name": "Production",
            "links": {
                "applications": [],
                "servers": [
                    1234567
                ]
            }
        }
        self.list_success_response = {
            'labels': [
                label,
            ],
        }
        self.create_success_response = {
            'label': label,
        }

    @patch.object(requests, 'get')
    def test_list_success(self, mock_get):
        """
        Test labels .list()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.list_success_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.label.list()

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_list_failure(self, mock_get):
        """
        Test labels .list() failure case
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.label.list()

    @patch.object(requests, 'put')
    def test_create_success(self, mock_put):
        """
        Test labels .create() success
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.create_success_response
        mock_put.return_value = mock_response

        # Call the method
        response = self.label.create(name='Production', category='Ambition')

        self.assertIsInstance(response, dict)
        self.assertEqual(response['label']['key'], 'Ambition:Production')

    @patch.object(requests, 'put')
    def test_create_failure(self, mock_put):
        """
        Test labels .create() failure
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_put.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.label.create(name='Production', category='Ambition')

    @patch.object(requests, 'delete')
    def test_delete_success(self, mock_delete):
        """
        Test labels .delete() success
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.create_success_response
        mock_delete.return_value = mock_response

        # Call the method
        response = self.label.delete(key='Ambition:Production')

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'delete')
    def test_delete_failure(self, mock_delete):
        """
        Test labels .delete() failure
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_delete.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.label.delete(key='Ambition:Production')
