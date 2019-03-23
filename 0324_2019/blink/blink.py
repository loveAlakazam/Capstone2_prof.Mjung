# 교재: 사물인터넷을 품은 라즈베리 파이 -6.2 GPIO 디지털 입출력 제어
import RPi.GPIO as GPIO
import time
import sys
pin_num =2 # raspberry_pi_pins_info 사진 참고
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_num, GPIO.OUT)
while True:
  try:
    GPIO.output(pin_num, 1) #turn on
    #print('turn on')
    time.sleep(1)
    
    GPIO.output(pin_num, 0) #turn off
    #print('turn off')
    time.sleep(1)
  except KeyboardInterrupt:
    break
GPIO.output(pin_num, 0)
sys.exit(1)
