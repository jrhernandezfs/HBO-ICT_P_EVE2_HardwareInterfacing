from pyfirmata2 import Arduino
import time

# ------------------------------------------------------------------------------
# Naam: Jairo Hernandez
# Cursus: Hardware Interfacing EVE2
# Opdracht: Automatische Sensor Kalibratie
# ------------------------------------------------------------------------------
# Beschrijving:
# Deze code kalibreert een **analoge sensor** door de **minimale** en **maximale** waarden 
# te bepalen bij opstarten. Daarna worden alle metingen **genormaliseerd** tussen 0 en 1.
#
# **Functionaliteit:**
# - Bepaalt min/max sensorwaarden in de eerste 5 seconden.
# - Normaliseert alle toekomstige sensorwaarden (tussen 0 en 1).
# - Drukt zowel de **ruwe** als de **gekalibreerde** waarden af.
#
# **Gebruik:**  
# - Handig voor **lijnsensoren, LDR’s, temperatuursensoren, etc.**  
# - Zorgt voor **consistentie** in verschillende lichtomstandigheden of sensorafwijkingen.
# ------------------------------------------------------------------------------

# Verbinden met de Arduino
PORT = Arduino.AUTODETECT  # Automatisch de juiste poort detecteren
board = Arduino(PORT)

print("Arduino gestart")
board.samplingOn(100)  # Stel de sample-interval in op 100ms

# Sensor instellen (bijv. LDR of lijnsensor op A0)
sensor_pin = 'a:0:i'
sensor = board.get_pin(sensor_pin)

# **Kalibratie-parameters**
calibration_time = 5  # Hoe lang (seconden) we data verzamelen voor kalibratie
sensor_min = float('inf')  # Beginwaarde voor minimum
sensor_max = float('-inf')  # Beginwaarde voor maximum

# Callback-functie om de sensorwaarde bij te werken
sensor_value = 0.0
def sensor_callback(value):
    global sensor_value
    sensor_value = value  # Update sensorwaarde

sensor.register_callback(sensor_callback)
sensor.enable_reporting()

# **Stap 1: Kalibratie-fase**
print(f"Kalibreren... Verzamel data voor {calibration_time} seconden.")
start_time = time.time()

while (time.time() - start_time) < calibration_time:
    if sensor_value < sensor_min:
        sensor_min = sensor_value
    if sensor_value > sensor_max:
        sensor_max = sensor_value
    print(f"Meet: {sensor_value:.3f} | Min: {sensor_min:.3f} | Max: {sensor_max:.3f}")
    time.sleep(0.1)  # Kleine vertraging om meetwaarden te stabiliseren

print(f"Kalibratie voltooid! Min: {sensor_min:.3f}, Max: {sensor_max:.3f}")

# **Stap 2: Genormaliseerde uitlezing**
while True:
    user_input = input("Type 'stop' om te stoppen of druk Enter om verder te gaan: ")
    if user_input.lower() == "stop":
        print("Programma beëindigd. Sensor uitlezing gestopt.")
        board.exit()
        break
    
    # **Normaliseren van de sensorwaarde**
    if sensor_max - sensor_min > 0:
        normalized_value = (sensor_value - sensor_min) / (sensor_max - sensor_min)
    else:
        normalized_value = 0  # Voorkom deling door nul als min == max

    print(f"Ruwe waarde: {sensor_value:.3f} | Gekalibreerde waarde: {normalized_value:.3f}")