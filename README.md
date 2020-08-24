Tuxbot is a french speaking Discord bot made for the GnousEU's discord server. He has been maintened since 2016.

This code is not intended to reuse "as is". If you want to configure your own instance, you will need to modify some files in the source code (see below).

### Requirements
- A server with a modern GNU/Linux distribution with internet connectivity 
- Python 3.7 or later with PIP
- Graphviz

### Installation
Install Python dependencies using ``pip3 install -r requirements.txt`` (make sure the pip executable match the correct python version)

Rename ``config.py.example`` to ``config.py`` and edit it with the required information. 
You may want to edit the file ``cogs/filter_messages.py`` as well.  

### Launch 
Start the program using ``python3 bot.py`` (make sure you use the right Python executable)

### Additional features 
#### Ipinfo.io API 
Tuxbot can use the ipinfo.io API for more precises results for the ``iplocalise`` command. If you want to use it you should create a ``ipinfoio.key`` in the top tuxbot folder.

### Versions
Version list : [Click here to display](https://git.gnous.eu/gnouseu/tuxbot-bot/releases)

### Main contributors
* **Maël** _alias_ [@outoutxyz](https://twitter.com/outoutxyz)
* **Romain** _alias_ [Romain le malchanceux](https://github.com/Rom194)

### Licensing

This project is under the ``Creative Commons BY-NC-SA 4.0`` license - see [LICENSE.md](LICENSE.md) for more details 
