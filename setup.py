"""
Tuxbot
~~~~~~~

bot made initially for https://gnous.eu, then proposed to the entire
free software community
"""

from setuptools import find_packages, setup

from tuxbot import __version__


with open("README.rst") as f:
    long_description = f.read()


setup(
    name="Tuxbot-bot",
    version=__version__,
    url="https://github.com/Rom1-J/tuxbot-bot/",
    author="Romain J.",
    author_email="romain@gnous.eu",
    maintainer="Romain J.",
    maintainer_email="romain@gnous.eu",
    description="A discord bot made for GnousEU's guild and OpenSource",
    long_description=long_description,
    license="agplv3",
    platforms="linux",
    python_requires=">=3.10",
    install_requires=[
        "aiofiles>=0.8.0",
        "aioredis>=2.0.1",
        "asyncpg>=0.21.0",
        "beautifulsoup4>=4.9.3",
        "datadog>=0.43.0",
        "ddtrace>=0.60.0",
        "discord.py @ git+https://github.com/Rapptz/discord.py",
        "discord-ext-menus>=1.1",
        "graphviz>=0.16",
        "humanize>=2.6.0",
        "ipinfo>=4.1.0",
        "ipwhois>=1.2.0",
        "jishaku @ git+https://github.com/Gorialis/jishaku",
        "Pillow>=8.2.0",
        "psutil>=5.7.2",
        "pydig>=0.3.0",
        "python_json_logger>=2.0.2",
        "PyYAML>=6.0",
        "rich>=9.10.0",
        "sentry_sdk>=0.20.2",
        "sympy>=1.8",
        "tortoise-orm>=0.16.17",
        "websockets>=10.3",
        "wolframalpha>=5.0.0",
    ],
    package_dir={"tuxbot": "tuxbot"},
    packages=find_packages(),
    package_data={"tuxbot": ["tuxbot/*", "tuxbot/**/*"]},
    include_package_data=True,
)
