from rich.console import Console
from rich.traceback import install


console = Console()
install(console=console, show_locals=True, width=console.width)
