from .base import Resource


class Labels(Resource):
    """
    An interface for interacting with the NewRelic label API.
    """
    def list(self, page=None):
        """
        This API endpoint returns a paginated list of the Labels
        associated with your New Relic account.

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results

        ::

            {
                "labels": [
                    {
                        "key": "string",
                        "category": "string",
                        "name": "string",
                        "links": {
                            "applications": [
                                "integer"
                            ],
                            "servers": [
                                "integer"
                            ]
                        }
                    }
                ],
                "pages": {
                    "last": {
                        "url": "https://api.newrelic.com/v2/labels.json?page=2",
                        "rel": "last"
                    },
                    "next": {
                        "url": "https://api.newrelic.com/v2/labels.json?page=2",
                        "rel": "next"
                    }
                }
            }

        """

        filters = [
            'page={0}'.format(page) if page else None
        ]

        return self._get(
            url='{0}labels.json'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(filters)
        )

    def create(self, name, category, applications=None, servers=None):
        """
        This API endpoint will create a new label with the provided name and
        category

        :type name: str
        :param name: The name of the label

        :type category: str
        :param category: The Category

        :type applications: list of int
        :param applications: An optional list of application ID's

        :type servers: list of int
        :param servers: An optional list of server ID's

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "label": {
                    "key": "string",
                    "category": "string",
                    "name": "string",
                    "links": {
                        "applications": [
                            "integer"
                        ],
                        "servers": [
                            "integer"
                        ]
                    }
                }
            }

        """

        data = {
            "label": {
                "category": category,
                "name": name,
                "links": {
                    "applications": applications or [],
                    "servers": servers or []
                }
            }
        }

        return self._put(
            url='{0}labels.json'.format(self.URL),
            headers=self.headers,
            data=data
        )

    def delete(self, key):
        """
        When applications are provided, this endpoint will remove those
        applications from the label.

        When no applications are provided, this endpoint will remove the label.

        :type key: str
        :param key: Label key. Example: 'Language:Java'

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "label": {
                    "key": "string",
                    "category": "string",
                    "name": "string",
                    "links": {
                        "applications": [
                            "integer"
                        ],
                        "servers": [
                            "integer"
                        ]
                    }
                }
            }

        """
        return self._delete(
            url='{url}labels/labels/{key}.json'.format(
                url=self.URL,
                key=key),
            headers=self.headers,
        )
