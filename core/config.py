import os
from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class BuzzerSettings:
    PIN: int = 14
    DEFAULT_FREQUENCY: int = 2500

@dataclass(frozen=True)
class LCDSettings:
    RS: int = 18
    EN: int = 23
    DATA_PINS: List[int] = field(default_factory=lambda: [12, 16, 20, 21])
    COLS: int = 16
    ROWS: int = 2
    SSH_MESSAGE: str = "Acesso via SSH"

@dataclass(frozen=True)
class Config:
    PORT: int = int(os.environ.get("PORT", "8888"))
    LISTEN_ADDRESS: str = "0.0.0.0"
    STATIC_PATH: str = os.path.join(os.path.dirname(__file__), "..", "client", "static")
    DEFAULT_PAGE: str = "index.html"
    LCD: LCDSettings = field(default_factory=LCDSettings)
    BUZZER: BuzzerSettings = field(default_factory=BuzzerSettings)

config = Config()