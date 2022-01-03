int sensorPin = A0;
int sensorValue = 0;

void setup(void) {
   Serial.begin(9600);
   pinMode(sensorPin, INPUT);
   pinMode(3, OUTPUT);
   digitalWrite(3, HIGH);
   analogReference(INTERNAL);
}
 
void loop(void) {
   sensorValue = analogRead(sensorPin);
   Serial.println(sensorValue);
   delay(10);
}
