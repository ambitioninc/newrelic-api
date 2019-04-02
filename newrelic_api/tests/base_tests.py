import os
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
    def test_get_ok_with_links(self, mock_get):
        """
        Test ._get() handles an ok response with links
        """
        mock_response = Mock(
            name='response',
            ok=True,
            status_code=200,
            links={
                "last": {
                    "url": "https://api.newrelic.com/v2/servers.json?page=2",
                    "rel": "last"
                },
                "next": {
                    "url": "https://api.newrelic.com/v2/servers.json?page=2",
                    "rel": "next"
                }
            }
        )
        mock_response.json.return_value = {
            "servers": [
                {
                    "id": "integer",
                    "account_id": "integer",
                    "name": "string",
                    "host": "string",
                    "reporting": "boolean",
                    "last_reported_at": "time",
                    "summary": {
                        "cpu": "float",
                        "cpu_stolen": "float",
                        "disk_io": "float",
                        "memory": "float",
                        "memory_used": "integer",
                        "memory_total": "integer",
                        "fullest_disk": "float",
                        "fullest_disk_free": "integer"
                    }
                }
            ]
        }

        mock_get.return_value = mock_response

        resource = Resource(api_key='123')

        response = resource._get(url=self.TEST_URL)

        self.assertIn(
            'pages',
            list(response.keys())
        )

    @patch.object(requests, 'get')
    def test_get_ok_without_links(self, mock_get):
        """
        Test ._get() handles an ok response with links
        """
        mock_response = Mock(
            name='response',
            ok=True,
            status_code=200,
            links=None
        )
        mock_response.json.return_value = {
            "servers": [
                {
                    "id": "integer",
                    "account_id": "integer",
                    "name": "string",
                    "host": "string",
                    "reporting": "boolean",
                    "last_reported_at": "time",
                    "summary": {
                        "cpu": "float",
                        "cpu_stolen": "float",
                        "disk_io": "float",
                        "memory": "float",
                        "memory_used": "integer",
                        "memory_total": "integer",
                        "fullest_disk": "float",
                        "fullest_disk_free": "integer"
                    }
                }
            ]
        }

        mock_get.return_value = mock_response

        resource = Resource(api_key='123')

        response = resource._get(url=self.TEST_URL)

        self.assertNotIn(
            'pages',
            list(response.keys())
        )

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

    @patch.object(requests, 'post')
    def test_post_not_ok(self, mock_post):
        """
        Test ._post() handles a not ok response
        """
        mock_response = Mock(name='response', ok=False, status_code=500, text='Server Error')
        mock_post.return_value = mock_response

        resource = Resource(api_key='123')

        with self.assertRaises(NewRelicAPIServerException):
            resource._post(url=self.TEST_URL)

        mock_post.assert_called_once_with(
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
        ]

        param_str = resource.build_param_string(test_params)

        self.assertEqual(param_str, 'filter[name]=dev&page=1')
