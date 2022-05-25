int sensorPin = A0;
int sensorValue = 0;

void setup(void) {
   Serial.begin(9600);
   pinMode(sensorPin, INPUT);
   pinMode(3, OUTPUT);
   analogReference(INTERNAL);
}
 
void loop(void) {
   digitalWrite(3, HIGH);
   delay(2);
   sensorValue = analogRead(sensorPin);
   Serial.println(sensorValue);
   delay(1);
   digitalWrite(3, LOW);
   delay(7);
}
