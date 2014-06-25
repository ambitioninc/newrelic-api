import os
from unittest import TestCase

from mock import patch

from newrelic_api.base import Resource
from newrelic_api.exceptions import ConfigurationException


class ResourceTests(TestCase):

    @patch.object(os.environ, 'get', spec_set=True)
    def test_resource_with_arg(self, os_environ_mock):
        """
        Test the api_key gets set by an argument
        """

        resource = Resource(api_key='123')

        self.assertFalse(os_environ_mock.called)

        self.assertEqual(resource.api_key, '123')

    @patch.object(os.environ, 'get', spec_set=True)
    def test_resource_from_os(self, os_environ_mock):
        """
        Test the api_key gets set by the OS
        """
        os_environ_mock.return_value = '123'

        resource = Resource()

        os_environ_mock.assert_called_once_with('NEWRELIC_API_KEY')

        self.assertEqual(resource.api_key, '123')

    @patch.object(os.environ, 'get', spec_set=True)
    def test_resource_raises_error(self, os_environ_mock):
        """
        Test the api_key is not set
        """
        os_environ_mock.return_value = None

        with self.assertRaises(ConfigurationException):
            Resource()

        os_environ_mock.assert_called_once_with('NEWRELIC_API_KEY')
