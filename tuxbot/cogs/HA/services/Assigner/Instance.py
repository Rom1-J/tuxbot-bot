"""
Instance
"""

from websockets import server as ws_server


class Instance:
    """Instance"""

    _name: str
    _hostname: str
    _port: int

    _client: ws_server.WebSocketServerProtocol = None
    _alive: bool = False
    _ping: float = float('inf')

    def __init__(self, name: str, hostname: str, port: int):
        self.name = name
        self.hostname = hostname
        self.port = port

    # =========================================================================

    def __repr__(self):
        return "<Instance name='%s' uri='%s' alive=%s ping=%s>" % (
            self.name, self.uri, self.alive, str(self.ping)
        )

    __str__ = __repr__

    # =========================================================================
    # =========================================================================

    @property
    def name(self) -> str:
        """instance name"""
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    # =========================================================================

    @property
    def hostname(self) -> str:
        """instance hostname"""
        return self._hostname

    @hostname.setter
    def hostname(self, value: str):
        self._hostname = value

    # =========================================================================

    @property
    def port(self) -> int:
        """instance port"""
        return self._port

    @port.setter
    def port(self, value: int):
        self._port = value

    # =========================================================================

    @property
    def client(self) -> ws_server.WebSocketServerProtocol:
        """instance ws client"""
        return self._client

    @client.setter
    def client(self, value: ws_server.WebSocketServerProtocol):
        self._client = value

    # =========================================================================

    @property
    def alive(self) -> bool:
        """instance alive"""
        return self._alive

    @alive.setter
    def alive(self, value: bool):
        self._alive = value

    # =========================================================================

    @property
    def ping(self) -> float:
        """instance ping"""
        return self._ping

    @ping.setter
    def ping(self, value: float):
        self._ping = value

    # =========================================================================

    @property
    def uri(self) -> str:
        """Websocket uri"""
        return f"ws://{self.hostname}:{self.port}/"

    # =========================================================================
