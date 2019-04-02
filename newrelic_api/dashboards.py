from .base import Resource


class Dashboards(Resource):
    """
    An interface for interacting with the NewRelic dashboard API.
    """
    def list(self, filter_title=None, filter_ids=None, page=None):
        """
        :type filter_title: str
        :param filter_title: Filter by dashboard title

        :type filter_ids: list of ints
        :param filter_ids: Filter by dashboard ids

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API, with an additional 'page' key
            if there are paginated results

        ::

            {
                "dashboards": [
                    {
                        "id": "integer",
                        "title": "string",
                        "description": "string",
                        "icon": "string",
                        "created_at": "time",
                        "updated_at": "time",
                        "visibility": "string",
                        "editable": "string",
                        "ui_url": "string",
                        "api_url": "string",
                        "owner_email": "string",
                        "filter": {
                            "event_types": ["string"],
                            "attributes": ["string"]
                        }
                    }
                ],
                "pages": {
                    "last": {
                        "url": "https://api.newrelic.com/v2/dashboards.json?page=1&per_page=100",
                        "rel": "last"
                    },
                    "next": {
                        "url": "https://api.newrelic.com/v2/dashboards.json?page=1&per_page=100",
                        "rel": "next"
                    }
                }
            }
        """
        filters = [
            'filter[title]={0}'.format(filter_title) if filter_title else None,
            'filter[ids]={0}'.format(','.join([str(dash_id) for dash_id in filter_ids])) if filter_ids else None,
            'page={0}'.format(page) if page else None
        ]
        return self._get(
            url='{0}dashboards.json'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(filters)
        )

    def show(self, id):
        """
        This API endpoint returns a single Dashboard, identified by its ID.

        :type id: int
        :param id: Dashboard ID

        :rtype: dict
        :return: The JSON response of the API

        ::
            {
                "dashboard": {
                    "id": "integer",
                    "title": "string",
                    "description": "string",
                    "icon": "string",
                    "created_at": "string",
                    "updated_at": "string",
                    "visibility": "string",
                    "editable": "string",
                    "ui_url": "string",
                    "api_url": "string",
                    "owner_email": "string",
                    "metadata": {
                        "version": "integer"
                    },
                    "widgets": [
                        {
                            "visualization": "string",
                            "layout": {
                                "width": "integer",
                                "height": "integer",
                                "row": "integer",
                                "column": "integer"
                            },
                            "widget_id": "integer",
                            "account_id": "integer",
                            "data": [
                                {
                                    "nrql": "string"
                                }
                            ],
                            "presentation": {
                                "title": "string",
                                "notes": "string"
                            }
                        }
                    ],
                    "filter": {
                        "event_types": ["string"],
                        "attributes": ["string"]
                    }
                }
            }
        """
        return self._get(
            url='{0}dashboards/{1}.json'.format(self.URL, id),
            headers=self.headers,
        )

    def delete(self, id):
        """
        This API endpoint deletes a dashboard and all its widgets.

        :type id: int
        :param id: Dashboard ID

        :rtype: dict
        :return: The JSON response of the API

        ::
            {
                "dashboard": {
                    "id": "integer"
                }
            }
        """
        return self._delete(
            url='{0}dashboards/{1}.json'.format(self.URL, id),
            headers=self.headers,
        )

    def create(self, dashboard_data):
        """
        This API endpoint creates a dashboard and all defined widgets.

        :type dashboard: dict
        :param dashboard: Dashboard Dictionary

        :rtype dict
        :return: The JSON response of the API

        ::
            {
                "dashboard": {
                    "id": "integer",
                    "title": "string",
                    "description": "string",
                    "icon": "string",
                    "created_at": "time",
                    "updated_at": "time",
                    "visibility": "string",
                    "editable": "string",
                    "ui_url": "string",
                    "api_url": "string",
                    "owner_email": "string",
                    "metadata": {
                        "version": "integer"
                    },
                    "widgets": [
                        {
                            "visualization": "string",
                            "layout": {
                                "width": "integer",
                                "height": "integer",
                                "row": "integer",
                                "column": "integer"
                            },
                            "widget_id": "integer",
                            "account_id": "integer",
                            "data": [
                                "nrql": "string"
                            ],
                            "presentation": {
                                "title": "string",
                                "notes": "string"
                            }
                        }
                    ],
                    "filter": {
                        "event_types": ["string"],
                        "attributes": ["string"]
                    }
                }
            }
        """
        return self._post(
            url='{0}dashboards.json'.format(self.URL),
            headers=self.headers,
            data=dashboard_data,
        )

    def update(self, id, dashboard_data):
        """
        This API endpoint updates a dashboard and all defined widgets.

        :type id: int
        :param id: Dashboard ID

        :type dashboard: dict
        :param dashboard: Dashboard Dictionary

        :rtype dict
        :return: The JSON response of the API

        ::
            {
                "dashboard": {
                    "id": "integer",
                    "title": "string",
                    "description": "string",
                    "icon": "string",
                    "created_at": "time",
                    "updated_at": "time",
                    "visibility": "string",
                    "editable": "string",
                    "ui_url": "string",
                    "api_url": "string",
                    "owner_email": "string",
                    "metadata": {
                        "version": "integer"
                    },
                    "widgets": [
                        {
                            "visualization": "string",
                            "layout": {
                                "width": "integer",
                                "height": "integer",
                                "row": "integer",
                                "column": "integer"
                            },
                            "widget_id": "integer",
                            "account_id": "integer",
                            "data": [
                                "nrql": "string"
                            ],
                            "presentation": {
                                "title": "string",
                                "notes": "string"
                            }
                        }
                    ],
                    "filter": {
                        "event_types": ["string"],
                        "attributes": ["string"]
                    }
                }
            }
        """
        return self._put(
            url='{0}dashboards/{1}.json'.format(self.URL, id),
            headers=self.headers,
            data=dashboard_data,
        )
