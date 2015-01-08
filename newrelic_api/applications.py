from .base import Resource


class Applications(Resource):
    """
    An interface for interacting with the NewRelic application API.
    """
    def list(
            self, filter_name=None, filter_ids=None, filter_language=None,
            page=None):
        """
        This API endpoint returns a paginated list of the Applications
        associated with your New Relic account. Applications can be filtered
        by their name, the list of application IDs or the application language
        as reported by the agents.

        :type filter_name: str
        :param filter_name: Filter by application name

        :type filter_ids: list of ints
        :param filter_ids: Filter by application ids

        :type filter_language: str
        :param filter_language: Filter by application language

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results

        ::

            {
                "applications": [
                    {
                        "id": "integer",
                        "name": "string",
                        "language": "string",
                        "health_status": "string",
                        "reporting": "boolean",
                        "last_reported_at": "time",
                        "application_summary": {
                            "response_time": "float",
                            "throughput": "float",
                            "error_rate": "float",
                            "apdex_target": "float",
                            "apdex_score": "float"
                        },
                        "end_user_summary": {
                            "response_time": "float",
                            "throughput": "float",
                            "apdex_target": "float",
                            "apdex_score": "float"
                        },
                        "settings": {
                            "app_apdex_threshold": "float",
                            "end_user_apdex_threshold": "float",
                            "enable_real_user_monitoring": "boolean",
                            "use_server_side_config": "boolean"
                        },
                        "links": {
                            "servers": [
                                "integer"
                            ],
                            "application_hosts": [
                                "integer"
                            ],
                            "application_instances": [
                                "integer"
                            ]
                        }
                    }
                ],
                "pages": {
                    "last": {
                        "url": "https://api.newrelic.com/v2/applications.json?page=2",
                        "rel": "last"
                    },
                    "next": {
                        "url": "https://api.newrelic.com/v2/applications.json?page=2",
                        "rel": "next"
                    }
                }
            }

        """
        filters = [
            'filter[name]={0}'.format(filter_name) if filter_name else None,
            'filter[language]={0}'.format(','.join(filter_language)) if filter_language else None,
            'filter[ids]={0}'.format(','.join([str(app_id) for app_id in filter_ids])) if filter_ids else None,
            'page={0}'.format(page) if page else None
        ]
        return self._get(
            url='{0}applications.json'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(filters)
        )

    def show(self, id):
        """
        This API endpoint returns a single Application, identified its ID.

        :type id: int
        :param id: Application ID

        :rtype: dict
        :return: The JSON response of the API.

        ::

                {
                    "application": {
                        "id": "integer",
                        "name": "string",
                        "language": "string",
                        "health_status": "string",
                        "reporting": "boolean",
                        "last_reported_at": "time",
                        "application_summary": {
                            "response_time": "float",
                            "throughput": "float",
                            "error_rate": "float",
                            "apdex_target": "float",
                            "apdex_score": "float"
                        },
                        "end_user_summary": {
                            "response_time": "float",
                            "throughput": "float",
                            "apdex_target": "float",
                            "apdex_score": "float"
                        },
                        "settings": {
                            "app_apdex_threshold": "float",
                            "end_user_apdex_threshold": "float",
                            "enable_real_user_monitoring": "boolean",
                            "use_server_side_config": "boolean"
                        },
                        "links": {
                            "servers": [
                                "integer"
                            ],
                            "application_hosts": [
                                "integer"
                            ],
                            "application_instances": [
                                "integer"
                            ]
                        }
                    }
                }

        """
        return self._get(
            url='{0}applications/{1}.json'.format(self.URL, id),
            headers=self.headers,
        )

    def update(
            self, id, name=None, app_apdex_threshold=None, end_user_apdex_threshold=None,
            enable_real_user_monitoring=None):
        """
        Updates any of the optional parameters of the application

        :type id: int
        :param id: Application ID

        :type name: str
        :param name: The name of the application

        :type app_apdex_threshold: float
        :param app_apdex_threshold: Application apdex threshold to update

        :type end_user_apdex_threshold: float
        :param end_user_apdex_threshold: End user apdex threshold to update

        :type enable_real_user_monitoring: bool
        :param enable_real_user_monitoring: Whether to enable real user
            monitoring

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "application": {
                    "id": "integer",
                    "name": "string",
                    "language": "string",
                    "health_status": "string",
                    "reporting": "boolean",
                    "last_reported_at": "time",
                    "application_summary": {
                        "response_time": "float",
                        "throughput": "float",
                        "error_rate": "float",
                        "apdex_target": "float",
                        "apdex_score": "float"
                    },
                    "end_user_summary": {
                        "response_time": "float",
                        "throughput": "float",
                        "apdex_target": "float",
                        "apdex_score": "float"
                    },
                    "settings": {
                        "app_apdex_threshold": "float",
                        "end_user_apdex_threshold": "float",
                        "enable_real_user_monitoring": "boolean",
                        "use_server_side_config": "boolean"
                    },
                    "links": {
                        "servers": [
                            "integer"
                        ],
                        "application_hosts": [
                            "integer"
                        ],
                        "application_instances": [
                            "integer"
                        ]
                    }
                }
            }

        """
        nr_data = self.show(id)['application']

        data = {
            'application': {
                'name': name or nr_data['name'],
                'settings': {
                    'app_apdex_threshold':
                        app_apdex_threshold or nr_data['settings']['app_apdex_threshold'],
                    'end_user_apdex_threshold':
                        end_user_apdex_threshold or nr_data['settings']['end_user_apdex_threshold'],
                    'enable_real_user_monitoring':
                        enable_real_user_monitoring or nr_data['settings']['enable_real_user_monitoring']
                }
            }
        }

        return self._put(
            url='{0}{1}/{2}.json'.format(
                self.URL,
                'applications',
                id),
            headers=self.headers,
            data=data
        )

    def delete(self, id):
        """
        This API endpoint deletes an application and all of its reported data.

        WARNING: Only applications that have stopped reporting can be deleted.
            This is an irreversible process which will delete all reported
            data for this application.

        :type id: int
        :param id: Application ID

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "application": {
                    "id": "integer",
                    "name": "string",
                    "language": "string",
                    "health_status": "string",
                    "reporting": "boolean",
                    "last_reported_at": "time",
                    "application_summary": {
                        "response_time": "float",
                        "throughput": "float",
                        "error_rate": "float",
                        "apdex_target": "float",
                        "apdex_score": "float"
                    },
                    "end_user_summary": {
                        "response_time": "float",
                        "throughput": "float",
                        "apdex_target": "float",
                        "apdex_score": "float"
                    },
                    "settings": {
                        "app_apdex_threshold": "float",
                        "end_user_apdex_threshold": "float",
                        "enable_real_user_monitoring": "boolean",
                        "use_server_side_config": "boolean"
                    },
                    "links": {
                        "servers": [
                            "integer"
                        ],
                        "application_hosts": [
                            "integer"
                        ],
                        "application_instances": [
                            "integer"
                        ]
                    }
                }
            }

        """
        return self._delete(
            url='{0}applications/{1}.json'.format(self.URL, id),
            headers=self.headers,
        )

    def metric_names(self, id, name=None, page=None):
        """
        Return a list of known metrics and their value names for the given resource.

        :type id: int
        :param id: Application ID

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
                        "url": "https://api.newrelic.com/v2/applications/{application_id}/metrics.json?page=2",
                        "rel": "last"
                    },
                    "next": {
                        "url": "https://api.newrelic.com/v2/applications/{application_id}/metrics.json?page=2",
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
            url='{0}applications/{1}/metrics.json'.format(self.URL, id),
            headers=self.headers,
            params=self.build_param_string(params)
        )

    def metric_data(
            self, id, names, values=None, from_dt=None, to_dt=None,
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

        :type id: int
        :param id: Application ID

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
            url='{0}applications/{1}/metrics/data.json'.format(self.URL, id),
            headers=self.headers,
            params=self.build_param_string(params)
        )
