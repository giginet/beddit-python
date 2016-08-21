
beddit-python
============================
.. image:: https://travis-ci.org/giginet/beddit-python.svg?branch=master :target: https://travis-ci.org/giginet/beddit-python
.. image:: https://coveralls.io/repos/github/giginet/beddit-python/badge.svg?branch=master :target: https://coveralls.io/github/giginet/beddit-python?branch=master

API Client for Beddit_ in Python.

.. _Beddit: https://www.beddit.com

Read `API Documentation`_ for detail.

.. _API Documentation: https://github.com/beddit/beddit-api

Installation
---------------------

.. code:: sh

  pip install beddit-python


Usage
--------------

List sleep scores per day
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

  from datetime import datetime
  from beddit.client import BedditClient

  client = BedditClient('user@example.com', password)

  start_date = datetime(2016, 7, 1)
  end_date = datetime(2016, 7, 31)

  sleeps = client.get_sleeps(start=start_date, end=end_date)
  for sleep in sleeps:
    print(sleep.date.strftime('%Y-%m-%d'), sleep.property.total_sleep_score)


.. code:: txt

  2016-07-01 75
  2016-07-02 92
  ....

Supported Python
------------------------

Python 2.7, 3.3, 3.4, 3.5

LICENSE
----------------

MIT License

