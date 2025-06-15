import platform
import logging
from config import LED_PIN

logger = logging.getLogger(__name__)

class LEDController:
    def __init__(self):
        self.is_raspberry_pi = platform.system() == 'Linux' and 'raspberry' in platform.platform().lower()
        self.gpio = None
        
        if self.is_raspberry_pi:
            try:
                import RPi.GPIO as GPIO
                self.gpio = GPIO
                self.gpio.setmode(GPIO.BCM)
                self.gpio.setup(LED_PIN, GPIO.OUT)
                logger.info("Successfully initialized GPIO for LED control")
            except ImportError:
                logger.warning("RPi.GPIO not available, running in simulation mode")
                self.is_raspberry_pi = False
        else:
            logger.info("Not running on Raspberry Pi, using simulation mode")

    def turn_on(self):
        """Turn on the LED."""
        if self.is_raspberry_pi and self.gpio:
            self.gpio.output(LED_PIN, self.gpio.HIGH)
        else:
            print("SIMULATION: LED turned ON")

    def turn_off(self):
        """Turn off the LED."""
        if self.is_raspberry_pi and self.gpio:
            self.gpio.output(LED_PIN, self.gpio.LOW)
        else:
            print("SIMULATION: LED turned OFF")

    def blink(self, times=3, interval=0.5):
        """Blink the LED a specified number of times."""
        import time
        for _ in range(times):
            self.turn_on()
            time.sleep(interval)
            self.turn_off()
            time.sleep(interval)

    def cleanup(self):
        """Clean up GPIO resources."""
        if self.is_raspberry_pi and self.gpio:
            self.gpio.cleanup()
            logger.info("GPIO cleanup completed")

# Create a singleton instance
led_controller = LEDController() 