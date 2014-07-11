# import multiprocessing to avoid this bug (http://bugs.python.org/issue15881#msg170215)
import multiprocessing
assert multiprocessing
import re
from setuptools import setup, find_packages


def get_version():
    """
    Extracts the version number from the version.py file.
    """
    VERSION_FILE = 'newrelic_api/version.py'
    mo = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', open(VERSION_FILE, 'rt').read(), re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError('Unable to find version string in {0}.'.format(VERSION_FILE))


setup(
    name='newrelic-api',
    version=get_version(),
    description='A python interface to the New Relic API v2',
    long_description=open('README.rst').read(),
    url='https://github.com/ambitioninc/newrelic-api',
    author='Micah Hausler',
    author_email='opensource@ambition.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    install_requires=[
        'requests>=2.0.0'
    ],
    test_suite='nose.collector',
    tests_require=[
        'coverage>=3.7.1',
        'mock>=1.0.1',
        'nose>=1.3.0',
    ],
    include_package_data=True,
    zip_safe=True,
)
