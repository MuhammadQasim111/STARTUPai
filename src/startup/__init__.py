from .agent import StartupAIAgent
from .cli import main

__all__ = ["StartupAIAgent", "main"]

def main() -> None:
    print("Hello from startup!")
