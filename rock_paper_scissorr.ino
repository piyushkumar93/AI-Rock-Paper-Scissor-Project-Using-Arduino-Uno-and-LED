String gesture;
int redLED = 8;
int greenLED = 9;
int yellowLED = 10;
int buzzer = 11;
int whiteLED = 12;

void setup() {
  Serial.begin(9600);
  pinMode(redLED, OUTPUT);
  pinMode(greenLED, OUTPUT);
  pinMode(yellowLED, OUTPUT);
  pinMode(whiteLED, OUTPUT);
  pinMode(buzzer, OUTPUT);
}

void playBuzzer() {
  digitalWrite(buzzer, HIGH);
  delay(100);
  digitalWrite(buzzer, LOW);
}

void resetOutputs() {
  digitalWrite(redLED, LOW);
  digitalWrite(greenLED, LOW);
  digitalWrite(yellowLED, LOW);
  digitalWrite(whiteLED, LOW);
}

void loop() {
  if (Serial.available()) {
    gesture = Serial.readStringUntil('\n');
    gesture.trim();  // Remove any whitespace or newline characters

    resetOutputs();  // Turn off all LEDs
    playBuzzer();    // Play buzzer on any gesture

    if (gesture == "Rock") {
      digitalWrite(redLED, HIGH);
    } else if (gesture == "Paper") {
      digitalWrite(greenLED, HIGH);
    } else if (gesture == "Scissors") {
      digitalWrite(yellowLED, HIGH);
    } else if (gesture == "Normal") {
      digitalWrite(whiteLED, HIGH);
    }

    // Debug print (optional)
    Serial.println("Detected: " + gesture);
  }
}
