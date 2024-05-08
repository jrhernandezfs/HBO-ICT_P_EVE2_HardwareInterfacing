// Definieer de pinnen waarop de LEDs zijn aangesloten
const int ledPin1 = 9;
const int ledPin2 = 10;
const int ledPin3 = 11;

void setup() {
  // Stel elk van de LED-pinnen in als een uitgang
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);
}

void loop() {
  // Zet LED 1 aan, wacht, zet het uit
  digitalWrite(ledPin1, HIGH);   // Zet LED 1 aan
  delay(1000);                   // Wacht 1 seconde
  digitalWrite(ledPin1, LOW);    // Zet LED 1 uit

  // Zet LED 2 aan, wacht, zet het uit
  digitalWrite(ledPin2, HIGH);   // Zet LED 2 aan
  delay(1000);                   // Wacht 1 seconde
  digitalWrite(ledPin2, LOW);    // Zet LED 2 uit

  // Zet LED 3 aan, wacht, zet het uit
  digitalWrite(ledPin3, HIGH);   // Zet LED 3 aan
  delay(1000);                   // Wacht 1 seconde
  digitalWrite(ledPin3, LOW);    // Zet LED 3 uit

  // Wacht even voordat we de cyclus herhalen
  delay(1000);
}