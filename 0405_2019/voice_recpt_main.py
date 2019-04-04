# -*- encoding: utf-8 -*-
import snowboydecoder as sdecoder
import signal
import led_test as leds
import time
import sys
import textToSpeech
import weatherforecast
import speech_listening


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
#simple mode(end/ saying hello / question weather)
cmdLists=[
    [u'끝',0], #ending
    [u'안녕',1], #saying hello
    [u'오늘 날씨',2], #question weather-today
    [u'미세 먼지',3], #question dust-today
    [u'미세먼지',3],
    [u'내일 날씨',4] #question weather-tomorrow
]

''' 
cmdLists=[
        [u'',0],    # ending code:0
        [u'',0],    #
        [u'',1],    # say hello code:1
        [u'',1],    #
        [u'',2],    # weather info code:2
        [u'',2],    # weather info code:2
        [u'',3],    # lamp on code :3
        [u'',3],    #
        [u'',4],    # lamp off code:4
        [u'',4],    #
        [u'',5],    # fan on code:5
        [u'',5],    #
        [u'',6],    # fan off code:6
        [u'',6]     #
]

'''
def main():
    while True:
        try:
            #1. key-word detection
            detector=sdecoder.HotwordDetector(model,sensitivity=0.6)
            print('Listening ... press Ctrl+c to exit..')
            detector.start(detected_callback=sdecoder.play_audio_file,
                           interrupt_check=interrupt_callback,
                           sleep_time=0.03)

            # if keyword detected keyword => using Speeh API
            # google Speech transcribe mic...
            # maximum listening time: about 65[s]
            #2. listening user's command
            leds.pixels.think()
            your_command=speech_listening.main()
            print(your_command)

            #3. check cmd Lists

            #4. answering command
            
            #5. ending command
            
            # if speech transcribe user's commands..
            #print('hello')
            #leds.pixels.listen()
            #time.sleep(0.5)
            #print('\n\n\ndetected\n\n\n')
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
