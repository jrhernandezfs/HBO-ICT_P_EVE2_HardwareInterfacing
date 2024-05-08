from pyfirmata import Arduino, util
import time

# Pas dit aan met de juiste COM-poort
board = Arduino('COM3')

# Definieer de pins
led_pins = [9, 10, 11]
for pin in led_pins:
    board.digital[pin].mode = util.OUTPUT

def blink_leds():
    try:
        while True:
            for pin in led_pins:
                board.digital[pin].write(1)  # LED aan
                time.sleep(1)               # Wacht 1 seconde
                board.digital[pin].write(0)  # LED uit
                time.sleep(1)               # Wacht 1 seconde
    except KeyboardInterrupt:
        for pin in led_pins:
            board.digital[pin].write(0)  # Zorg dat alle LEDs uit zijn bij afsluiten
        board.exit()

if __name__ == '__main__':
    blink_leds()
