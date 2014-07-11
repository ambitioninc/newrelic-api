Configuration
=============

You will need your New Relic API key for authenticating your requests. The
New Relic documentation for accessing this can be found `here`_.

.. _here: https://docs.newrelic.com/docs/apis/api-key

You can set the API key as the environment variable ``NEWRELIC_API_KEY``, or
you can pass the API key as an argument in the interface constructor:

.. code-block:: python

    from newrelic_api import Applications

    app = Applications(api_key='4baa5d20cfba466a5e075b02698f455c')
    response = app.list(filter_name='demo')
