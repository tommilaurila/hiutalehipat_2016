import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)

GPIO.output(17, GPIO.HIGH) #enable
GPIO.output(27, GPIO.HIGH) #in 1
GPIO.output(22, GPIO.LOW)  #in 2

GPIO.output(17, GPIO.LOW) #enable
GPIO.output(27, GPIO.LOW) #in 1
GPIO.output(22, GPIO.LOW)  #in 2
