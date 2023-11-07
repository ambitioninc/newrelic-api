from .base import Resource


class AlertViolations(Resource):
    """
    An interface for interacting with the NewRelic Alerts Violations API.
    """
    def list(self, filter_start_date=None, filter_end_date=None, filter_only_open=None, page=None):
        """
        This API endpoint returns a paginated list of the violations
        associated with your New Relic account. Alert violations can be filtered
        by time window and open status.

        :type filter_start_date: datetime.datetime
        :param filter_start_date: Filter to violations created after this time

        :type filter_end_date: datetime.datetime
        :param filter_end_date: Filter to violations created before this time

        :type filter_only_open: boolean
        :param filter_start_date: Filter by open violations

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results

        ::

            {
              "violation": {
                "id": "integer",
                "label": "string",
                "duration": "integer",
                "policy_name": "string",
                "condition_name": "string",
                "priority": "string",
                "opened_at": "integer",
                "closed_at": "integer",
                "entity": {
                  "product": "string",
                  "type": "string",
                  "group_id": "integer",
                  "id": "integer",
                  "name": "string"
                },
                "links": {
                  "policy_id": "integer",
                  "condition_id": "integer",
                  "incident_id": "integer"
                }
              }
            }

        """
        filters = [
            'start_date={0}'.format(filter_start_date.isoformat()) if filter_start_date else None,
            'end_date={0}'.format(filter_end_date.isoformat()) if filter_end_date else None,
            'only_open={0}'.format('true' if filter_only_open else 'false') if filter_only_open is not None else None,
            'page={0}'.format(page) if page else None
        ]

        return self._get(
            url='{0}alerts_violations.json'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(filters)
        )
