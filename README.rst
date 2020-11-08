|image0| |image1| |image2|

.. role:: bash(code)
   :language: bash

Installing Tuxbot
=================

It is preferable to install the bot on a dedicated user. If you don't
know how to do it, please refer to `this guide <https://www.digitalocean.com/community/tutorials/how-to-create-a-sudo-user-on-ubuntu-quickstart>`__

Installing the pre-requirements
-------------------------------

-  The pre-requirements are:

   -  Python 3.7 or greater
   -  Pip
   -  Git

Operating systems
~~~~~~~~~~~~~~~~~

Arch Linux
^^^^^^^^^^

.. code-block:: bash

    $ sudo pacman -Syu python python-pip python-virtualenv git

Continue to `create the venv <#creating-the-virtual-environment>`__.

--------------

Debian
^^^^^^

.. code-block:: bash

    $ sudo apt update
    $ sudo apt -y install python3 python3-dev python3-pip python3-venv git

Continue to `create the venv <#creating-the-virtual-environment>`__.

--------------

Windows
^^^^^^^

*not for now and not for the future*

Creating the Virtual Environment
--------------------------------

To set up the virtual environment and install the bot, simply run this
two commands:

.. code-block:: bash

    $ make
    $ make install

Now, switch your environment to the virtual one by run this single
command: :bash:`source ~/tuxvenv/bin/activate`

Configuration
-------------

It's time to set up your first instance, to do this, you can simply
execute this command:

:bash:`tuxbot-setup [your instance name]`

After following the instructions, you can run your instance by executing
this command:

:bash:`tuxbot [your instance name]`

Update
------

To update the whole bot after a :bash:`git pull`, just execute

.. code-block:: bash

    $ make update

.. |image0| image:: https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-%23007ec6
.. |image1| image:: https://img.shields.io/badge/dynamic/json?color=%23dfb317&label=issues&query=%24.open_issues_count&suffix=%20open&url=https%3A%2F%2Fgit.gnous.eu%2Fapi%2Fv1%2Frepos%2FGnousEU%2Ftuxbot-bot%2F
.. |image2| image:: https://img.shields.io/badge/code%20style-black-000000.svg