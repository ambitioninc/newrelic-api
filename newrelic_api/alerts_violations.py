from .base import Resource


class AlertsViolations(Resource):
    """
    An interface for interacting with the NewRelic Alerts Violations API.
    """
    def list(
            self, only_open=None, page=None):
        """
        This API endpoint works with new Alerts on alerts.newrelic.com.
        It returns a list of the violations associated with your New Relic account.
        """
        filters = [
            'only_open={0}'.format(only_open) if only_open in [True, False] else None,
            'page={0}'.format(page) if page else None
        ]
        return self._get(
            url='{0}alerts_violations.json'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(filters)
        )
