============
Contributing
============

Contributions and issues are most welcome! Once you have cloned the source
code, you can run the code quality and unit tests by running::

    $ flake8 . --max-line-length=120 --max-complexity=10 --exclude='doc,venv,env,*.egg'
    $ nosetests --cover-branches --with-coverage --cover-min-percentage=100 --cover-package=newrelic_api

