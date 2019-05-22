# -*- encoding: utf-8 -*-
import snowboydecoder as sdecoder
import signal
import led_test as leds
import time
import sys
from textToSpeech import answer
from weatherforecast import todayInfo  
import speech_listening
import os


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
            ['끝', '끝내자', '종료'],
            ['안녕', '안녕하세요', '하이'],
            ['날씨', '오늘 날씨'],
            ['미세먼지', '먼지', '미세먼지 알려줘'],
            ['내일 날씨', '내일 날씨 알려줘']
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
            #print(your_command)
            
            #날씨 정보 찾는다.
            # today_weather_info : 오늘 날씨 정보
            # tomorrow_weather_info : 내일 날씨 정보
            # today_dust_info : 오늘 미세먼지 정보
            today_weahter_info, tomorrow_weather_info, today_dust_info = todayInfo()
            
            #3. check cmdLists
            #초기화. your_command가 cmdLists에 존재하지 않음을 의미함.
            check=-1 
            #your_command가 cmdLists에 있는지 확인한다.
            for cmd in cmdLists:
                if your_command in cmd: #cmd에 명령이 존재한다면
                    check=cmdLists.index(cmd) #cmd의 index추출
                    break #빠져나온다
             
            #명령어가 cmdList에 존재하지 않음.
            if check==-1:
                # led상태 : speak
                leds.pixels.speak()
                time.sleep(0.1)
                answer('죄송합니다. 다시 명령해주세요.')
                
            
            else: #명령어가 존재한다.
                if check==0: #명령어: 종료 -> 반응: led off & 띵소리만 낸다.
                    # led 상태: 불끈다.
                    os.system('aplay terminated.wav')
                    leds.pixels.off()             

                elif check==1: #명령어: 인사 -> 반응: 인사
                    leds.pixels.speak()
                    answer('안녕하세요?')
                
                elif check==2: #명령어: 오늘날씨
                    leds.pixels.speak()
                    answer(today_weahter_info)
                
                elif check==3: #명령어: 오늘 미세먼지
                    leds.pixels.speak()
                    answer(today_dust_info)
                
                elif check==4: #명령어: 내일 날씨
                    leds.pixels.speak()
                    answer(tomorrow_weather_info)
                    
            leds.pixels.off()
            time.sleep(0.1)
        except KeyboardInterrupt: #detected signals
            break
    leds.pixels.off()
    time.sleep(1)
    sys.exit(1)
        

if __name__=='__main__':
    main()
