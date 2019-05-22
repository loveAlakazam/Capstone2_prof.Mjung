import RPi.GPIO as GPIO
import time

channel=23

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)

def light_on(pin):
	GPIO.output(pin, GPIO.HIGH)

def light_off(pin):
	GPIO.output(pin, GPIO.LOW)

if __name__=='__main__':
	try:
		light_on(channel)
		time.sleep(1)
		light_off(channel)
		time.sleep(1)
		GPIO.cleanup()
	except KeyboardInterrupt:
		GPIO.cleanup()
		pass
