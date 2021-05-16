|image0| |image1| |image2| |image3|

.. role:: bash(code)
   :language: bash

Installing Tuxbot
=================

It is preferable to install the bot on a dedicated user. If you don't
know how to do it, please refer to `this guide <https://www.digitalocean.com/community/tutorials/how-to-create-a-sudo-user-on-ubuntu-quickstart>`__

Installing the pre-requirements
-------------------------------

-  The pre-requirements are:

   -  Python 3.8 or greater
   -  Pip
   -  Git

Operating systems
~~~~~~~~~~~~~~~~~

Arch Linux
^^^^^^^^^^

.. code-block:: bash

    $ sudo pacman -Syu python python-pip python-virtualenv git make gcc postgresql

Continue to `configure postgresql <#configure-postgresql>`__.

--------------

Debian
^^^^^^

.. code-block:: bash

    $ sudo apt update
    $ sudo apt -y install python3 python3-dev python3-pip python3-venv git make gcc postgresql postgresql-client

Continue to `configure postgresql <#configure-postgresql>`__.

--------------

RHEL and derivatives (CentOS, Fedora...)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ sudo dnf update
    $ sudo dnf install python3 python3-devel python3-pip python3-virtualenv git make gcc postgresql-server postgresql-contrib

Continue to `configure postgresql <#configure-postgresql>`__.

--------------

Windows
^^^^^^^

*not for now and not for the future*

--------------

Configure PostgreSQL
--------------------

Now, you need to setup PostgreSQL

Operating systems
~~~~~~~~~~~~~~~~~

Arch Linux
^^^^^^^^^^

https://wiki.archlinux.org/index.php/PostgreSQL

Continue to `create the venv <#creating-the-virtual-environment>`__.

--------------

Debian
^^^^^^

https://wiki.debian.org/PostgreSql

Continue to `create the venv <#creating-the-virtual-environment>`__.

--------------

RHEL and derivatives (CentOS, Fedora...)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

https://fedoraproject.org/wiki/PostgreSQL

Continue to `create the venv <#creating-the-virtual-environment>`__.

--------------

Creating the Virtual Environment
--------------------------------

To set up the virtual environment and install the bot, simply run this
two commands:

.. code-block:: bash

    $ make
    $ make install

Now, switch your environment to the virtual one by run this single
command: :bash:`source ~/venv/bin/activate`

Configuration
-------------

It's time to set up your first instance, to do this, you can simply
execute this command:

:bash:`tuxbot-setup`

After following the instructions, you can run your instance by executing
this command:

:bash:`tuxbot`

Update
------

To update the whole bot after a :bash:`git pull`, just execute

.. code-block:: bash

    $ make update

.. |image0| image:: https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-%23007ec6
.. |image1| image:: https://img.shields.io/github/issues/Rom1-J/tuxbot-bot
.. |image2| image:: https://img.shields.io/badge/code%20style-black-000000.svg
.. |image3| image:: https://wakatime.com/badge/github/Rom1-J/tuxbot-bot.svg
    :target: https://wakatime.com/badge/github/Rom1-J/tuxbot-bot
