# -*- encoding: utf-8 -*-
import snowboydecoder as sdecoder
import signal
import led_test as leds
import time
import sys
from textToSpeech import answer
from weatherforecast import parsing_weather_info,today_weather_status, today_weather_dust, tomorrow_weather_status 
import speech_listening
import os
import RPi.GPIO as GPIO

FAN_CHANNEL=12
LIGHT_CHANNEL=13

def turn_on(channel):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.OUT)
    GPIO.output(channel, GPIO.LOW)
    

def turn_off(channel):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.OUT)
    GPIO.output(channel, GPIO.HIGH)

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
            ['끝', '끝내자', '종료'],#0
            ['안녕', '안녕하세요', '하이'],#1
            ['날씨', '오늘 날씨', '오늘날씨 알려줘', '오늘 날씨 알려 줘'],#2
            ['미세먼지', '먼지', '미세먼지 알려 줘'],#3
            ['내일 날씨', '내일 날씨 알려줘'],#4
            ['불 켜','불켜줘', '불 켜 줘', '스탠드 켜 줘', '스탠드', '불','조명', '조명 켜줘', '불 켜주세요', '불켜주세요' ], #only light on
            ['불 꺼','불 꺼줘' '불 꺼 줘','불 꺼 줘','스탠드 꺼 줘', '조명 꺼줘', '불 꺼주세요', '불꺼주세요','불꺼줄래','불끌래','불끌게'], # only light off
            ['선풍기 켜줘', '더워', '덥다', '개더워', '너무 더워' ,'선풍기', '바람', '선풍기 바람', '선풍기바람', '선풍기 켜', '선풍기켜줘', '선풍기켜'], # only fan on
            ['선풍기 꺼줘','추워','춥다','개추워','너무 추워', '선풍기 꺼주세요', '선풍기 끌래', '선풍기 그만'], # only fan off
            ['기상 모드', '다 켜 줘','켜 줘', '켜 줘','둘다 켜줘','모두 켜줘','모두다 켜줘', '기상'], # fan and light on
            ['취침 모드', '다 꺼 줘','꺼 줘','둘다 꺼줘','모두 꺼줘','모두다 꺼줘', '취침']  # fan and light off
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
                    turn_off(12)
                    turn_off(13)
                    sdecoder.play_audio_file()
                    #os.system('aplay terminated.wav')
                    leds.pixels.off()             

                elif check==1: #명령어: 인사 -> 반응: 인사
                    leds.pixels.speak()
                    answer('안녕하세요?')
                
                elif check==2: #명령어: 오늘날씨
                    leds.pixels.speak()
                    answer(today_weather_status())
                
                elif check==3: #명령어: 오늘 미세먼지
                    leds.pixels.speak()
                    answer(today_weather_dust())
                
                elif check==4: #명령어: 내일 날씨
                    leds.pixels.speak()
                    answer(tomorrow_weather_status())

                elif check==5:  # 조명on
                    turn_on(13)
                    time.sleep(1)
                    
                elif check==6:  # 조명off
                    turn_off(13)
                    time.sleep(1)
                    
                elif check==7:  # 선풍기on
                    turn_on(12)
                    time.sleep(1)
                    
                elif check==8:  # 선풍기off
                    turn_off(12)
                    time.sleep(1)
                    
                elif check==9:  # 조명&선풍기on
                    turn_on(13)
                    time.sleep(1)
                    turn_on(12)
                    time.sleep(1)
                    
                else:#check==10 조명&선풍기off
                    turn_off(13)
                    time.sleep(1)
                    turn_off(12)
                    time.sleep(1)
                   
            leds.pixels.off()
            time.sleep(0.1)
        except KeyboardInterrupt: #detected signals
            GPIO.cleanup()
            break
    
    leds.pixels.off()
    time.sleep(1)
    sys.exit(1)

if __name__=='__main__':
    main()
