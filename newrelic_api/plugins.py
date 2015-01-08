from .base import Resource


class Plugins(Resource):
    """
    An interface for interacting with the NewRelic Plugins API.
    """
    def list(self, filter_guid=None, filter_ids=None, detailed=None, page=None):
        """
        This API endpoint returns a paginated list of the plugins associated
        with your New Relic account.

        Plugins can be filtered by their name or by a list of IDs.

        :type filter_guid: str
        :param filter_guid: Filter by name

        :type filter_ids: list of ints
        :param filter_ids: Filter by user ids

        :type detailed: bool
        :param detailed: Include all data about a plugin

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results

        ::

            {
                "plugins": [
                    {
                        "id": "integer",
                        "name": "string",
                        "guid": "string",
                        "publisher": "string",
                        "details": {
                            "description": "integer",
                            "is_public": "string",
                            "created_at": "time",
                            "updated_at": "time",
                            "last_published_at": "time",
                            "has_unpublished_changes": "boolean",
                            "branding_image_url": "string",
                            "upgraded_at": "time",
                            "short_name": "string",
                            "publisher_about_url": "string",
                            "publisher_support_url": "string",
                            "download_url": "string",
                            "first_edited_at": "time",
                            "last_edited_at": "time",
                            "first_published_at": "time",
                            "published_version": "string"
                        },
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
                        "url": "https://api.newrelic.com/v2/plugins.json?page=2",
                        "rel": "last"
                    },
                    "next": {
                        "url": "https://api.newrelic.com/v2/plugins.json?page=2",
                        "rel": "next"
                    }
                }
            }

        """
        filters = [
            'filter[guid]={0}'.format(filter_guid) if filter_guid else None,
            'filter[ids]={0}'.format(','.join([str(app_id) for app_id in filter_ids])) if filter_ids else None,
            'detailed={0}'.format(detailed) if detailed is not None else None,
            'page={0}'.format(page) if page else None
        ]

        return self._get(
            url='{0}plugins.json'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(filters)
        )

    def show(self, id, detailed=None):
        """
        This API endpoint returns a single Key transaction, identified its ID.

        :type id: int
        :param id: Key transaction ID

        :type detailed: bool
        :param detailed:

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "plugin": {
                    "id": "integer",
                    "name": "string",
                    "guid": "string",
                    "publisher": "string",
                    "details": {
                        "description": "integer",
                        "is_public": "string",
                        "created_at": "time",
                        "updated_at": "time",
                        "last_published_at": "time",
                        "has_unpublished_changes": "boolean",
                        "branding_image_url": "string",
                        "upgraded_at": "time",
                        "short_name": "string",
                        "publisher_about_url": "string",
                        "publisher_support_url": "string",
                        "download_url": "string",
                        "first_edited_at": "time",
                        "last_edited_at": "time",
                        "first_published_at": "time",
                        "published_version": "string"
                    },
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
        filters = [
            'detailed={0}'.format(detailed) if detailed is not None else None,
        ]
        return self._get(
            url='{root}plugins/{id}.json'.format(
                root=self.URL,
                id=id
            ),
            headers=self.headers,
            params=self.build_param_string(filters) or None
        )
