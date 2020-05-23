from .base import Resource


class ApplicationDeployments(Resource):
    """
    An interface for interacting with the New Relic Application Deployments API.
    """
    def list(self, application_id, page=None):
        """
        This API endpoint returns a paginated list of the deployments associated
            with a given application.

        :type application_id: int
        :param application_id: Application ID

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results

        ::

            {
                "deployment": {
                    "id": "integer",
                    "revision": "string",
                    "changelog": "string",
                    "description": "string",
                    "user": "string",
                    "timestamp": "datetime",
                    "links": {
                    "application": "integer"
                    }
                }
            }

        """

        filters = [
            f'page={page}' if page else None
        ]
        print(filters)
        return self._get(
            url=f'{self.URL}applications/{application_id}/deployments.json',
            headers=self.headers,
            params=self.build_param_string(filters)
        )

    def create(self, application_id, revision, changelog=None, description=None, user=None, timestamp=None):
        """
        This API endpoint creates a deployment record for a given application.
            Deployment records are created with the following attributes:

        Required:
        - Application ID
        - Revision, such as a git SHA

        Optional:
        - Changelog
        - Description
        - User posting the deployment
        - Timestamp of the deployment

        Note that the optional timestamp of the deployment must be provided in
            UTC and in ISO8601 format. For example, ‘2019-10-08T00:15:36Z’” If
            you have not provided a timestamp, the time of your deployment will
            be recorded as the current time in UTC.

        :type revision: str
        :param revision: A unique ID for this deployment, visible in the
            Overview page and on the Deployments page. Can be any string,
            but is usually a version number or a Git checksum, 127 character maximum

        :type changelog: str
        :param changelog: A summary of what changed in this deployment, visible
            in the Deployments page when you select (selected deployment)
            > Change log, 65535 character maximum

        :type description: str
        :param description: A high-level description of this deployment, visible
            in the Overview page and on the Deployments page when you select an
            individual deployment, 65535 character maximum

        :type user: str
        :param user: A username to associate with the deployment, visible in
            the Overview page and on the Deployments page, 31 character maximum

        :type timestamp: str
        :param timestamp: When the deployment occurred, down to the second.
            If not specified, the deployment will be recorded at the time
            when the API call was received.
            
            Timestamp requirements:
            
            Must be in UTC time.
            
            Must be after the most recent deployment timestamp.
            
            Cannot be in the future.
            
            Must be in ISO8601 format; for example, "2019-10-08T00:15:36Z"

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "deployment": {
                    "id": "integer",
                    "revision": "string",
                    "changelog": "string",
                    "description": "string",
                    "user": "string",
                    "timestamp": "datetime",
                    "links": {
                    "application": "integer"
                    }
                }
            }

        """

        data = {
            "deployment": {
                "revision": revision,
                "changelog": changelog,
                "description": description,
                "user": user
            }
        }

        return self._post(
            url=f'{self.URL}applications/{application_id}/deployments.json',
            headers=self.headers,
            data=data
        )

    def delete(self, application_id, deployment_id=None):
        """
        This API endpoint deletes the specified deployment record.

        Note: Admin User’s API Key is required.

        :type application_id: int
        :param application_id: Application ID

        :type id: int
        :param id: Deployment ID

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "deployment": {
                    "id": "integer",
                    "revision": "string",
                    "changelog": "string",
                    "description": "string",
                    "user": "string",
                    "timestamp": "datetime",
                    "links": {
                    "application": "integer"
                    }
                }
            }

        """
        return self._delete(
            url=f'{self.URL}applications/{application_id}/deployments/{deployment_id}.json',
            headers=self.headers
        )
