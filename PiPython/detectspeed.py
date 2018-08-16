import time
import datetime
import RPi.GPIO as GPIO

def calculateSpeed():
  global start
  done = time.time()
  elapsed = done - start
  elaspesedMinute = elapsed*0.01666668
  rpm = 1/elaspesedMinute
  distance = rpm* 22
  speed = distance/1
  speedKms = speed*.0006
  print(speedKms)
  start = done

def detectSensor(channel):
  # Called if sensor output changes
  timestamp = time.time()
  stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
  if not GPIO.input(channel):
    calculateSpeed()

def main():
  detectSensor(14)

  try:
    # Loop until users quits with CTRL-C
    while True :
      time.sleep(0.1)

  except KeyboardInterrupt:
    # Reset GPIO settings
    GPIO.cleanup()

GPIO.setmode(GPIO.BCM)

print("Setup GPIO pin as input on GPIO14")


GPIO.setup(14 , GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(14, GPIO.BOTH, callback=detectSensor, bouncetime=200)
start = time.time()

if __name__=="__main__":
   main()
