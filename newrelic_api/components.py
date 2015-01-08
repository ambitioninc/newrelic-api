from .base import Resource


class Components(Resource):
    """
    An interface for interacting with the NewRelic component API.
    """
    def list(
            self, filter_name=None, filter_ids=None, filter_plugin_id=None,
            page=None):
        """
        This API endpoint returns a paginated list of the Components
        associated with your New Relic account. Components can be filtered
        by their name or by a list of component IDs.

        :type filter_name: str
        :param filter_name: Filter by component name

        :type filter_ids: list of ints
        :param filter_ids: Filter by component ids

        :type filter_plugin_id: int
        :param filter_plugin_id: Filter components by the plugin

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results

        ::

            {
                "components": [
                    {
                        "id": "integer",
                        "name": "string",
                        "summary_metrics": [
                            {
                                "id": "integer",
                                "name": "string",
                                "metric": "string",
                                "value_function": "string",
                                "thresholds": {
                                    "caution": "float",
                                    "critical": "float"
                                },
                                "values": {
                                    "raw": "float",
                                    "formatted": "string"
                                }
                            }
                        ]
                    }
                ],
                "pages": {
                    "last": {
                        "url": "https://api.newrelic.com/v2/components.json?page=2",
                        "rel": "last"
                    },
                    "next": {
                        "url": "https://api.newrelic.com/v2/components.json?page=2",
                        "rel": "next"
                    }
                }
            }

        """
        filters = [
            'filter[name]={0}'.format(filter_name) if filter_name else None,
            'filter[ids]={0}'.format(
                ','.join([str(app_id) for app_id in filter_ids])
            ) if filter_ids else None,
            'filter[plugin_id]={0}'.format(filter_plugin_id) if filter_plugin_id else None,
            'page={0}'.format(page) if page else None
        ]
        return self._get(
            url='{0}components.json'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(filters)
        )

    def show(self, id):
        """
        This API endpoint returns a single component, identified its ID.

        :type id: int
        :param id: Component ID

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "component": {
                    "id": "integer",
                    "name": "string",
                    "summary_metrics": [
                        {
                            "id": "integer",
                            "name": "string",
                            "metric": "string",
                            "value_function": "string",
                            "thresholds": {
                                "caution": "float",
                                "critical": "float"
                            },
                            "values": {
                                "raw": "float",
                                "formatted": "string"
                            }
                        }
                    ]
                }
            }

        """
        return self._get(
            url='{0}components/{1}.json'.format(self.URL, id),
            headers=self.headers,
        )

    def metric_names(self, id, name=None, page=None):
        """
        Return a list of known metrics and their value names for the given resource.

        :type id: int
        :param id: Component ID

        :type name: str
        :param name: Filter metrics by name

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API

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
                        "url": "https://api.newrelic.com/v2/components/{component_id}/metrics.json?page=2",
                        "rel": "last"
                    },
                    "next": {
                        "url": "https://api.newrelic.com/v2/components/{component_id}/metrics.json?page=2",
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
            url='{0}components/{1}/metrics.json'.format(self.URL, id),
            headers=self.headers,
            params=self.build_param_string(params)
        )

    def metric_data(
            self, id, names, values=None, from_dt=None, to_dt=None,
            summarize=False):
        """
        This API endpoint returns a list of values for each of the requested
        metrics. The list of available metrics can be returned using the Metric
        Name API endpoint.

        Metric data can be filtered by a number of parameters, including
        multiple names and values, and by time range. Metric names and values
        will be matched intelligently in the background.

        You can also retrieve a summarized data point across the entire time
        range selected by using the summarize parameter.

        **Note** All times sent and received are formatted in UTC. The default
        time range is the last 30 minutes.

        :type id: int
        :param id: Component ID

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
            url='{0}components/{1}/metrics/data.json'.format(self.URL, id),
            headers=self.headers,
            params=self.build_param_string(params)
        )
