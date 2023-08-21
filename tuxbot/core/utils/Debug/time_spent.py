"""Log time spent between each update."""
import time
import typing


class TimeSpent:
    """Log time spent between each update."""

    def __init__(self: typing.Self) -> None:
        self.order: list[str] = []
        self.times: dict[str, list[float]] = {}

    def start(self: typing.Self, name: str) -> None:
        """Start timer."""
        self.order.append(name)
        self.times[name] = [time.perf_counter()]

    def stop(self: typing.Self, name: str) -> None:
        """Stop timer."""
        self.times[name].append(time.perf_counter())

    def display(self: typing.Self) -> str:
        """Return breakpoints."""
        output = ""

        for point in self.order:
            delta = "..."

            if len(self.times[point]) == 2:
                delta = str(
                    (self.times[point][1] - self.times[point][0]) * 1000
                )
                delta = f"{delta:.2f}ms"

            output += f"\n{point}: {delta}"

        return output
