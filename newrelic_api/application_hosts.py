from .base import Resource


class ApplicationHosts(Resource):
    """
    An interface for interacting with the New Relic Application Hosts API.
    """
    def list(
            self, application_id, filter_hostname=None, filter_ids=None,
            page=None):
        """
        This API endpoint returns a paginated list of hosts associated with the
        given application.

        Application hosts can be filtered by hostname, or the list of
        application host IDs.

        :type application_id: int
        :param application_id: Application ID

        :type filter_hostname: str
        :param filter_hostname: Filter by server hostname

        :type filter_ids: list of ints
        :param filter_ids: Filter by application host ids

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results

        ::

            {
                "application_hosts": [
                    {
                        "id": "integer",
                        "application_name": "string",
                        "host": "string",
                        "language": "integer",
                        "health_status": "string",
                        "application_summary": {
                            "response_time": "float",
                            "throughput": "float",
                            "error_rate": "float",
                            "apdex_score": "float"
                        },
                        "end_user_summary": {
                            "response_time": "float",
                            "throughput": "float",
                            "apdex_score": "float"
                        },
                        "links": {
                            "application": "integer",
                            "application_instances": [
                                "integer"
                            ],
                            "server": "integer"
                        }
                    }
                ],
                "pages": {
                    "last": {
                        "url": "https://api.newrelic.com/v2/applications/{application_id}/hosts.json?page=2",
                        "rel": "last"
                    },
                    "next": {
                        "url": "https://api.newrelic.com/v2/applications/{application_id}/hosts.json?page=2",
                        "rel": "next"
                    }
                }
            }

        """
        filters = [
            'filter[hostname]={0}'.format(filter_hostname) if filter_hostname else None,
            'filter[ids]={0}'.format(','.join([str(app_id) for app_id in filter_ids])) if filter_ids else None,
            'page={0}'.format(page) if page else None
        ]
        return self._get(
            url='{root}applications/{application_id}/hosts.json'.format(
                root=self.URL,
                application_id=application_id
            ),
            headers=self.headers,
            params=self.build_param_string(filters)
        )

    def show(self, application_id, host_id):
        """
        This API endpoint returns a single application host, identified by its
        ID.

        :type application_id: int
        :param application_id: Application ID

        :type host_id: int
        :param host_id: Application host ID

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "application_host": {
                    "id": "integer",
                    "application_name": "string",
                    "host": "string",
                    "language": "integer",
                    "health_status": "string",
                    "application_summary": {
                        "response_time": "float",
                        "throughput": "float",
                        "error_rate": "float",
                        "apdex_score": "float"
                    },
                    "end_user_summary": {
                        "response_time": "float",
                        "throughput": "float",
                        "apdex_score": "float"
                    },
                    "links": {
                        "application": "integer",
                        "application_instances": [
                            "integer"
                        ],
                        "server": "integer"
                    }
                }
            }

        """
        return self._get(
            url='{root}applications/{application_id}/hosts/{host_id}.json'.format(
                root=self.URL,
                application_id=application_id,
                host_id=host_id
            ),
            headers=self.headers,
        )

    def metric_names(self, application_id, host_id, name=None, page=None):
        """
        Return a list of known metrics and their value names for the given resource.

        :type application_id: int
        :param application_id: Application ID

        :type host_id: int
        :param host_id: Application Host ID

        :type name: str
        :param name: Filter metrics by name

        :type page: int
        :param page: Pagination index

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
                ],
                "pages": {
                    "last": {
                        "url": "https://api.newrelic.com/v2/\
applications/{application_id}/hosts/{host_id}/metrics.json?page=2",
                        "rel": "last"
                    },
                    "next": {
                        "url": "https://api.newrelic.com/v2/\
applications/{application_id}/hosts/{host_id}/metrics.json?page=2",
                        "rel": "next"
                    }
                }
            }

        """
        params = [
            'name={0}'.format(name) if name else None,
            'page={0}'.format(page) if page else None
        ]
        return self._get(
            url='{root}applications/{application_id}/hosts/{host_id}/metrics.json'.format(
                root=self.URL,
                application_id=application_id,
                host_id=host_id
            ),
            headers=self.headers,
            params=self.build_param_string(params)
        )

    def metric_data(
            self, application_id, host_id, names, values=None, from_dt=None, to_dt=None,
            summarize=False):
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

        :type application_id: int
        :param application_id: Application ID

        :type host_id: int
        :param host_id: Application Host ID

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

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "metric_data": {
                    "from": "time",
                    "to": "time",
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

        return self._get(
            url='{url}applications/{application_id}/hosts/{host_id}/metrics/data.json'.format(
                url=self.URL,
                application_id=application_id,
                host_id=host_id,
            ),
            headers=self.headers,
            params=self.build_param_string(params)
        )
