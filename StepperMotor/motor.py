import math
import ctypes
import RPi.GPIO as GPIO

libc = ctypes.CDLL("libc.so.6")
GPIO.setmode(GPIO.BCM)
class Motor_28byj48:
    stride_angle = 5.625 # in degree
    gear_ratios = 63.68395 # or 64
    step_pattern = [
        [1,0,0,0], # pattern 0
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1]  # pattern 7
    ]
    delay=900 # in us

    def __init__(self, r, step_length, pins):
        self.stride_length = 2*math.pi*r*self.stride_angle/360/self.gear_ratios
        self.step_length = step_length
        self.pins = pins
        self.steps_now = -1
        GPIO.setwarnings(False)
        for i in pins:
            GPIO.setup(i, GPIO.OUT)

        print("A motor class is created. Please initialize it.")

    def initialize(self, init_thread_length):
        self.steps_now = int(init_thread_length / (self.step_length * self.stride_length))
        self.steps_now -= self.steps_now%8
        print("The motor has been initialized.")

    def rotate(self, steps):
        if steps > 0:
            clockwise=-1
        elif steps<0:
            clockwise=1
        else:
            return

        if self.steps_now==-1:
            #if clockwise, then pattern start from 1 to 7 to 0
            #else then pattern start from 7 to 0
            start = int(4-clockwise*3)
            stop = int(4+clockwise*5)
            for i in range(abs(steps)):
                for j in range(start, stop, clockwise):
                    for k in range(4):
                        GPIO.output(self.pins[k], self.step_pattern[j%8][k])
                    libc.usleep(self.delay)
        else:
            for i in range(abs(steps)):
                self.steps_now-=clockwise
                for k in range(4):
                    GPIO.output(self.pins[k], self.step_pattern[self.steps_now%8][k])
                libc.usleep(self.delay)
                
        for k in range(4):
            GPIO.output(self.pins[k], 0)

    def move(self, thread_length):
        steps_next = int(thread_length/(self.step_length*self.stride_length))
        steps = steps_next - self.steps_now
        print("move to", steps_next, "from", self.steps_now)
        self.rotate(steps)
        
def test():
    motor_a = Motor_28byj48(r=3, step_length=1, pins=[4,17,23,24])
    #motor_a.rotate(1)
    motor_a.initialize(100)
    motor_a.move(100.5)
    libc.usleep(400000)
    motor_a.move(100)
    
if __name__ == "__main__":
    test()