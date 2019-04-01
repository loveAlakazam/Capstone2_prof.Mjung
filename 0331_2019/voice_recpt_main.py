import snowboydecoder as sdecoder
import signal
import led_test as leds
import time
import sys

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

'''
실제로 실행했을 때 아래의 명령어가 어떤 형식으로 출력되는지 확인할 것.
'''
cmdLists=[
        # ending code:0
        [u'끝내자',0],    
        [u'끝',0],
        
        # say hello code:1
        [u'안녕',1],    
        [u'안녕하세요',1],
        
        # weather info code:2
        [u'날씨',2],
        [u'날씨 어때',2],    
        [u'날씨 알려줘',2],    
        [u'오늘 날씨 어때',2],
        [u'오늘 날씨',2],
        
        # lamp on code :3
        [u'불',3],
        [u'스탠드',3],
        [u'불 켜',3],
        [u'불 켜 줘',3],
        [u'불 켜 주세요',3],
        [u'불 켜 줄래',3],
        [u'스탠드 켜줘',3],
        [u'스탠드 킬래',3],
        
        # lamp off code:4
        [u'불 꺼',4],    
        [u'불 꺼 줘',4],
        [u'불 꺼 주세요',4],
        [u'불 끌 래',4],
        [u'스탠드 꺼 줘',4],
        [u'스탠드 끌 래',4]
        
        # fan on code:5
        [u'선풍기 켜',5],
        [u'선풍기 켜 줘',5],
        [u'선풍기 켜 주세요',5],
        [u'선풍기 킬래',5],
        [u'선풍기 켜줄래',5],
        [u'선풍기',5],     
        [u'더워',5],
        [u'아 더워',5],
        [u'덥다',5],
        
        # fan off code:6
        [u'선풍기 꺼',6],
        [u'선풍기 꺼 줘',6],
        [u'선풍기 꺼 주세요',6],
        [u'선풍기 끌래',6],
        [u'추워',6],
        [u'춥다',6],
        [u'너무 추워',6],
        
        # fan/lamp on code: 7
        [u'선풍기 스탠드',7],
        [u'스탠드 선풍기',7],
        [u'켜',7],
        [u'켜줘',7],
        [u'다 켜',7],
        [u'다 켜줘',7],
        [u'싹 다',7],
        [u'다',7],
        
        # fan/lamp off code: 8
        [u'다 꺼줘',8],
        [u'꺼',8],
        [u'다 꺼',8],
        [u'꺼줘',8],
        [u'나 잘래',8],
        [u'졸려',8],
        [u'잘래',8]
]



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
