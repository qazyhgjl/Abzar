from dataclasses import dataclass
from pathlib import Path

@dataclass
class Settings:
    fps: int = 60
    speed: float = 1.0
    width: int = 1440
    height: int = 900
    root: Path = Path(__file__).resolve().parent.parent
