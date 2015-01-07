import os
from datetime import time
from unittest import TestCase

from mock import patch, call, Mock
import requests

from newrelic_api.base import Resource
from newrelic_api.exceptions import ConfigurationException, NewRelicAPIServerException


class ResourceTests(TestCase):

    def setUp(self):
        self.TEST_URL = 'https://www.google.com'

    @patch.object(os.environ, 'get', spec_set=True)
    def test_resource_with_arg(self, os_environ_mock):
        """
        Test the api_key gets set by an argument
        """

        resource = Resource(api_key='123')

        self.assertFalse(os_environ_mock.called)

        self.assertEqual(resource.api_key, '123')

    @patch.object(os.environ, 'get', spec_set=True)
    def test_second_resource_from_os(self, os_environ_mock):
        """
        Test the api_key gets set by the OS by NEWRELIC_API_KEY
        """
        os_environ_mock.side_effect = (None, '123')

        resource = Resource()

        os_environ_mock.assert_has_calls(
            [
                call('NEW_RELIC_API_KEY'),
                call('NEWRELIC_API_KEY'),
            ]
        )

        self.assertEqual(resource.api_key, '123')

    @patch.object(os.environ, 'get', spec_set=True)
    def test_resource_from_os(self, os_environ_mock):
        """
        Test the api_key gets set by the OS
        """
        os_environ_mock.return_value = '123'

        resource = Resource()

        os_environ_mock.assert_called_once_with('NEW_RELIC_API_KEY')

        self.assertEqual(resource.api_key, '123')

    @patch.object(os.environ, 'get', spec_set=True)
    def test_resource_raises_error(self, os_environ_mock):
        """
        Test the api_key is not set
        """
        os_environ_mock.return_value = None

        with self.assertRaises(ConfigurationException):
            Resource()

        # os_environ_mock.assert_called_once_with('NEWRELIC_API_KEY')

    @patch.object(requests, 'get')
    def test_get_not_ok(self, mock_get):
        """
        Test ._get() handles a not ok response
        """
        mock_response = Mock(name='response', ok=False, status_code=500, text='Server Error')
        mock_get.return_value = mock_response

        resource = Resource(api_key='123')

        with self.assertRaises(NewRelicAPIServerException):
            resource._get(url=self.TEST_URL)

        mock_get.assert_called_once_with(
            url=self.TEST_URL,
        )

    @patch.object(requests, 'put')
    def test_put_not_ok(self, mock_put):
        """
        Test ._put() handles a not ok response
        """
        mock_response = Mock(name='response', ok=False, status_code=500, text='Server Error')
        mock_put.return_value = mock_response

        resource = Resource(api_key='123')

        with self.assertRaises(NewRelicAPIServerException):
            resource._put(url=self.TEST_URL)

        mock_put.assert_called_once_with(
            url=self.TEST_URL,
        )

    @patch.object(requests, 'delete')
    def test_delete_not_ok(self, mock_delete):
        """
        Test ._delete() handles a not ok response
        """
        mock_response = Mock(name='response', ok=False, status_code=500, text='Server Error')
        mock_delete.return_value = mock_response

        resource = Resource(api_key='123')

        with self.assertRaises(NewRelicAPIServerException):
            resource._delete(url=self.TEST_URL)

        mock_delete.assert_called_once_with(
            url=self.TEST_URL,
        )

    def test_build_param_string(self):
        """
        Tests .build_param_string() returns the correct string
        """
        resource = Resource(api_key='123')

        test_params = [
            False,
            'filter[name]=dev',
            None,
            'page=1',
            0,
            [],
            {},
            time(0)
        ]

        param_str = resource.build_param_string(test_params)

        self.assertEqual(param_str, 'filter[name]=dev&page=1')
