from setuptools import setup

setup(
    python_requires=">=3.8",
    install_requires=[
        "aiocache>=0.11.1",
        "asyncpg>=0.21.0",
        "Babel>=2.8.0",
        "beautifulsoup4>=4.9.3",
        "discord.py @ git+https://github.com/Rapptz/discord.py",
        "discord-ext-menus",
        "graphviz>=0.16",
        "humanize>=2.6.0",
        "ipinfo>=4.1.0",
        "ipwhois>=1.2.0",
        "jishaku @ git+https://github.com/Gorialis/jishaku",
        "Pillow>=8.2.0",
        "python-Levenshtein>=0.12.2.",
        "psutil>=5.7.2",
        "pydig>=0.3.0",
        # "ralgo @ git+https://github.com/Rom1-J/ralgo",
        "rich>=9.10.0",
        "sentry_sdk>=0.20.2",
        "structured_config>=4.12",
        "sympy>=1.8",
        "tortoise-orm>=0.16.17",
        "wolframalpha>=5.0.0",
    ],
)
