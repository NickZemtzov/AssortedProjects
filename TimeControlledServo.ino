#include <Servo.h>
#include <Wire.h>
#include <TimeLib.h>
#include <DS1307RTC.h>
#include <HX711_ADC.h>
#include <EEPROM.h>

//pins:
const int HX711_dout = 4; //mcu > HX711 dout pin
const int HX711_sck = 5; //mcu > HX711 sck pin
//HX711 constructor:
HX711_ADC LoadCell(HX711_dout, HX711_sck);
const int calVal_eepromAdress = 0;
unsigned long t = 0;
float TypicalWeightOnBed = 1000;//ur mac charger is 286.6
bool OnBed = false;
float weight = 0;

Servo myservo;
int pos = 0;

tmElements_t activationTime; 

void setup() {
  myservo.attach(9);
  Serial.begin(9600);
  while (!Serial) ; // wait for serial
  delay(200);
  
  activationTime.Second = 0; //this is where you set the time. It's military time
  activationTime.Minute = 9;
  activationTime.Hour = 22;
  Serial.print("Servo Should Activate at: "); 
  Serial.print(activationTime.Hour);
  Serial.write(',');
  Serial.print(activationTime.Minute);
  Serial.write(',');
  Serial.println(activationTime.Second);

  LoadCell.begin();
  unsigned long stabilizingtime = 2000; // preciscion right after power-up can be improved by adding a few seconds of stabilizing time
  boolean _tare = false; //set this to false if you don't want tare to be performed in the next step
  LoadCell.start(stabilizingtime, _tare);
  if (LoadCell.getTareTimeoutFlag() || LoadCell.getSignalTimeoutFlag()) {
    Serial.println("Timeout, check MCU>HX711 wiring and pin designations");
    while (1);
  }
  else {
    LoadCell.setCalFactor(1.0); // user set calibration value (float), initial value 1.0 may be used for this sketch
    Serial.println("Startup is complete");
  }
  while (!LoadCell.update());
  calibrate(); //start calibration procedure
}
  

void loop() {
  tmElements_t tm;
  if (RTC.read(tm)) {
      Serial.print("Ok, Time = ");
      print2digits(tm.Hour);
      Serial.write(':');
      print2digits(tm.Minute);
      Serial.write(':');
      print2digits(tm.Second);
      Serial.print(", Date (D/M/Y) = ");
      Serial.print(tm.Day);
      Serial.write('/');
      Serial.print(tm.Month);
      Serial.write('/');
      Serial.print(tmYearToCalendar(tm.Year));
      Serial.println();

      static boolean newDataReady = 0;
      const int serialPrintInterval = 0; //increase value to slow down serial print activity
    
      // check for new data/start next conversion:
      if (LoadCell.update()) newDataReady = true;
    
      // get smoothed value from the dataset:
      if (newDataReady) {
        if (millis() > t + serialPrintInterval) {
          weight = LoadCell.getData();
          Serial.print("Load_cell output val: ");
          Serial.println(weight);
          newDataReady = 0;
          t = millis();
        }
      }

      // receive command from serial terminal
      if (Serial.available() > 0) {
        char inByte = Serial.read();
        if (inByte == 't') LoadCell.tareNoDelay(); //tare
        else if (inByte == 'r') calibrate(); //calibrate
        else if (inByte == 'c') changeSavedCalFactor(); //edit calibration value manually
      }
    
      // check if last tare operation is complete
      if (LoadCell.getTareStatus() == true) {
        Serial.println("Tare complete");
      }

      if (tm.Hour == activationTime.Hour && tm.Minute == activationTime.Minute && tm.Second == activationTime.Second) {
        //initial reading of whether on bed  or not
        if (weight > TypicalWeightOnBed && OnBed == false) {
          OnBed = true;
          activationTime.Minute = activationTime.Minute + 5;//Idk if this will have issues if over 60 but just don't do that
          Serial.println("Alarm will go off in 5 minutes");
        } else if (weight > TypicalWeightOnBed && OnBed == true) {
          OnBed = false;
          activationTime.Minute = activationTime.Minute - 5;
          for (pos = 0; pos <= 120; pos += 1) {
            myservo.write(pos);              
            delay(20);                       //delay is in ms
          }
          for (pos = 10; pos >= 0; pos -= 1) { 
            myservo.write(pos);              
            delay(20);                       
          }
        }
      }

  delay(1000);
  }
}


void print2digits(int number) {
  if (number >= 0 && number < 10) {
    Serial.write('0');
  }
  Serial.print(number);
}

void calibrate() {
  Serial.println("***");
  Serial.println("Start calibration:");
  Serial.println("Place the load cell an a level stable surface.");
  Serial.println("Remove any load applied to the load cell.");
  Serial.println("Send 't' from serial monitor to set the tare offset.");

  boolean _resume = false;
  while (_resume == false) {
    LoadCell.update();
    if (Serial.available() > 0) {
      if (Serial.available() > 0) {
        char inByte = Serial.read();
        if (inByte == 't') LoadCell.tareNoDelay();
      }
    }
    if (LoadCell.getTareStatus() == true) {
      Serial.println("Tare complete");
      _resume = true;
    }
  }

  Serial.println("Now, place your known mass on the loadcell.");
  Serial.println("Then send the weight of this mass (i.e. 100.0) from serial monitor.");

  float known_mass = 0;
  _resume = false;
  while (_resume == false) {
    LoadCell.update();
    if (Serial.available() > 0) {
      known_mass = Serial.parseFloat();
      if (known_mass != 0) {
        Serial.print("Known mass is: ");
        Serial.println(known_mass);
        _resume = true;
      }
    }
  }

  LoadCell.refreshDataSet(); //refresh the dataset to be sure that the known mass is measured correct
  float newCalibrationValue = LoadCell.getNewCalibration(known_mass); //get the new calibration value

  Serial.print("New calibration value has been set to: ");
  Serial.print(newCalibrationValue);
  Serial.println(", use this as calibration value (calFactor) in your project sketch.");
  Serial.print("Save this value to EEPROM adress ");
  Serial.print(calVal_eepromAdress);
  Serial.println("? y/n");

  _resume = false;
  while (_resume == false) {
    if (Serial.available() > 0) {
      char inByte = Serial.read();
      if (inByte == 'y') {
#if defined(ESP8266)|| defined(ESP32)
        EEPROM.begin(512);
#endif
        EEPROM.put(calVal_eepromAdress, newCalibrationValue);
#if defined(ESP8266)|| defined(ESP32)
        EEPROM.commit();
#endif
        EEPROM.get(calVal_eepromAdress, newCalibrationValue);
        Serial.print("Value ");
        Serial.print(newCalibrationValue);
        Serial.print(" saved to EEPROM address: ");
        Serial.println(calVal_eepromAdress);
        _resume = true;

      }
      else if (inByte == 'n') {
        Serial.println("Value not saved to EEPROM");
        _resume = true;
      }
    }
  }

  Serial.println("End calibration");
  Serial.println("***");
  Serial.println("To re-calibrate, send 'r' from serial monitor.");
  Serial.println("For manual edit of the calibration value, send 'c' from serial monitor.");
  Serial.println("***");
}

void changeSavedCalFactor() {
  float oldCalibrationValue = LoadCell.getCalFactor();
  boolean _resume = false;
  Serial.println("***");
  Serial.print("Current value is: ");
  Serial.println(oldCalibrationValue);
  Serial.println("Now, send the new value from serial monitor, i.e. 696.0");
  float newCalibrationValue;
  while (_resume == false) {
    if (Serial.available() > 0) {
      newCalibrationValue = Serial.parseFloat();
      if (newCalibrationValue != 0) {
        Serial.print("New calibration value is: ");
        Serial.println(newCalibrationValue);
        LoadCell.setCalFactor(newCalibrationValue);
        _resume = true;
      }
    }
  }
  _resume = false;
  Serial.print("Save this value to EEPROM adress ");
  Serial.print(calVal_eepromAdress);
  Serial.println("? y/n");
  while (_resume == false) {
    if (Serial.available() > 0) {
      char inByte = Serial.read();
      if (inByte == 'y') {
#if defined(ESP8266)|| defined(ESP32)
        EEPROM.begin(512);
#endif
        EEPROM.put(calVal_eepromAdress, newCalibrationValue);
#if defined(ESP8266)|| defined(ESP32)
        EEPROM.commit();
#endif
        EEPROM.get(calVal_eepromAdress, newCalibrationValue);
        Serial.print("Value ");
        Serial.print(newCalibrationValue);
        Serial.print(" saved to EEPROM address: ");
        Serial.println(calVal_eepromAdress);
        _resume = true;
      }
      else if (inByte == 'n') {
        Serial.println("Value not saved to EEPROM");
        _resume = true;
      }
    }
  }
  Serial.println("End change calibration value");
  Serial.println("***");
}
