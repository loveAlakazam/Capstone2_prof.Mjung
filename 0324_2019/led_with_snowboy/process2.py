# process2.py : snowboy(keyword detection) + pixel 3 leds
import snowboydecoder as sdecoder
import signal
import led_test as leds
import time
import sys
interrupted=False

def signal_handler(signal, frame):
    global interrupted
    interrupted=True

def interrupt_callback():
    global interrupted
    return interrupted


if len(sys.argv)==1:
    print("Error: need to specify model name")
    print("Usage: python3 voice_reception_main.py model")
    sys.exit(-1)
    
model = sys.argv[1]

def main():
    while True:
        try:
            # key-word detection
            detector=sdecoder.HotwordDetector(model,sensitivity=0.6)
            print('Listening ... press Ctrl+c to exit..')
            detector.start(detected_callback=sdecoder.play_audio_file,
                           interrupt_check=interrupt_callback,
                           sleep_time=0.03)
                
            #print('hello')
            leds.pixels.listen()
            time.sleep(0.5)
            print('\n\n\ndetected\n\n\n')
            #leds.pixels.speak()
            #time.sleep(3)
            #print('leds off')
            leds.pixels.off()
            time.sleep(0.1)
        except KeyboardInterrupt: #detected signals
            break
    leds.pixels.off()
    time.sleep(1)
    sys.exit(1)
        

if __name__=='__main__':
    main()
