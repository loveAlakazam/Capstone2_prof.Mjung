import pixels as leds
import time
import sys
def main():
  while True:
    try:
      print('hello')
      leds.pixels.wakeup()
      time.sleep(3)
      
      print('speaking')
      leds.pixels.speak()
      time.sleep(3)
      
      print('led off')
      leds.pixels.off()
      time.sleep(3)
  
    except: KeyboardInterrupt: #detected signals
      break
     
  leds.pixels.off()
  time.sleep(1)
  sys.exit(1)


if '__name__'=='__main__':
  main()
