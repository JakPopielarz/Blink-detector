#define VALUE_ARRAY_SIZE 100

int sensorPin = A0;
int sensorValue = 0;
int ledPin = 3;
int values[VALUE_ARRAY_SIZE]; 
int lastFilledIndex = 0;

/*
Setup array of values - set every element to -1,
which indicates it hasn't been used yet.
*/
void setupValueArray(int valueArray[]) {
   for (int i=0; i<VALUE_ARRAY_SIZE; i++) {
      valueArray[i] = -1;
   }
}

/*
Save a value to the array - if there are still elements previously not used
override them; if the array is already full - shift elements to the left and
insert new one on the end.
*/
void saveValue(int valueArray[], int value) {
   if (lastFilledIndex < VALUE_ARRAY_SIZE) {
      int index = lastFilledIndex + 1;
      valueArray[index] = value;
      lastFilledIndex++;
   } else {
      for (int i=0; i<VALUE_ARRAY_SIZE-1; i++) {
         valueArray[i] = valueArray[i+1];
      }
      valueArray[VALUE_ARRAY_SIZE-1] = value;
   }
}

/*
Print out an array in one line:
[x0, x1, x2, x3, x4, ]
*/
void serialPrintArray(int array[], int size) {
   Serial.print("[");
   for (int i=0; i<size; i++) {
      Serial.print(array[i]);
      Serial.print(", ");
   }
   Serial.println("]");
}

void setup(void) {
   setupValueArray(values);

   Serial.begin(9600);
   pinMode(sensorPin, INPUT);
   // pinMode(ledPin, OUTPUT);
   analogReference(INTERNAL);
}
 
void loop(void) {
   // digitalWrite(ledPin, HIGH);
   delay(2);
   sensorValue = analogRead(sensorPin);
   saveValue(values, sensorValue);
   serialPrintArray(values, VALUE_ARRAY_SIZE);
   delay(1);
   // digitalWrite(ledPin, LOW);
   delay(7);
}
