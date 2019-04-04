.. image:: https://travis-ci.org/ambitioninc/newrelic-api.png
   :target: https://travis-ci.org/ambitioninc/newrelic-api

.. image:: https://coveralls.io/repos/ambitioninc/newrelic-api/badge.png?branch=develop
    :target: https://coveralls.io/r/ambitioninc/newrelic-api?branch=develop

.. image:: https://pypip.in/v/newrelic-api/badge.png
    :target: https://pypi.python.org/pypi/newrelic-api
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/newrelic-api/badge.png
    :target: https://pypi.python.org/pypi/newrelic-api
    :alt: Number of PyPI downloads

newrelic-api: A Python interface to New Relic's API
===================================================

newrelic-api is a package for easily interacting with New Relic's API in a
concise, pythonic way. For full documentation on each endpoint, please see
`New Relic's API explorer`_. This is based off of the v2 API.

.. _New Relic's API explorer: https://rpm.newrelic.com/api/explore/

Project status
==============

This client is out of sync with the latest changes to New Relic's APIs, work
is under way to update this project and bring it up to date. If you need to
use an NR resource that is not supported or is out of date then please submit
a PR.

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

Documentation
=============

All documentation can be found at http://new-relic-api.readthedocs.org

Author
======
`Micah Hausler`_

.. _Micah Hausler: mailto:micah.hausler@ambition.com
