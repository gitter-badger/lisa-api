===============================
lisa-api
===============================

| |docs| |travis| |coveralls|
| |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/lisa-api/badge/?style=flat
    :target: https://readthedocs.org/projects/lisa-api
    :alt: Documentation Status

.. |travis| image:: https://img.shields.io/travis/project-lisa/lisa-api.svg
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/project-lisa/lisa-api

.. |coveralls| image:: https://img.shields.io/coveralls/project-lisa/lisa-api.svg
    :alt: Coverage Status
    :target: https://coveralls.io/r/project-lisa/lisa-api

.. |version| image:: http://img.shields.io/pypi/v/lisa-api.png?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/lisa-api

.. |downloads| image:: http://img.shields.io/pypi/dm/lisa-api.png?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/lisa-api

.. |wheel| image:: https://pypip.in/wheel/lisa-api/badge.png?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/lisa-api

.. |supported-versions| image:: https://pypip.in/py_versions/lisa-api/badge.png?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/lisa-api

.. |supported-implementations| image:: https://pypip.in/implementation/lisa-api/badge.png?style=flat
    :alt: Supported imlementations
    :target: https://pypi.python.org/pypi/lisa-api

Lisa-api is a core component of LISA Project. It provides a REST api and execute all actions for the LISA project.

* Free software: Apache license

Installation
============
::

    pip install lisa-api

Documentation
=============

https://lisa-api.readthedocs.org/

You can also play with the api by going to http://url-of-lisa/

Development
===========
To run the server::

    python lisa_api/server.py

To run the all tests run::

    tox
