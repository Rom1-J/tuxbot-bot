============
Installation
============

Prerequisites
-------------

* Python 3.10 interpreter (with poetry as package manager)
* PostgreSQL server
* Redis server
* Datadog Agent (optional)
* Sentry App (optional)
* Discord App with following enabled intents:

    * PRESENCE
    * SERVER MEMBERS
    * MESSAGE CONTENT


Python interpreter
^^^^^^^^^^^^^^^^^^

Install Python for your host system.

Assuming Ubuntu Server host and using PPA:

.. code-block:: bash

    $ sudo apt update && sudo apt upgrade -y
    $ sudo apt install software-properties-common -y
    $ sudo add-apt-repository ppa:deadsnakes/ppa
    $ sudo apt install python3.10


Downloading dependencies
^^^^^^^^^^^^^^^^^^^^^^^^

Assuming PostgreSQL already configured, and `Poetry <https://python-poetry.org/docs/#installation>`_ installed:

.. code-block:: bash

    $ git clone https://github.com/Rom1-J/tuxbot-bot /opt/tuxbot-bot
    $ cd /opt/tuxbot-bot
    $ git checkout v4
    $ poetry env use 3.10
    $ poetry shell
    $ poetry install

.. note:: ``wolf`` and ``quote`` commands both need DejaVu Sans font, make sure you have them:

.. code-block:: bash

    $ sudo apt install fonts-dejavu-core fonts-dejavu-extra


Configuration
^^^^^^^^^^^^^

Copy the ``data.example`` directory and adjust for your settings in ``data/settings/{development,production}.yaml``.

.. code-block:: bash

    $ cp -R data.example data

.. note::

    - If you don't want to use `Sentry <https://sentry.io>`_, do not fill in the corresponding key in the config file:

    - If you don't want to use `Datadog <https://datadoghq.com>`_, do not fill in the corresponding key in the config file:


Systemd
^^^^^^^

Create a systemd services.

``/etc/systemd/system/tuxbot.service``

.. code-block:: ini

    [Unit]
    Description=Tuxbot, a discord bot
    After=network.target

    [Service]
    Type=simple
    User=tuxbot

    Restart=on-failure
    Restart=always
    RestartSec=5

    WorkingDirectory=/opt/tuxbot-bot
    ExecStart=<poetry_venv>/bin/ddtrace-run <poetry_venv>/bin/python tuxbot/start.py

    Environment=DD_ACTIVE=true
    Environment=DD_SERVICE="Tuxbot-bot"
    Environment=DD_ENV="Tuxbot-prod"
    Environment=DD_LOGS_INJECTION=true
    Environment=DD_PROFILING_ENABLED=true

    Environment=PYTHON_ENV=production

    Environment=CLUSTER_ID=1
    Environment=CLUSTER_COUNT=1

    Environment=SHARD_ID=0
    Environment=SHARD_COUNT=1

    Environment=FIRST_SHARD_ID=0
    Environment=LAST_SHARD_ID=0

    StandardOutput=file:/opt/tuxbot-bot/data/logs/systemd.log

    [Install]
    WantedBy=multi-user.target


.. note:: if you have not configured `Datadog <https://datadoghq.com>`_, replace the following lines:

.. code-block:: ini

    ExecStart=<poetry_venv>/bin/python tuxbot/start.py

    Environment=DD_ACTIVE=false
