from hardware.display import LCDManager
from hardware.buzzer import BuzzerManager
from core.logger import get_logger

logger = get_logger("HardwareSystem")

class HardwareSystem:
    def __init__(self):
        self.lcd = LCDManager()
        self.buzzer = BuzzerManager()

    def startup_sequence(self, ip: str):
        logger.info("Iniciando sequência de boot do hardware...")
        self.lcd.show_idle(ip)
        self.buzzer.play_imperial_march()

    def notify_victory(self, winner: str):
        self.lcd.show_status("Vencedor!", f"Jogador {winner}")
        self.buzzer.play_mario_victory()

    def update_game_status(self, turn: str, game_over: bool):
        if game_over:
            self.lcd.show_status("Fim de Jogo!", "")
        else:
            self.lcd.show_status("Vez do jogador:", turn)