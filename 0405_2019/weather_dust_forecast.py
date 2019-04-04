# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 18:34:35 2019
@author: lovesAlakazam
"""
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

def todayInfo():
    #가져올 페이지: 네이버 '오늘의 날씨' 검색 결과
    url='https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%98%A4%EB%8A%98%EC%9D%98+%EB%82%A0%EC%94%A8'

    # 현재 url에 해당하는 페이지를 가져온다.
    page = urlopen(Request(url))

    # page를 읽는다.
    html = page.read()

    soup = BeautifulSoup(html, 'html5lib')
    #print(soup) 
    
    ## 오늘 날씨 정보를 알려줌.
    # 현재 위치한 지역
    location=soup.find('span', class_='btn_select').find('em').text
    today_weather_info='오늘 '+ location[:-1]+'의 기온은 '
    
    #기온: 
    temperature=soup.find_all('span', class_='todaytemp')
    temperature=[x.text for x in temperature] #text만을 추출
    #temperatrue=[오늘온도, 내일오전온도, 내일오후온도, 모레오전온도, 모레오후온도]
    
    #오늘 기온 temperature[0]
    today_weather_info+=(temperature[0]+'도이고 ')
    tomorrow_weather_info='내일 오전은 '+temperature[1]+'도이고 오후는 '+temperature[2]+'도 입니다.'
    
    
    #오늘 날씨 상태: weather_info[2]
    cy=soup.find('p',class_='cast_txt').text
    now_status=cy[:cy.find(',')]
    today_weather_info +=(now_status+'입니다. ')
    
    
    #체감온도: weather_info[4]
    cy= soup.find('span',class_='sensible').text
    sensing_temp=cy[ cy.find(' ')+1:cy.find('˚')]
    today_weather_info+=('체감온도는 '+sensing_temp+ '도 입니다.')
    
    ## 미세먼지 상태 정보
    today_dust_info='오늘 '
    cy = soup.find_all('dd', class_='lv2')  #리스트
    c=cy[0].text #미세먼지부분만 
    today_dust_info+=('미세먼지 상태는 '+c[c.find('㎥')+1:]+'입니다.')
    
    return today_weather_info, tomorrow_weather_info, today_dust_info
   

if __name__=='__main__':
    today_temp, tomorrow_temp ,today_dust= todayInfo()
    print('[날씨]\n\t{}\n[미세먼지&오존]\n\t{}'.format(today_temp, today_dust))
    print(tomorrow_temp)
   
