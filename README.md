# Installing Tuxbot

It is preferable to install the bot on a dedicated user. If you don't know how to do it, please refer to [this guide](https://www.digitalocean.com/community/tutorials/how-to-create-a-sudo-user-on-ubuntu-quickstart)

## Installing the pre-requirements

  - The pre-requirements are:
      - Python 3.7 or greater
      - Pip
      - Git
      - JRE 11 (voice support)

### Operating systems

-----

### Arch Linux

```shell script
sudo pacman -Syu python python-pip git jre11-openjdk-headless base-devel
```

Continue by [creating virtual env](#creating-a-virtual-env).

-----

#### Debian Stretch

```shell script
sudo echo "deb http://deb.debian.org/debian stretch-backports main" >> /etc/apt/sources.list.d/tuxbot.list
sudo apt update
sudo apt -y install make build-essential python3-openssl git openjdk-11-jre-headless
```

Continue by [creating virtual env](#creating-a-virtual-env).

## Creating a virtual env

Make sure you have the virtualenv package installed before following the next steps.

Create the virtual environment by executing the following command:
```shell script
python3 -m venv ~/tuxvenv
```

And activate it with this command:
```shell script
source ~/tuxvenv/bin/activate
```

## Installing Tuxbot

Now, you can finish the installation by executing this single command:
```shell script
python setup.py install
```

## Configuration

todo...