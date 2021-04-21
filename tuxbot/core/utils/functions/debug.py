import time


class TimeSpent:
    def __init__(self, *breakpoints):
        self.breakpoints: tuple = breakpoints
        self.times: list = [time.perf_counter()]

    def update(self) -> None:
        self.times.append(time.perf_counter())

    def display(self) -> str:
        output = ""

        for i, value in enumerate(self.breakpoints):
            output += f'\n{value}: {f"{(self.times[i + 1] - self.times[i]) * 1000:.2f}ms" if i + 1 < len(self.times) else "..."}'

        return output
