/* Audio Processor for Teensy
 * Copyright (c) 2022, Antonin Novak, antonin.novak(at)univ-lemans.fr
 * 
 * Laboratoire d'Acoustique de l'Université du Mans (LAUM), 
 * UMR 6613, Institut d'Acoustique - Graduate School (IA-GS), 
 * CNRS, Le Mans Université, France 
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice, development funding notice, and this permission
 * notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */


#ifndef audio_processor_h_
#define audio_processor_h_
#include "Arduino.h"
#include "AudioStream.h"

class AudioProcessor : public AudioStream
{
public:
  AudioProcessor(void) : AudioStream(2, inputQueueArray) {  
    changeParameters();
  }
  virtual void update(void);
  
  void changeFrequency(float _f);
  void changeQ(float _Q);
  void changeParameters();

  const int resolutionDAC = 16;
  const int resolutionADC = 16;
  const float conversionConstADC = 1.0f/((1<<resolutionADC)-1);
  const float conversionConstDAC = (1<<resolutionDAC)-1;

  const float fs = 48000.0;
  float f = 1000.0;
  float Q = 0.7;
  float alpha, wc;

  float b0, b1, b2, a1, a2;
  float dL0 = 0.0, dL1 = 0.0, dL2 = 0.0, dL3 = 0.0;
  float dR0 = 0.0, dR1 = 0.0, dR2 = 0.0, dR3 = 0.0;

private:
  audio_block_t *inputQueueArray[2];
};

#endif
