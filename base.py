import serial, time
from PIL import Image
from alive_progress import alive_bar

# simulate means that no data gets send, but
#    the code still creates an image.
#    Usefull for debugging
SIMULATE = True
if not SIMULATE:
    arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1) 

# helper function to wait until a certain string is recived
def waitFor(goal=""):
    # readline returns bytes, so convert the goal string to bytes also
    goal = bytes(f"{goal}\r\n", "UTF-8")
    line = arduino.readline()
    while line != goal:
        line = arduino.readline()

def draw():
    # The pixel data to be drawn on the OLED
    bitmap = Image.new(mode="1", size=(SIMWIDTH, SIMHEIGHT))
    # The pixel data to be saved to a file
    frame = Image.new(mode="RGB", size=(SIMWIDTH, SIMHEIGHT))

    #################################################
    # TODO: DRAW STUFF HERE TO THE BITMAP AND FRAME #
    #################################################
    
    if not SIMULATE:
        with alive_bar(SIMWIDTH) as bar:
            # for every horizontal slice
            for x in range(SIMWIDTH):
                # create a vertical slice out of "1" and "0"
                mp = ""
                for y in range(SIMHEIGHT):
                    # YES string is less efficient than bytes
                    mp += str(bitmap.getpixel((x, y)))
                waitFor("next line")
                # once arduino is ready, send vertical slice
                arduino.write(bytes(mp, "UTF-8"))
                bar() # update progress bar
    frame.save("./frame.png")

if not SIMULATE:
    while True:
        print("waiting for arduino....")
        waitFor("online")
        print("arduino is online")
        while arduino.isOpen():
            draw()
        print("serial was closed")
else:
    while True:
        draw()
        time.sleep(0.4)