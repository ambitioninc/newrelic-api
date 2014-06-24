[![Build Status](https://travis-ci.org/ambitioninc/newrelic-api.svg?branch=master)](https://travis-ci.org/ambitioninc/newrelic-api)
New Relic Api
=============
newrelic-api is a package for easily interacting with New Relic's API in a
concise, pythonic way. For full documentation on each endpoint, please see
[New Relic's API explorer](https://rpm.newrelic.com/api/explore/). This is
based off of the v2 API.

## Configuration

You will need your New Relic API key for authenticating your requests. The
New Relic documentation for accessing this can be found
[here](https://docs.newrelic.com/docs/apis/api-key)

You can set the API key in the constructor for each interface like below:

```python
from newrelic_api import Applications

app = Applications(NEWRELIC_API_KEY='4baa5d20cfba466a5e075b02698f455c')
response = app.list(filter_name='demo')
```

or you can set it as the environment variable `NEWRELIC_API_KEY`

## Documentation

All documentation can be found at http://newrelic-api.readthedocs.org

## Author
[Micah Hausler](mailto:micah.hausler@ambition.com)
