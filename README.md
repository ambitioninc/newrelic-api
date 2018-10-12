# newrelic-api: A Python interface to New Relic's API

Forked from [https://github.com/ambitioninc/newrelic-api](https://github.com/ambitioninc/newrelic-api)
which is out of date and no longer maintained.

A package for easily interacting with New Relic's API in a
concise, pythonic way. For full documentation on each endpoint, please see
New Relic's API explorer.

This is based off of the v2 API and is currently out of date, update is in
progress.

* New Relic's API explorer: https://rpm.newrelic.com/api/explore/

## Installation

### Pip

This module has not been pushed to any repositories so installation from
Git is the only option:

```BASH
# Direct
pip install git+ssh://git@github.com/sansible/newrelic-api.git@vx.x.x
# requirements file
...
git+ssh://git@github.com/sansible/newrelic-api.git@vx.x.x
...
```

### Source

If you want to install from source, grab the git repository and run setup.py:

```BASH
git clone git@github.com:sansible/newrelic-api.git
cd newrelic-api
python setup.py install
```

## Local development

Tests can be run like so:

```bash
make test
```
