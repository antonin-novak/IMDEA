#include <Audio.h>

// GUItool: begin automatically generated code
AudioInputUSB            usb1;           //xy=111,174
AudioAmplifier           amp1;           //xy=311,96
AudioAmplifier           amp2;           //xy=332,249
AudioFilterBiquad        biquad1;        //xy=454,98
AudioFilterBiquad        biquad2;        //xy=460,248
AudioOutputI2S           i2s1;           //xy=651,169
AudioConnection          patchCord1(usb1, 0, amp1, 0);
AudioConnection          patchCord2(usb1, 1, amp2, 0);
AudioConnection          patchCord3(amp1, biquad1);
AudioConnection          patchCord4(amp2, biquad2);
AudioConnection          patchCord5(biquad1, 0, i2s1, 0);
AudioConnection          patchCord6(biquad2, 0, i2s1, 1);
AudioControlSGTL5000     sgtl5000_1;     //xy=135,341
// GUItool: end automatically generated code

float f = 200;
float Q = 0.707;

void setup() {
  AudioMemory(12);

  sgtl5000_1.enable();  // Enable the audio shield
  sgtl5000_1.volume(0.5);

  // filter design
  biquad1.setLowpass(0, f, Q);
  biquad2.setLowpass(0, f, Q);

  Serial.begin(9600);
  while (Serial.available() != 0) {}

}


void loop() {
  float volume = usb1.volume();
  amp1.gain(volume);
  amp2.gain(volume);


  if (Serial.available() > 0) {
    // Read the incoming data as a string
    String inputString = Serial.readStringUntil('\n');

    // Find the delimiter position (space in this case)
    int spaceIndex = inputString.indexOf('=');

    // Extract the variable name and its value from the input string
    String varName = inputString.substring(0, spaceIndex);
    float value = inputString.substring(spaceIndex + 1).toFloat();

    // Update the appropriate variable based on the name
    if (varName == "f") {
      Serial.print("New frequency: ");
      Serial.println(value);
      f = value;
    } else if (varName == "Q") {
      Serial.print("New Q factor: ");
      Serial.println(value);
      Q = value;
    } else {
      Serial.println("Invalid variable name");
    }

    // update filter
    biquad1.setLowpass(0, f, Q);
    biquad2.setLowpass(0, f, Q);    
  }
}


