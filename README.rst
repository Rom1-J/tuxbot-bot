|image0| |image1| |image2| |image3|


Tuxbot
======

Tuxbot, made by `GnousEU <https://gnous.eu/>`_


Project Purpose
---------------

**Tuxbot** is a discord bot written in python and maintained since 2017.
Its main missions are to propose useful commands for domains related to network, system administration, mathematics and others.

--------------

Basic Makefile Commands
-----------------------


Type checks
~~~~~~~~~~~

Running type and lint checks with ``pre_commit``:

.. code-block:: bash

    $ make pre_commit


Running development instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To run a development instance:

.. code-block:: bash

    $ make dev


Sentry
~~~~~~

Sentry is an error logging aggregator service. You can sign up for a free account at `<https://sentry.io/signup/>`_ or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

--------------

Deployment
----------

The following details how to deploy this application.

Refer to `INSTALL.rst <./INSTALL.rst>`_


.. |image0| image:: https://img.shields.io/badge/python-3.10-%23007ec6
.. |image1| image:: https://img.shields.io/github/issues/Rom1-J/tuxbot-bot
.. |image2| image:: https://img.shields.io/badge/code%20style-black-000000.svg
.. |image3| image:: https://wakatime.com/badge/github/Rom1-J/tuxbot-bot.svg
    :target: https://wakatime.com/badge/github/Rom1-J/tuxbot-bot
