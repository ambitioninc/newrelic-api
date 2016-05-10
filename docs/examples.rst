Examples
========

As stated in :doc:`Configuration <configuration>`, you need to pass in your API
key to the constructor for each resource class, or set the ``NEW_RELIC_API_KEY``
environment variable. The following examples assume the environment variable
is set.

Applications & AlertPolicies Example
------------------------------------

**Scenario:** Say we want to move our application, 'Marketing Website' from
the default Alert Policy, 'Marketing Policy', to a second Alert Policy, 'Marketing Policy2'.

First we need to get the ID for our application and the alert policy that we
want to add it to:

.. code-block:: python

    from newrelic_api import AlertPolicies, Applications

    website_app_id = Applications().list(
        filter_name='Marketing Website'
    )['applications'][0]['id']

    marketing_policy = AlertPolicies().list(
        filter_name='Marketing Policy',
        filter_type=['application'],
        filter_enabled=True
    )['alert_policies'][0]

    
Next, we need to determine if our application is already in the alert_policy.
Since each alert_policy dictionary in the the AlertPolicies ``.list()``
method response has an inner dictionary ``links`` with a key ``applications``
whose value is a list of application ids, we can simply check if the id for
'Marketing Website' is in the list.

.. code-block:: python

    app_in_policy = website_app_id in marketing_policy.get('links', {}).get('applications')


Finally, we need to construct a new policy and call ``.update()`` with the new
policy for 'Marketing Policy'.

.. code-block:: python

    if app_in_policy:
        app_ids = marketing_policy['links']['applications']
        app_ids.append(website_app_id)


        new_alert_policy = AlertPolicies().list(
            filter_name='Marketing Policy2',
            filter_type=['application'],
            filter_enabled=True
        )['alert_policies'][0]

        new_alert_policy_wrapper = {"alert_policy": {"test":"test"}}
        new_alert_policy_wrapper['alert_policy'] = new_alert_policy
        new_alert_policy_wrapper['alert_policy']['links']['applications'] = app_ids


        AlertPolicies().update(
            id=new_alert_policy_wrapper['alert_policy']['id'],
            policy_update=new_alert_policy_wrapper
        )

