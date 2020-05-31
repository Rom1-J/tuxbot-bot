from .settings import token, postgresql, logs, ipinfo

protected = [
    token, str(list(token)),
    postgresql, str(list(postgresql)),
    *[channel.get('webhook').get('token') for channel in logs.values()],
    ipinfo
]

