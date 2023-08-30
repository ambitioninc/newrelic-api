Release Notes
=============

v1.0.7
------

* Read the docs config v2

v1.0.6
------

* Makes a start on supporting the latest New Relic APIs
* Adds support for Alert Conditions
* Adds support NRQL Alerts
* Updates/fixes for V2 Alert policies
* Adds support for Notification Channels

v1.0.4
------

* Added ``pages`` in response for paginated responses
* Added Labels and Browser Application support

v1.0.3
------

* Add support for filtering server via labels - `@mwarkentin`_
* Check for error on responses
* PUTS now json-encode input

.. _@mwarkentin: https://github.com/mwarkentin

v1.0.2
------
* Updated to match the `New Relic Python agent's`_ use of environment variables

.. _New Relic Python agent's: https://docs.newrelic.com/docs/agents/python-agent/installation-configuration/python-agent-configuration#environment-variables

v1.0.1
------
* Added example usage to docs
* Added python 3.3, 3.4 compatibility

v1.0
----

This is a feature release of newrelic-api.

Added API resources include

* Application Hosts
* Application Instances
* Key Transactions
* Plugins
* Components

All resources have updated documentation with API schema response examples.

v0.1
----

This is the initial release of newrelic-api.

Current API resources include

* Alert Policies
* Applications
* Notification Channels
* Servers
* Users
