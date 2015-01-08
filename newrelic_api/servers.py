from .base import Resource


class Servers(Resource):
    """
    An interface for interacting with the NewRelic server API.
    """
    def list(self, filter_name=None, filter_ids=None, filter_labels=None, page=None):
        """
        This API endpoint returns a paginated list of the Servers
        associated with your New Relic account. Servers can be filtered
        by their name or by a list of server IDs.

        :type filter_name: str
        :param filter_name: Filter by server name

        :type filter_ids: list of ints
        :param filter_ids: Filter by server ids

        :type filter_labels: dict of label type: value pairs
        :param filter_labels: Filter by server labels

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results

        ::

            {
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
                ],
                "pages": {
                    "last": {
                        "url": "https://api.newrelic.com/v2/servers.json?page=2",
                        "rel": "last"
                    },
                    "next": {
                        "url": "https://api.newrelic.com/v2/servers.json?page=2",
                        "rel": "next"
                    }
                }
            }

        """
        label_param = ''

        if filter_labels:
            label_param = ';'.join(['{}:{}'.format(label, value) for label, value in filter_labels.items()])

        filters = [
            'filter[name]={0}'.format(filter_name) if filter_name else None,
            'filter[ids]={0}'.format(','.join([str(app_id) for app_id in filter_ids])) if filter_ids else None,
            'filter[labels]={0}'.format(label_param) if filter_labels else None,
            'page={0}'.format(page) if page else None
        ]

        return self._get(
            url='{0}servers.json'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(filters)
        )

    def show(self, id):
        """
        This API endpoint returns a single Server, identified its ID.

        :type id: int
        :param id: Server ID

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "server": {
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
            }

        """
        return self._get(
            url='{0}servers/{1}.json'.format(self.URL, id),
            headers=self.headers,
        )

    def update(self, id, name=None):
        """
        Updates any of the optional parameters of the server

        :type id: int
        :param id: Server ID

        :type name: str
        :param name: The name of the server

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "server": {
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
            }

        """
        nr_data = self.show(id)['server']

        data = {
            'server': {
                'name': name or nr_data['name'],
            }
        }

        return self._put(
            url='{0}servers/{1}.json'.format(self.URL, id),
            headers=self.headers,
            data=data
        )

    def delete(self, id):
        """
        This API endpoint deletes an server and all of its reported data.

        WARNING: Only servers that have stopped reporting can be deleted.
            This is an irreversible process which will delete all reported
            data for this server.

        :type id: int
        :param id: Server ID

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "server": {
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
            }

        """
        return self._delete(
            url='{0}servers/{1}.json'.format(
                self.URL,
                id),
            headers=self.headers,
        )

    def metric_names(self, id, name=None, page=None):
        """
        Return a list of known metrics and their value names for the given resource.

        :type id: int
        :param id: Server ID

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
                        "url": "https://api.newrelic.com/v2/servers/{server_id}/metrics.json?page=2",
                        "rel": "last"
                    },
                    "next": {
                        "url": "https://api.newrelic.com/v2/servers/{server_id}/metrics.json?page=2",
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
            url='{0}servers/{1}/metrics.json'.format(self.URL, id),
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
        :param id: Server ID

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
            url='{0}servers/{1}/metrics/data.json'.format(self.URL, id),
            headers=self.headers,
            params=self.build_param_string(params)
        )
