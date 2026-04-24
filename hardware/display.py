try:
    from RPLCD.gpio import CharLCD
    import RPi.GPIO as GPIO
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

from core.logger import get_logger
from core.config import config

logger = get_logger("LCDManager")

class LCDManager:
    def __init__(self):
        self.lcd = None
        if HAS_HARDWARE:
            try:
                GPIO.setmode(GPIO.BCM)
                self.lcd = CharLCD(
                    numbering_mode=GPIO.BCM,
                    cols=config.LCD.COLS,
                    rows=config.LCD.ROWS,
                    pin_rs=config.LCD.RS,
                    pin_e=config.LCD.EN,
                    pins_data=config.LCD.DATA_PINS,
                )
                logger.info("LCD inicializado com sucesso.")
            except Exception as e:
                logger.warning(f"Falha ao inicializar LCD: {e}")
                self.lcd = None

    def show_status(self, line1: str, line2: str = ""):
        if self.lcd:
            self.lcd.clear()
            self.lcd.write_string(line1[:16])
            if line2:
                self.lcd.cursor_pos = (1, 0)
                self.lcd.write_string(line2[:16])
        else:
            logger.info(f"[LCD SIMULADO] {line1} | {line2}")

    def show_idle(self, ip: str):
        self.show_status("Jogo da Velha", ip)