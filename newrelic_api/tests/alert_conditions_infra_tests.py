from unittest import TestCase

from mock import patch, Mock
import requests

from newrelic_api.alert_conditions_infra import AlertConditionsInfra


class NRAlertConditionsInfraInfraTests(TestCase):
    def setUp(self):
        super(NRAlertConditionsInfraInfraTests, self).setUp()
        self.alert_conditions_infra = AlertConditionsInfra(api_key='dummy_key')

        self.list_success_response = {
            "meta": {
                "total": 1,
                "limit": 50,
                "offset": 0
            },
            "data": [
                {
                    "comparison": "above",
                    "select_value": "cpuPercent",
                    "created_at_epoch_millis": 1532946280004,
                    "name": "CPU usage alert",
                    "enabled": "true",
                    "updated_at_epoch_millis": 1532947363110,
                    "event_type": "SystemSample",
                    "critical_threshold": {
                        "duration_minutes": 1,
                        "value": 50,
                        "time_function": "all"
                    },
                    "type": "infra_metric",
                    "id": 100,
                    "policy_id": 1
                }
            ],
            "links": {}
        }

        self.single_success_response = {
            "data": {
                "comparison": "above",
                "select_value": "cpuPercent",
                "created_at_epoch_millis": 1532946280004,
                "name": "CPU usage alert",
                "enabled": "true",
                "updated_at_epoch_millis": 1532947363110,
                "event_type": "SystemSample",
                "critical_threshold": {
                    "duration_minutes": 1,
                    "value": 50,
                    "time_function": "all"
                },
                "type": "infra_metric",
                "id": 100,
                "policy_id": 1
            }
        }

    @patch.object(requests, 'get')
    def test_list_success(self, mock_get):
        """
        Test alert conditions .list()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.list_success_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.alert_conditions_infra.list(policy_id=1)

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'get')
    def test_list_failure(self, mock_get):
        """
        Test alert conditions .list() failure case
        """
        mock_response = Mock(name='response')
        mock_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_get.return_value = mock_response

        with self.assertRaises(ValueError):
            # Call the method
            self.alert_conditions_infra.list(policy_id=1)

    @patch.object(requests, 'get')
    def test_show_success(self, mock_get):
        """
        Test alert conditions .show()
        """
        mock_response = Mock(name='response')
        mock_response.json.return_value = self.single_success_response
        mock_get.return_value = mock_response

        # Call the method
        response = self.alert_conditions_infra.show(
            alert_condition_infra_id=100
        )

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'post')
    def test_create_success(self, mock_post):
        """
        Test alerts_conditions .update() success
        """
        mock_update_response = Mock(name='response')
        mock_update_response.json.return_value = self.single_success_response
        mock_post.return_value = mock_update_response

        # Call the method
        response = self.alert_conditions_infra.create(
            policy_id=1, name='New Name', condition_type='infra_metric',
            alert_condition_configuration=self.single_success_response['data']
        )

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'put')
    def test_update_success(self, mock_put):
        """
        Test alerts_conditions .update() success
        """
        mock_update_response = Mock(name='response')
        mock_update_response.json.return_value = self.single_success_response
        mock_put.return_value = mock_update_response

        # Call the method
        response = self.alert_conditions_infra.update(
            alert_condition_infra_id=100, policy_id=1, name='New Name',
            condition_type='infra_metric',
            alert_condition_configuration=self.single_success_response['data']
        )

        self.assertIsInstance(response, dict)

    @patch.object(requests, 'put')
    def test_update_failure(self, mock_put):
        """
        Test alerts_conditions .update() failure
        """
        mock_update_response = Mock(name='response')
        mock_update_response.json.side_effect = ValueError('No JSON object could be decoded')
        mock_put.return_value = mock_update_response

        # Call the method
        with self.assertRaises(ValueError):
            self.alert_conditions_infra.update(
                alert_condition_infra_id=100, policy_id=1, name='New Name',
                condition_type='infra_metric',
                alert_condition_configuration=self.single_success_response['data']
            )

    @patch.object(requests, 'delete')
    def test_delete_success(self, mock_delete):
        """
        Test alert policies .delete() success
        """

        self.alert_conditions_infra.delete(alert_condition_infra_id=100)

        mock_delete.assert_called_once_with(
            url='https://infra-api.newrelic.com/v2/alerts/conditions/100',
            headers=self.alert_conditions_infra.headers
        )
