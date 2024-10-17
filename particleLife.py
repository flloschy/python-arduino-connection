import serial, random, math, time, colour
from PIL import Image
from alive_progress import alive_bar


SIMULATE = False

STARTCOLOR = colour.Color("red")
ENDCOLOR = colour.Color("blue")
COLORS = 2
COLORSLIST = list(STARTCOLOR.range_to(ENDCOLOR, COLORS+1))
PARTICLES = 150
SIMWIDTH = 128
SIMHEIGHT = 64
RANGE = 2
STRENGTH = 60
HARDNESS = 5


colortable = [[(random.random() * 10 - 5) for _ in range(COLORS)] for _ in range(COLORS)]
arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1) 


def waitFor(goal=""):
    goal = bytes(f"{goal}\r\n", "UTF-8")
    line = arduino.readline()
    # print(f"{line=} {goal=}")
    while line != goal:
        line = arduino.readline()
        # print(f"{line=} {goal=}")

class Particle:
    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.c = c
        self.vx = 0
        self.vy = 0
    def physic(self, parB):
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)
        return

        if (parB == self): return

        dx = parB.x - self.x
        dy = parB.y - self.y

        if (dx > SIMWIDTH / 2): dx -= SIMWIDTH
        if (dx < SIMWIDTH / 2): dx += SIMWIDTH
        if (dy > SIMHEIGHT / 2): dy -= SIMHEIGHT
        if (dy < SIMHEIGHT / 2): dy += SIMHEIGHT

        d = math.sqrt(dx ** 2 + dy ** 2)
        if (d > RANGE): return

        factor = colortable[self.c][parB.c]
        force = self.f(d, factor)

        self.vx += dx * 0.0000001 * force * 0.000000000000001
        self.vy += dy * 0.0000001 * force * 0.000000000000001

    def updatePos(self):
        self.x = self.mod(SIMWIDTH, self.x, self.vx)
        self.y = self.mod(SIMHEIGHT, self.y, self.vy)
        self.vx = 0 
        self.vy = 0

    def mod(self, base, value, addition):
        n = (value + addition) % base
        if (n < 0): return base + n
        return n
    
    def f(self, distance, force):
        if (distance > RANGE): return 0
        if (distance < RANGE * 0.126): return ((8 * distance) / RANGE - 1) * (STRENGTH * HARDNESS)
        return ((-16 * force * abs(distance - (9 / 16) * RANGE)) / (7 * RANGE) + force) * STRENGTH


particles = [Particle(random.randint(0, SIMWIDTH), random.randint(0, SIMHEIGHT), random.randint(0, COLORS)) for _ in range(PARTICLES)]


def draw():
    bitmap = Image.new(mode="1", size=(SIMWIDTH, SIMHEIGHT))
    frame = Image.new(mode="RGB", size=(SIMWIDTH, SIMHEIGHT))
    for i, par in enumerate(particles):
        bitmap.putpixel((par.x, par.y), 1)
        frame.putpixel((par.x, par.y), (int(255 * COLORSLIST[par.c].get_red()), int(255 * COLORSLIST[par.c].get_green()), int(255 * COLORSLIST[par.c].get_blue())))

    if not SIMULATE:
        with alive_bar(SIMWIDTH) as bar:
            for x in range(SIMWIDTH):
                mp = ""
                for y in range(SIMHEIGHT):
                    mp += str(bitmap.getpixel((x, y)))
                waitFor("next line")
                arduino.write(bytes(mp, "UTF-8"))
                bar()
    frame.save("./frame.png")
def physics():
    for a in particles:
        for b in particles:
            a.physic(b)
        a.updatePos()


if not SIMULATE:
    while True:
        print("waiting for arduino....")
        waitFor("online")
        print("arduino is online")
        while arduino.isOpen():
            physics()
            draw()
        print("serial was closed")
else:
    while True:
        physics()
        draw()
        time.sleep(0.4)