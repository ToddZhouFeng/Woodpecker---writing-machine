import RPi.GPIO as GPIO
import time
def setServoAngle(angle):
   GPIO.setmode(GPIO.BCM)
   GPIO.setwarnings(False)
   GPIO.setup(17, GPIO.OUT)
   tilt = GPIO.PWM(17, 50)
   tilt.start(0)
   DutyCycle = angle/18 + 2
   tilt.ChangeDutyCycle(DutyCycle)
   time.sleep(0.1)
   tilt.stop()
c = input("If you want to continue, type 'c' please. Type 'e' to end.")
while c == 'c':
   angle = input('Please type an angle:')  # input输入的是字符串，需要用int（）函数转化成数字。
   angle = int(angle)
   setServoAngle(angle)
   c = input("'c' or 'e'?") 
GPIO.cleanup()
exit()
