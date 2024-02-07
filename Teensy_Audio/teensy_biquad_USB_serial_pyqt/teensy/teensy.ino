#include <Audio.h>
#include <ArduinoJson.h>

// Audio Adaptor Board
AudioControlSGTL5000     sgtl5000_1;

// Define audio input and output objects
AudioInputUSB            usb1;
AudioOutputI2S           i2s1;

// Define amplifiers to adjust the USB volume
AudioAmplifier           amp1;
AudioAmplifier           amp2;

// Define audio filter objects
AudioFilterBiquad        biquad1; // Filter for left channel
AudioFilterBiquad        biquad2; // Filter for right channel

// Connections
AudioConnection          patchCord1(usb1, 0, amp1, 0);
AudioConnection          patchCord2(usb1, 1, amp2, 0);
AudioConnection          patchCord4(amp1, biquad1);
AudioConnection          patchCord3(amp2, biquad2);
AudioConnection          patchCord5(biquad1, 0, i2s1, 0);
AudioConnection          patchCord6(biquad2, 0, i2s1, 1);


double coeffs[5]; // IIR Filter coefficients

// Setup function for initial configurations
void setup() {

  // reset filters coefficients to baypass [1.0, 0.0, 0.0, 0.0, 0.0]
  for (int i=0; i<5; i++){
    coeffs[i] = 0.0;
  }
  coeffs[0] = 1.0;

  // Initialize the Audio Adaptor Board
  sgtl5000_1.enable();
  sgtl5000_1.volume(0.5);

  // Initialize serial communication
  Serial.begin(9600);
  while (Serial.available() != 0) {}

  // Initialize audio library
  AudioMemory(12);

  // Set filter coefficients
  updateCoefficients();
}


// Loop function runs repeatedly to handle real-time audio processing
void loop() {
  
  // Set the USB volume
  float vol = usb1.volume();  // read USB volume setting
  amp1.gain(vol);             // set gain according to USB volume
  amp2.gain(vol);


  // Check if new filter coefficients are available from serial
  // If so, update the filter coefficients for left and right channels
  if (Serial.available() > 0) {
    
    // Read the incoming data as a string
    String jsonData = Serial.readStringUntil('\n');
    Serial.println(jsonData);

    // Convert the JSON string with filter coefficients to 'doc' variable
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, jsonData);
    if (error) {
        Serial.print("deserializeJson() failed: ");
        Serial.println(error.c_str());
        return;
    }

    // Parse the JSON array
    JsonArray arr = doc.as<JsonArray>();
    for (unsigned int i = 0; i < arr.size(); i++) {
        coeffs[i] = arr[i];
    }        
    Serial.println("Array received.");

    // Optionally, print the received array for debugging
    for (double value : coeffs) {
        Serial.println(value);
    }

    // Set new filter coefficients
    updateCoefficients();

  }

  // Add delay for stability
  delay(100);
}


void updateCoefficients(){
  // Audio processing is handled automatically by the Teensy audio library  
  biquad1.setCoefficients(0, coeffs); // update left channel coefficients
  biquad2.setCoefficients(0, coeffs); // update right channel coefficients
}