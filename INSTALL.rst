============
Installation
============

Prerequisites
-------------

* Python 3.10 interpreter (with poetry as package manager)
* PostgreSQL server
* Redis server
* Datadog Agent (optional)

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

Assuming PostgreSQL already installed and project cloned in ``/opt/tuxbot-bot``:

.. code-block:: bash

    $ cd /opt/tuxbot-bot
    $ poetry install


Configuration
^^^^^^^^^^^^^

Copy the ``data.example`` directory and adjust for your settings in ``data/settings/{development,production}.yaml``.

.. code-block:: bash

    $ cp -R data.example data

.. note:: If you don't want to use `Sentry <https://sentry.io>`_, do not fill in the corresponding key in the config file:


Systemd
^^^^^^^

Create a systemd services.

`/etc/systemd/system/tuxbot.socket`

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

    WorkingDirectory=/opt/tuxbot-bot/tuxbot
    ExecStart=/opt/tuxbot-bot/venv/bin/ddtrace-run /opt/tuxbot-bot/venv/bin/python start.py

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
