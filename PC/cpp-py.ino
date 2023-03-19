// DHT declaration
#include "DHT.h"
#define DHTPIN 2           // Digital pin 2 connected to the DHT sensor
#define DHTTYPE DHT22      // Sensor type
DHT dht(DHTPIN, DHTTYPE);  // Initialize DHT sensor.
#define FANPIN 3           // Digital pin 3 connected to Fan motor

// Water level detection sensor module declaration
#define SENSORPIN A0        // Analog pin 0 connected to water level sensor
#define BUZZER 4           // Digital pin 4 connected to buzzer

// Photo sensor module declaration
#define PHOTOPIN A1         // Analog pin 1 at Photoresistor 
#define REDLED 7           // Led pin at Arduino pin 7
#define BLUELED 8          // Led pin at Arduino pin 8


void setup() {
  pinMode(FANPIN, OUTPUT); // The fan sensor will be an output to the arduino

  pinMode(SENSORPIN, INPUT); // The liquid level sensor will be an input to the arduino

  pinMode(PHOTOPIN, INPUT);// Set pResistor as an input
  pinMode(REDLED, OUTPUT);  // Set lepPin as an output
  pinMode(BLUELED, OUTPUT);  // Set lepPin as an output

  Serial.begin(115200);
  Serial.setTimeout(1);  // Sets the baud rate for data transfer in bits/second
  while (!Serial);
  dht.begin();
}

void loop() {
  while (!Serial.available());
  String str(Serial.readString());
  char str_array[str.length()+1];
  str.toCharArray(str_array, str.length()+1);

  if (strcmp(str_array, "readT") == 0) {
    Serial.print(dht.readTemperature(true));
    Serial.print(",");
    Serial.print(dht.readTemperature());
  }

  if (strcmp(str_array, "hot") == 0) { 
    analogWrite(FANPIN, 150);   
    digitalWrite(BLUELED, LOW); // Stop turning up blinds
    digitalWrite(REDLED, HIGH); // Turn down blinds
  } else if (strcmp(str_array, "cold") == 0) { // If cold, open blinds 
    analogWrite(FANPIN, 0);   
    digitalWrite(REDLED, LOW); // Stop turning up blinds
    digitalWrite(BLUELED, HIGH); // Turn up blinds   
  } else {
    int light = analogRead(PHOTOPIN);
    analogWrite(FANPIN, 0);   
    if (light > 900){ // Its bright AND not cold, red led on -> Close blinds
      digitalWrite(BLUELED, LOW); // Stop turning up blinds
      digitalWrite(REDLED, HIGH); // Turn down blinds
    } else if (light < 500){ // Its dark, blue led on -> Open blinds
      digitalWrite(REDLED, LOW); // Stop turning up blinds
      digitalWrite(BLUELED, HIGH); // Turn up blinds   
    } else {
      digitalWrite(REDLED, LOW); // Stop turning up blinds
      digitalWrite(BLUELED, LOW); // Stop turning up blinds
    }  
  }

  // Check water level, if less than half, an alarm will turn on
  int water = analogRead(SENSORPIN);
  if ( water < 255){ tone(BUZZER, 2500); }// Send 1KHz sound signal...
  else { noTone(BUZZER); }
}