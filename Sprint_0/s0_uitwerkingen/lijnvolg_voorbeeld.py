from pyfirmata2 import Arduino
import time

# ------------------------------------------------------------------------------
# Naam: Jairo Hernandez
# Cursus: Hardware Interfacing EVE2
# Inhoud: Lijnvolgende robot voor restaurantnavigatie
# ------------------------------------------------------------------------------
# Beschrijving:
# Deze code is bedoeld als basisimplementatie voor een lijnvolgende robot in het 
# kader van de EVE2-opdracht. De robot gebruikt vijf lijnsensoren om een lijn te 
# volgen en twee motoren om te navigeren. Hij past zijn richting aan op basis 
# van een beslisboom.
#
# **Belangrijke opmerking:**
# - Alle configuratiewaarden zoals motorsnelheden, drempelwaarden en sensorlogica 
#   kunnen variëren afhankelijk van de specifieke hardware, omgevingsfactoren 
#   en gewenste precisie.
# - Dit is een eenvoudige opzet en vereist verdere uitbreiding en optimalisatie.
# - Deze code kan collega's helpen als startpunt bij hun eigen implementatie.
#
# **Link met de datapunten:**
# - Sprint 0 - Datapunt 5: Sensorinstellingen en uitlezing
# - Sprint 1 - Datapunt 4: Lijnen volgen met bochten
# Deze code implementeert de basisconfiguratie van sensoren en een beslisboom voor 
# lijnvolging en bochtdetectie.
# ------------------------------------------------------------------------------

# Verbinden met de Arduino
PORT = Arduino.AUTODETECT  # Automatisch de juiste poort detecteren
board = Arduino(PORT)

print("Arduino gestart")
board.samplingOn(100)  # Stel de sample-interval in op 100ms

# Definieer de pins voor de lijnsensoren (analoge input)
SENSOR_PINS = ['a:0:i', 'a:1:i', 'a:2:i', 'a:3:i', 'a:4:i']  # A0 t/m A4

# Drempelwaarde voor lijnherkenning (zwart)
THRESHOLD = 0.2  # **Let op:** Dit moet worden aangepast op basis van sensorwaarden!

# Definieer de motorpins (PWM voor snelheid)
motor_links = board.get_pin('d:11:p')  # PWM pin voor linker motor
motor_rechts = board.get_pin('d:3:p')  # PWM pin voor rechter motor

# Variabelen voor sensorwaarden
sensor_waarden = [0.0] * 5  # Opslaan van A0 t/m A4 sensorwaarden

# Callback-functies om sensorwaarden te updaten
def sensor_callback(index):
    def callback(value):
        sensor_waarden[index] = value
    return callback

# Sensoren instellen en callbacks registreren
sensoren = []
for i, pin in enumerate(SENSOR_PINS):
    sensor = board.get_pin(pin)
    sensor.register_callback(sensor_callback(i))
    sensor.enable_reporting()
    sensoren.append(sensor)

# Functie om de motorsnelheden in te stellen
def zet_motoren(snelheid_links, snelheid_rechts):
    motor_links.write(snelheid_links)  # Snelheid tussen 0 (stop) en 1 (vol gas)
    motor_rechts.write(snelheid_rechts)

# Hoofdprogramma
def loop():
    while True:
        # Print de actuele sensorwaarden voor debugging
        print(f"Sensorwaarden: {sensor_waarden}")

        # Controleer of de middelste sensor (A2) de lijn detecteert
        if sensor_waarden[2] < THRESHOLD:
            # Lijn in het midden -> recht vooruit rijden
            zet_motoren(0.2, 0.2)  # **Let op:** Pas snelheid aan op basis van tests!
        else:
            # Lijn niet in het midden, corrigeer richting
            if sensor_waarden[1] < THRESHOLD:
                # Lijn gedetecteerd door linker sensor (A1), stuur naar links
                zet_motoren(0.2, 0.3)  
            elif sensor_waarden[3] < THRESHOLD:
                # Lijn gedetecteerd door rechter sensor (A3), stuur naar rechts
                zet_motoren(0.3, 0.2)
            else:
                # Geen lijn gedetecteerd -> stop of zoek naar de lijn
                zet_motoren(0, 0)

        time.sleep(0.1)  # Korte vertraging om CPU-gebruik te beperken

# Start het programma
if __name__ == "__main__":
    try:
        loop()
    except KeyboardInterrupt:
        # Stop de motoren en sluit de verbinding af bij onderbreking
        zet_motoren(0, 0)
        board.exit()
