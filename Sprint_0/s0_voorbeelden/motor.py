from pyfirmata2 import Arduino
import time

# ------------------------------------------------------------------------------
# Naam: Jairo Hernandez
# Cursus: Hardware Interfacing EVE2
# Inhoud: PWM-snelheidsdemo met busy waiting en automatische stop
# ------------------------------------------------------------------------------
# Beschrijving:
# Deze code stelt gebruikers in staat om verschillende PWM-snelheden te testen 
# op de motoren zonder `time.sleep()`. De gebruiker voert een percentage (0-100) in, 
# dat wordt omgerekend naar een PWM-duty cycle (0.0 - 1.0). De motoren draaien 
# **exact 1 seconde**, waarna ze automatisch stoppen. Vervolgens wordt een nieuwe invoer gevraagd.
# De loop stopt als de gebruiker "stop" invoert.
#
# **Belangrijke opmerking:**
# - De snelheid moet tussen 0 en 100 procent liggen.
# - Dit programma helpt bij het testen en demonstreren van motorrespons op PWM.
# - In plaats van `time.sleep()`, wordt busy waiting gebruikt voor nauwkeurige timing.
# ------------------------------------------------------------------------------

# Verbinden met de Arduino
PORT = Arduino.AUTODETECT  # Automatisch de juiste poort detecteren
board = Arduino(PORT)

print("Arduino gestart")
board.samplingOn(100)  # Stel de sample-interval in op 100ms

print("Verbinding met de Arduino opgezet.")

# Setup de digitale PWM-pinnen voor motoren
pwm_3 = board.get_pin('d:3:p')   # Linkermotor
pwm_11 = board.get_pin('d:11:p') # Rechtermotor

# Hoofdprogramma: vraag PWM-invoer en pas deze toe
while True:
    v = input("Geef een PWM duty cycle in (0-100) of type 'stop' om te stoppen: ")

    if v.lower() == "stop":
        print("Programma beëindigd. Motoren stoppen...")
        pwm_3.write(0)
        pwm_11.write(0)
        board.exit()
        break
    
    try:
        pwm_value = float(v) / 100.0
        if 0.0 <= pwm_value <= 1.0:
            print(f"Instellen van PWM op {int(pwm_value * 100)}%...")
            pwm_3.write(pwm_value)
            pwm_11.write(pwm_value)

            # 1 seconde
            time.sleep(1)
            
            # Automatisch de motoren uitschakelen na 1 seconde
            pwm_3.write(0)
            pwm_11.write(0)
            print("Motoren gestopt.")

        else:
            print("Fout: Voer een getal in tussen 0 en 100.")
    except ValueError:
        print("Fout: Ongeldige invoer. Voer een getal in of typ 'stop'.")

# Sluit de seriële verbinding correct af (indien niet via 'stop' gestopt)
board.exit()