# Arduino image transfer
This project allows for python to render/process/simulate/edit/generate an image, which then gets send through arduino's Serial connection to be able to show the image on an OLED.

# Requirements
1. Python (created on 3.12.7 (others might still work))
2. required pip packages
    1. `pip install -r ./requirements.txt`
3. Arduino Mega 2560 (others might still work)
4. Arduino OLED Display
    1. Needs to be properly connected to the arduino
    2. Needs to work with [U8glib by olver](https://github.com/olikraus/u8glib)
5. Something to upload to arduino (probably arduino IDE)
    1. and said [U8glib by olver](https://github.com/olikraus/u8glib) must be installed

# Run it
1. Copy `base.py`
2. Create some rendering code at line 27
3. Upload the `./arduinocode.ino` to the arduino
4. Wait until uploading is done
5. Run your python file withing ~5 seconds of uploading 
6. Should work :TM:

Once the code is uploaded to arduino, you can also just press the reset button going forwards

##### You can also run the already working `particleLife.py`, which sadly doesnt result in an satisfiying simulation, but is able to generate an image and transfer it to arduino correctly

# How
> *steps marked with [A] run on the Arduino, while [P] run with Python*

1. [P] wait until arduino sends `online` via. Serial
2. [A] send `online` via. Serial
3. [P] run *custom rendering code*
4. [P] send current vertical slice / [A] keep track of current vertical slice index
    1. [P] for every pixel in this slice
        1. [P] append "0" (off) or "1" (on) to a string
    2. [P] wait for arduino to send `next line`
    3. [A] send `next line` via. Serial
    4. [P] send this string over Serial
    5. [A] read Serial line
        1. [A] go over each character
        2. [A] if character is "1"
            1. [A] update x and y coordinates inside the pixel array
    6. [P] increase current slice index
    7. [A/P]repeat `{4.}` until no slices are left
5. [A] render image
    1. [A] loop through every stored pixel
    2. [A] place pixel on stored x,y position
6. [P] go back to `{3.}` / [A] go back to `{4.3.}`