newrelic-api: A Python interface to New Relic's API
===================================================

newrelic-api is a package for easily interacting with New Relic's API in a
concise, pythonic way. For full documentation on each endpoint, please see
`New Relic's API explorer`_. This is based off of the v2 API.

.. _New Relic's API explorer: https://rpm.newrelic.com/api/explore/


.. toctree::
   :maxdepth: 1

   ref/alert_policies
   ref/applications
   ref/application_hosts
   ref/application_instances
   ref/components
   ref/key_transactions
   ref/notification_channels
   ref/plugins
   ref/servers
   ref/users
   ref/base
   ref/exceptions
   contributing

.. toctree::
   :maxdepth: 2

   releasenotes/index

Installation
============

To install, install via pip or easy_install::

    $ pip install newrelic-api
    or
    $ easy_install newrelic-api

If you want to install it from source, grab the git repository and run setup.py::

 $ git clone git://github.com/ambitioninc/newrelic-api.git
 $ cd newrelic-api
 $ python setup.py install

Configuration
=============

You will need your New Relic API key for authenticating your requests. The
New Relic documentation for accessing this can be found `here`_.

.. _here: https://docs.newrelic.com/docs/apis/api-key

You can set the API key as the environment variable ``NEWRELIC_API_KEY``, or
you can pass the API key as an argument in the interface constructor::

    from newrelic_api import Applications

    app = Applications(NEWRELIC_API_KEY='4baa5d20cfba466a5e075b02698f455c')
    response = app.list(filter_name='demo')

Currently Supported Resources
=============================

* Alert Policies (:doc:`API Reference <ref/alert_policies>`)
* Applications (:doc:`API Reference <ref/applications>`)
* Application Hosts (:doc:`API Reference <ref/application_hosts>`)
* Application Instances (:doc:`API Reference <ref/application_instances>`)
* Components (:doc:`API Reference <ref/components>`)
* Key Transactions (:doc:`API Reference <ref/key_transactions>`)
* Notification Channels (:doc:`API Reference <ref/notification_channels>`)
* Plugins (:doc:`API Reference <ref/plugins>`)
* Servers (:doc:`API Reference <ref/servers>`)
* Users (:doc:`API Reference <ref/users>`)

Internal resources
==================

* Exceptions (:doc:`API Reference <ref/exceptions>`)
* Resource (:doc:`API Reference <ref/base>`)


Release Notes
=============

.. toctree::

   releasenotes/v1.0
   releasenotes/v0.1

Contributing
============

Please see :doc:`Contributing <contributing>`
