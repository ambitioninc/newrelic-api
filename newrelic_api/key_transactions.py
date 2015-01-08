from .base import Resource


class KeyTransactions(Resource):
    """
    An interface for interacting with the NewRelic key transactions API.
    """
    def list(self, filter_name=None, filter_ids=None, page=None):
        """
        This API endpoint returns a paginated list of the key transactions
        associated with your New Relic account.

        Key transactions can be filtered by their name or by a list of IDs.

        :type filter_name: str
        :param filter_name: Filter by name

        :type filter_ids: list of ints
        :param filter_ids: Filter by user ids

        :type page: int
        :param page: Pagination index

        :rtype: dict
        :return: The JSON response of the API, with an additional 'pages' key
            if there are paginated results

        ::

            {
                "key_transactions": [
                    {
                        "id": "integer",
                        "name": "string",
                        "transaction_name": "string",
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
                        "links": {
                            "application": "integer"
                        }
                    }
                ],
                "pages": {
                    "last": {
                        "url": "https://api.newrelic.com/v2/key_transactions.json?page=2",
                        "rel": "last"
                    },
                    "next": {
                        "url": "https://api.newrelic.com/v2/key_transactions.json?page=2",
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
            url='{0}key_transactions.json'.format(self.URL),
            headers=self.headers,
            params=self.build_param_string(filters)
        )

    def show(self, id):
        """
        This API endpoint returns a single Key transaction, identified its ID.

        :type id: int
        :param id: Key transaction ID

        :rtype: dict
        :return: The JSON response of the API

        ::

            {
                "key_transaction": {
                    "id": "integer",
                    "name": "string",
                    "transaction_name": "string",
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
                    "links": {
                        "application": "integer"
                    }
                }
            }

        """
        return self._get(
            url='{root}key_transactions/{id}.json'.format(
                root=self.URL,
                id=id
            ),
            headers=self.headers,
        )
