from .base import Resource


class MobileApplications(Resource):
    """
    An interface for interacting with the NewRelic mobile application API.
    """
    def list(
            self, filter_name=None, filter_ids=None, filter_language=None,
            page=None):
        """
        This API endpoint returns a paginated list of the Mobile Applications
        associated with your New Relic account.

        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results

        ::

            {
                "applications": [
                    {
                        "id": "integer",
                        "name": "string",
                        "health_status": "string",
                        "reporting": "boolean",
                        "mobile_summary": {
                            "active_users": "integer",
                            "launch_count": "integer",
                            "throughput": "float",
                            "response_time": "float",
                            "calls_per_session": "float",
                            "interaction_time": "float",
                            "failed_call_rate": "float",
                            "remote_error_rate": "float"
                        },
                        "crash_summary": {
                            "supports_crash_data": "boolean",
                            "unresolved_crash_count": "integer",
                            "crash_count": "integer",
                            "crash_rate": "float"
                        }
                    }
                ]
            }

        """

        return self._get(
            url='{0}mobile_applications.json'.format(self.URL),
            headers=self.headers
        )

    def show(self, id):
        """
        This API endpoint returns a single Mobile Application, identified its ID.

        :type id: int
        :param id: Mobile Application ID

        :rtype: dict
        :return: The JSON response of the API.

        ::

                {
                    "application": {
                        "id": "integer",
                        "name": "string",
                        "health_status": "string",
                        "reporting": "boolean",
                        "mobile_summary": {
                        "active_users": "integer",
                        "launch_count": "integer",
                        "throughput": "float",
                        "response_time": "float",
                        "calls_per_session": "float",
                        "interaction_time": "float",
                        "failed_call_rate": "float",
                        "remote_error_rate": "float"
                        },
                        "crash_summary": {
                        "supports_crash_data": "boolean",
                        "unresolved_crash_count": "integer",
                        "crash_count": "integer",
                        "crash_rate": "float"
                        }
                    }
                }

        """
        return self._get(
            url='{0}mobile_applications/{1}.json'.format(self.URL, id),
            headers=self.headers,
        )

    def metric_names(self, id, name=None, page=None, cursor=None):
        """
        Return a list of known metrics and their value names for the given resource.

        :type id: int
        :param id: Mobile Application ID

        :type name: str
        :param name: Filter metrics by name

        :type page: int
        :param page: Pagination index (will be depecrated)

        :type cursor: str
        :param cursor: Cursor for next page (replacing page param)

        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results

        ::

            {
                "metrics": [
                    {
                        "name": "string",
                        "values": [
                            "string"
                        ]
                    }
                ]
            }

        """
        params = [
            'name={0}'.format(name) if name else None,
            'page={0}'.format(page) if page else None,
            'cursor={0}'.format(cursor) if cursor else None
        ]

        return self._get(
            url='{0}mobile_applications/{1}/metrics.json'.format(self.URL, id),
            headers=self.headers,
            params=self.build_param_string(params)
        )

    def metric_data(
            self, id, names, values=None, from_dt=None, to_dt=None,
            summarize=False, period=None):
        """
        This API endpoint returns a list of values for each of the requested
        metrics. The list of available metrics can be returned using the Metric
        Name API endpoint. Metric data can be filtered by a number of
        parameters, including multiple names and values, and by time range.
        Metric names and values will be matched intelligently in the
        background. You can also retrieve a summarized data point across the
        entire time range selected by using the summarize parameter.

        **Note** All times sent and received are formatted in UTC. The default
        time range is the last 30 minutes.

        :type id: int
        :param id: Mobile Application ID

        :type names: list of str
        :param names: Retrieve specific metrics by name

        :type values: list of str
        :param values: Retrieve specific metric values

        :type from_dt: datetime
        :param from_dt: Retrieve metrics after this time

        :type to_dt: datetime
        :param to_dt: Retrieve metrics before this time

        :type summarize: bool
        :param summarize: Summarize the data

        :type period: int
        :param period: Period of timeslices in seconds

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "metric_data": {
                    "from": "time",
                    "to": "time",
                    "metrics_not_found": "string",
                    "metrics_found": "string",
                    "metrics": [
                        {
                            "name": "string",
                            "timeslices": [
                                {
                                    "from": "time",
                                    "to": "time",
                                    "values": "hash"
                                }
                            ]
                        }
                    ]
                }
            }

        """
        params = [
            'from={0}'.format(from_dt) if from_dt else None,
            'to={0}'.format(to_dt) if to_dt else None,
            'summarize=true' if summarize else None
        ]

        params += ['names[]={0}'.format(name) for name in names]
        if values:
            params += ['values[]={0}'.format(value) for value in values]

        if period:
            params += ['period={0}'.format(period)]

        return self._get(
            url='{0}mobile_applications/{1}/metrics/data.json'.format(self.URL, id),
            headers=self.headers,
            params=self.build_param_string(params)
        )
