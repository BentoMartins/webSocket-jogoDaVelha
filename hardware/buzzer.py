try:
    import RPi.GPIO as GPIO
    HAS_HARDWARE = True
except ImportError:
    HAS_HARDWARE = False

from core.logger import get_logger
from core.config import config

logger = get_logger("BuzzerManager")

class BuzzerManager:
    def __init__(self):
        self.pwm = None
        if HAS_HARDWARE:
            try:
                GPIO.setup(config.BUZZER.PIN, GPIO.OUT)
                self.pwm = GPIO.PWM(config.BUZZER.PIN, config.BUZZER.DEFAULT_FREQUENCY)
                logger.info("Buzzer inicializado com sucesso.")
            except Exception as e:
                logger.warning(f"Falha ao inicializar Buzzer: {e}")
                self.pwm = None

    def beep(self, frequency: int = 1000, duration: float = 0.2):
        if self.pwm:
            self.pwm.start(50)
            self.pwm.ChangeFrequency(frequency)
            import time; time.sleep(duration)
            self.pwm.stop()
        else:
            logger.info(f"[BUZZER SIMULADO] {frequency}Hz por {duration}s")

    def play_mario_victory(self):
        notes = [
            (660, 0.1), (660, 0.1), (0, 0.1), (660, 0.1),
            (0, 0.1), (510, 0.1), (660, 0.1), (0, 0.1),
            (770, 0.1), (0, 0.3), (380, 0.3),
        ]
        logger.info("[BUZZER] Tocando tema de vitória!")
        for freq, dur in notes:
            if freq == 0:
                import time; time.sleep(dur)
            else:
                self.beep(freq, dur)

    def play_imperial_march(self):
        notes = [
            (440, 0.3), (440, 0.3), (440, 0.3), (349, 0.2),
            (523, 0.1), (440, 0.3), (349, 0.2), (523, 0.1), (440, 0.4),
        ]
        logger.info("[BUZZER] Tocando marcha imperial!")
        for freq, dur in notes:
            self.beep(freq, dur)