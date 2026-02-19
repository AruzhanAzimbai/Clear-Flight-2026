const int buzzerPin = 8;
char command;

void setup() {
  pinMode(buzzerPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    command = Serial.read();

    if (command == 'H') {
      tone(buzzerPin, 1200);   // громкий отпугивающий звук
    }

    if (command == 'L') {
      noTone(buzzerPin);
    }
  }
}
