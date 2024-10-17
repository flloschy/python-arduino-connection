#include "U8glib.h"
U8GLIB_SH1106_128X64 oled(12, 11, 8, 9, 10);

// about the maximum amount of pixels available in memory
const int MOSTPOSSIBLEPIXELS = 128 * 64 / 2.118 - 180;

// 2d array to temporarly store pixel positions
//   and the current position/length of resived pixels
//   to sort of emulate dynamic memory allocation
int currentPixelIndex = 0;
byte pixel[MOSTPOSSIBLEPIXELS][2];

String slice; // reserve space for a horizontal slice of the image

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  oled.begin();
  oled.setRot180();
  
  // give 5 seconds time in order to start the python script
  delay(5000);

  // inform the python script that the arduino is ready
  Serial.println("online");
}


void loop() {

  // 128 vertical slices of the screen
  for (int x = 0; x < 128; x++) {
    // tell the python script to send a new slice
    Serial.println("next line");
    delay(10); // 10 ms seams to be the stable minimum
    // get the new pixel data ("0010100100001...")
    slice = Serial.readString();
    // for every character (vertical slice)
    for (int y = 0; y < 64; y++) {
      // check for active pixel
      if (slice.charAt(y) == '1') {
        // and save it
        pixel[currentPixelIndex][0] = x;
        pixel[currentPixelIndex][1] = y;
        currentPixelIndex++;
      }
    }
  }

  oled.firstPage();
  do {
    // render every active pixel
    for (int i = 0; i < currentPixelIndex; i++) {
      oled.drawPixel(pixel[i][0], pixel[i][1]);
    }
  } while (oled.nextPage());

  // reset the pixel amount (dynamic memory)
  currentPixelIndex = 0;
}
