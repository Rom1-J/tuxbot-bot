from setuptools import setup

setup(
    python_requires=">=3.9",
    install_requires=[
        "aiofiles>=0.8.0",
        "aiocache>=0.11.1",
        "aioredis>=2.0.1",
        "asyncpg>=0.21.0",
        "Babel>=2.8.0",
        "beautifulsoup4>=4.9.3",
        "datadog>=0.43.0",
        "discord.py @ git+https://github.com/iDevision/enhanced-discord.py",
        "discord-ext-menus",
        "graphviz>=0.16",
        "humanize>=2.6.0",
        "ipinfo>=4.1.0",
        "ipwhois>=1.2.0",
        "jishaku @ git+https://github.com/Gorialis/jishaku",
        "Pillow>=8.2.0",
        "psutil>=5.7.2",
        "pydig>=0.3.0",
        "python_json_logger>=2.0.2",
        "rich>=9.10.0",
        "sentry_sdk>=0.20.2",
        "structured_config>=4.12",
        "sympy>=1.8",
        "tortoise-orm>=0.16.17",
        "Wavelink>=0.9.9",
        "wolframalpha>=5.0.0",
    ],
)
