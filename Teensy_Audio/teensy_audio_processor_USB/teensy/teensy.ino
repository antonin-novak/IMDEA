#include <Audio.h>
#include "audio_processor.h"

AudioInputUSB usb1;
AudioAmplifier amp2;
AudioAmplifier amp1;
AudioOutputI2S i2s1;
AudioProcessor proc;
AudioControlSGTL5000     sgtl5000_1;

AudioConnection patchCord1(usb1, 0, amp1, 0);
AudioConnection patchCord2(usb1, 1, amp2, 0);
AudioConnection patchCord4(amp1, 0, proc, 0);
AudioConnection patchCord3(amp2, 0, proc, 1);
AudioConnection patchCord6(proc, 0, i2s1, 0);
AudioConnection patchCord5(proc, 1, i2s1, 1);

void setup() {
  sgtl5000_1.enable();
  sgtl5000_1.volume(0.5);

  Serial.begin(9600);
  while (Serial.available() != 0) {}

  AudioMemory(12);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
}

void loop() {
  float vol = usb1.volume();  // read PC volume setting
  amp1.gain(vol);             // set gain according to PC volume
  amp2.gain(vol);

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
      proc.changeFrequency(value);
    } else if (varName == "Q") {
      Serial.print("New Q factor: ");
      Serial.println(value);
      proc.changeQ(value);
    } else {
      Serial.println("Invalid variable name");
    }
  }
  delay(100);
}