#include <Audio.h>

#define BUTTON 1

AudioControlSGTL5000     sgtl5000_1;

AudioInputI2S            i2s1;
AudioAmplifier           amp1;
AudioAmplifier           amp2;
AudioFilterBiquad        biquad1;
AudioFilterBiquad        biquad2;
AudioOutputI2S           i2s2;
AudioConnection          patchCord1(i2s1, 0, amp1, 0);
AudioConnection          patchCord2(i2s1, 1, amp2, 0);
AudioConnection          patchCord4(amp1, biquad1);
AudioConnection          patchCord3(amp2, biquad2);
AudioConnection          patchCord5(biquad1, 0, i2s2, 0);
AudioConnection          patchCord6(biquad2, 0, i2s2, 1);


float f = 800;   // frequency
float Q = 0.707; // quality factor
int type = 0;    // filter type
int N_types = 2; // number of filter types


void setup() {
  // enable the Teensy Audio Board
  sgtl5000_1.enable();
  sgtl5000_1.volume(0.5);

  Serial.begin(9600);
  while (Serial.available() != 0) {}

  AudioMemory(12);

  // set the BUUTN as input type with a pull-up resistor
  pinMode(BUTTON, INPUT_PULLUP);

  // prepare the filter
  setFilters();

  
}

void loop() {

  // read the values from potentiometers and buttons
  readValues();

  // update the filter
  setFilters();

  delay(200);
}

// read the values from potentiometers and buttons
void readValues(){
  
  // filter type (button read)
  if (digitalRead(BUTTON)==0){
    type = (type+1) % N_types;
  }    

  // frequency (from potentiometer)
  int val = analogRead(A0);
  // logarithmic scale
  f = 20 * pow(10, 3*(val/1024.0));

  // Q factor (from potentiometer)
  val = analogRead(A1);
  // logarithmic scale
  Q = pow(10, 4*(val/1024.0)-2);

}

// set filter
void setFilters(){

  switch (type) {
    case 0:
      biquad1.setLowpass(0, f, Q);
      biquad2.setLowpass(0, f, Q);
      break;
    case 1:
      biquad1.setHighpass(0, f, Q);
      biquad2.setHighpass(0, f, Q);
      break;
  }

  // print variables to serial port
  // (these values are read by the computer)
  Serial.print("type = ");
  Serial.print(type);
  Serial.print("; f = ");
  Serial.print(f);
  Serial.print("; Q = ");
  Serial.println(Q);

  delay(50);
}