from pyfirmata2 import Arduino

# ------------------------------------------------------------------------------
# Naam: Jairo Hernandez
# Cursus: Hardware Interfacing EVE2
# Inhoud: Individuele sensor uitlezen en testen
# ------------------------------------------------------------------------------
# Beschrijving:
# Deze code stelt gebruikers in staat om **individuele sensoren** op de Arduino te testen. 
# De sensorwaarde wordt continu uitgelezen en weergegeven in de console.
# 
# **Functionaliteit:**
# - Verbindt met de Arduino en activeert een analoge sensor.
# - Leest de sensorwaarden en toont deze live in de console.
#
# **Gebruik:** 
# - Handig om te testen of een sensor correct is aangesloten en functioneert.
# - Mogelijk om te kalibreren door drempelwaarden te analyseren.
# ------------------------------------------------------------------------------

# Verbinden met de Arduino
PORT = Arduino.AUTODETECT  # Automatisch de juiste poort detecteren
board = Arduino(PORT)

print("Arduino gestart")
board.samplingOn(100)  # Stel de sample-interval in op 100ms

# Koppel een sensor aan analoge pin A0
sensor = board.get_pin('a:0:i')
sensor_value = 0.0  # Opslag voor sensorwaarde

# Callback-functie om de sensorwaarde bij te werken
def sensor_callback(value):
    global sensor_value
    sensor_value = value  # Sla de gemeten sensorwaarde op

# Koppel de callback-functie en activeer de sensor
sensor.register_callback(sensor_callback)
sensor.enable_reporting()

# Hoofdprogramma: blijf sensorwaarden weergeven totdat gebruiker "stop" invoert
while True:
    print(sensor_value)
