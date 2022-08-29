# all the wiring here is pretty self explanatory, just look at the GPIO 
# numbers on pin diagrams for the pi to see which numbers match the ones
# here in the code.  The one thing to mention not already made obvious by just
# looking at the numbers in the code here, is that 'echo' on the ultrasonic
# sensor connects via a 1k ohm resistor to GPIO 11-- and that a 2k ohm resistor
# forms an alternate path AFTER the 1k ohm resistor, connecting back to ground
# as an alternative to connecting back up to GPIO 11

#import all of the libraries here 
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

#set mode for GPIO
GPIO.setmode(GPIO.BCM)

# Ultrasonic pin assignments
SR04_trigger_pin = 7
SR04_echo_pin = 11

# Set up the SR04 pins
GPIO.setup(SR04_trigger_pin, GPIO.OUT)
GPIO.setup(SR04_echo_pin, GPIO.IN)
GPIO.output(SR04_trigger_pin, GPIO.LOW)

#create variable for button
button = 19
#setup button as input
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Remember what the button was so we can see if it changed
prevButton = GPIO.input(button)
prevPressTime = time.time()
nextDist = time.time() - 1

def distance(metric):
        # set Trigger to HIGH
        GPIO.output(SR04_trigger_pin, GPIO.HIGH)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(SR04_trigger_pin, GPIO.LOW)

        startTime = time.time()
        stopTime = time.time()

        # Get the returnb pulse start time
        while 0 == GPIO.input(SR04_echo_pin):
                startTime = time.time()

        # Get the pulse length
        while 1 == GPIO.input(SR04_echo_pin):
                stopTime = time.time()

        elapsedTime = stopTime - startTime
        # The speed of sound is 33120 cm/S or 13039.37 inch/sec.
        # Divide by 2 since this is a round trip
        if (1 == metric):
                d = (elapsedTime * 33120.0) / 2   # metric
        else:
                d = (elapsedTime * 13039.37) / 2   # english

        return d

import ultrasonicCleanAndCompileDistArraysTest2a

import statistics
import math

arrCombo=[]

arr2=[]
arr2cleaned=[]
arr2NowMean=0

angleNow=8888
input1angle=0
input1x=8888
input1y=8888
input1xArr=[]
input1yArr=[]
input1xCleanedArr=[]
input1yCleanedArr=[]

xNowMean=0
yNowMean=0

oldInputAngle=8

autoRotationInputMode=True

latestMeasurement=0

setReset=0

#wrap our code in a try block for error handling
try:

  #create variables for LEDs and set them to out
  led = 4
  GPIO.setup(led, GPIO.OUT)
  #create a loop that checks for button input
  while True:
    input_state = GPIO.input(button)
    #if button pressed, light up timed LEDs
    if input_state == False:
      print('Button Pressed')
      print('debug test 1')
      if time.time() > nextDist:
        if angleNow>360:
          print('measuring initial distance values')
        elif angleNow<=360:
          print('with initial distance value calculated, and angle input, rotate body to match starting rotation of 0, to measure x from start')
        latestMeasurement=(distance(False))
        if input1y==9999:
          input1yArr.append(latestMeasurement)
        elif input1x==9999:
          input1xArr.append(latestMeasurement)
        else:
          arr2.append(latestMeasurement)
          
        print("Distance=" + str(latestMeasurement))
        d = int(100 * latestMeasurement) / 100
        m = str(d) + " in."
        print("m=", str(m))
      time.sleep(0.2)
      GPIO.output(led, 1)
      time.sleep(0.5)
    else:
#      print('button NOT pushed')
      if input1y==9999 and len(input1yArr)>0:
        ultrasonicCleanAndCompileDistArraysTest2a.f1arrCleaner(input1yArr,input1yCleanedArr)
        yNowMean=statistics.mean(input1yCleanedArr); print('calculated yNowMean: '+str(yNowMean))
        input1yArr=[]
      elif input1x==9999 and len(input1xArr)>0:
        ultrasonicCleanAndCompileDistArraysTest2a.f1arrCleaner(input1xArr,input1xCleanedArr)
        xNowMean=statistics.mean(input1xCleanedArr); print('calculated xNowMean: '+str(xNowMean))
        input1xArr=[]
      elif len(arr2)>0:
        ultrasonicCleanAndCompileDistArraysTest2a.f1arrCleaner(arr2,arr2cleaned); print('|||---->>> DEBUG TESTING arr2 to arr2cleaned through func in other module <<<----|||')
        arr2NowMean=statistics.mean(arr2cleaned); print('calculated arr2NowMean: '+str(arr2NowMean))
        arr2=[]
        angleNow==9999
        if angleNow==9999:
          ultrasonicCleanAndCompileDistArraysTest2a.f1arrCleaner(arr2,arr2cleaned)
          arr2NowMean=statistics.mean(arr2cleaned)

          input1angle=''
          input1angle=input('enter digit from 1 to 8 representing multiples of 45 degrees to record which direction faced while  measuring or just hit enter to use 360:')
          if input1angle == '':
            if autoRotationInputMode==True:
              print('entering auto-rotation angle +45 degrees')
              if oldInputAngle < 8:
                input1angle=oldInputAngle+1
              else:
                input1angle=1
            elif autoRotationInputMode==False:
              print('entering starting rotation angle of 360 degrees')
              input1angle=int(8)

          if input1angle > 0 and input1angle < 9:
            input1angle=int(input1angle)
            oldInputAngle=input1angle          
            angleNow=(input1angle*45)
            input1angle=0
            print('angle was input CORRECTLY; directional angle of measured distances is: '+str(angleNow))
            print('rotate so that you are facing 180 opposite of starting rotation and then press and hold button to calculate X distance from start location:')

      elif input1y!=8888 and input1x!=8888 and angleNow!=8888:
        arrCombo.append((angleNow, xNowMean, yNowMean, arr2NowMean))

        # ----------------------------------------------------------------------------------------------------
        # place into RESET FUNC- set this reset up as own func for modularity/simplicity if desired:

        arr2cleaned=[]
        arr2NowMean=0

        angleNow=8888
        input1angle=0
        input1x=8888
        input1y=8888
        input1xArr=[]
        input1yArr=[]
        input1xCleanedArr=[]
        input1yCleanedArr=[]

        xNowMean=0
        yNowMean=0

        latestMeasurement=0
        # ----------------------------------------------------------------------------------------------------

        print('---------------------------------------')
        print('---------------------------------------')
        print('updated arrCombo is now: '+ arrCombo)
        print('---------------------------------------')
        print('---------------------------------------')

      # if we have a cleaned measured sonic dist and 
#      if len(arr2cleaned)>0 and angleNow==9999:
        else:
          # ----------------------------------------------------------------------------------------------------
          # place into RESET FUNC- set this reset up as own func for modularity/simplicity if desired:
          setReset=input('input 9999 and then hit enter to delete previous measurements and reset all variables EXCEPT arrCombo: ')
          setReset=int(setReset)
          if setReset==9999:
            print('RESET FUNC: all variables except arrCombo are reset to default starting value')
            arr2cleaned=[]
            arr2NowMean=0

            angleNow=8888
            input1angle=0
            input1x=8888
            input1y=8888
            input1xArr=[]
            input1yArr=[]
            input1xCleanedArr=[]
            input1yCleanedArr=[]

            xNowMean=0
            yNowMean=0

            latestMeasurement=0
          # ----------------------------------------------------------------------------------------------------
          print('previous distance measurements deleted')
#      elif angleNow != 9999:
#        print('rotate body to face perpendicular to starting wall')
#        print('...then press and hold button to ')
      GPIO.output(led, 0)
#      print('debug END of try <======================= ||||||||||||||||||||||||| (fin)')

#execute this code if CTRL + C is used to kill python script
except KeyboardInterrupt:
  print("You've exited the program")
#execute code inside this block as the program exits
finally:
  GPIO.cleanup()

