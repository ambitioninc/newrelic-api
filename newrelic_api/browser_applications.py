from .base import Resource


class BrowserApplications(Resource):
    """
    An interface for interacting with the NewRelic Browser Application API.
    """
    def list(self, filter_name=None, filter_ids=None, page=None):
        """
        This API endpoint returns a list of the Browser Applications associated
        with your New Relic account.

        Browser Applications can be filtered by their name, or by the
        application IDs.

        :type filter_name: str
        :param filter_name: Filter by application name

        :type filter_ids: list of ints
        :param filter_ids: Filter by application ids

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results

        ::

            {
                "browser_applications": [
                    {
                        "id": "integer",
                        "name": "string",
                        "browser_monitoring_key": "string",
                        "loader_script": "string"
                    }
                ],
                "pages": {
                    "last": {
                        "url": "https://api.newrelic.com/v2/browser_applications.json?page=2",
                        "rel": "last"
                    },
                    "next": {
                        "url": "https://api.newrelic.com/v2/browser_applications.json?page=2",
                        "rel": "next"
                    }
                }
            }

        """
        filters = [
            'filter[name]={0}'.format(filter_name) if filter_name else None,
            'filter[ids]={0}'.format(','.join([str(app_id) for app_id in filter_ids])) if filter_ids else None,
            'page={0}'.format(page) if page else None
        ]

        return self._get(
            url='{0}browser_applications.json'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(filters)
        )

    def create(self, name):
        """
        This API endpoint allows you to create a standalone Browser Application

        :type name: str
        :param name: The name of the application

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "browser_application": {
                    "id": "integer",
                    "name": "string",
                    "browser_monitoring_key": "string",
                    "loader_script": "string"
                }
            }

        """

        data = {
            "browser_application": {
                "name": name
            }
        }

        return self._post(
            url='{0}browser_applications.json'.format(self.URL),
            headers=self.headers,
            data=data
        )
