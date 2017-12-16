# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import os
import time
import datetime
import smbus
import random
import requests
import json
import Adafruit_DHT as dht

# GPIO는 두가지 버전으로 설정 가능합니다. 그 중, 기능별로 포트 번호를 구분해 놓은 BCM을 사용합니다.
GPIO.setmode(GPIO.BCM)

# i2C 버스를 가져옵니다. 최신버전이라서 1을 입력. 구버전은 0.
bus = smbus.SMBus(1)

# TSL2561 address, 0x39(57)
# Select `control register`, 0x00(00) with command register, 0x80(128)
# Power ON mode => 0x03(03)
bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)

# TSL2561 address, 0x39(57)
# Select `timing register`, 0x01(01) with command register, 0x80(128)
# Norminal integration time = 402ms 0x02(02)
bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)

# 데이타가 도착할 서버 url 설정
url = 'http://deepmind.dothome.co.kr/controller.php'

while True:
    now = datetime.datetime.now()
    record_time = now.strftime('%Y-%m-%d %H:%M:%S')
    h,t = dht.read_retry(dht.DHT22, 4)
    print 'Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(t,h)

    data = bus.read_i2c_block_data(0x39, 0x0c | 0x80, 2)
    data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)
    ch0 = data[1] * 256 + data[0]
    ch1 = data[1] * 256 + data1[1]
    print "Full Spectrum(IR + Visible) : %d lux" %ch0

    # 임시로 랜덤값을 지정해 놓는다
    ph = random.randint(5,15)

    # 서버에 전달할 센서값들을 한데 모은다
    records = {
      'temperature': format(t, '.2f'),
      'humidity': format(h, '.2f'),
      'light': ch0,
      'ph': ph,
      'time': record_time
    }

    print records

    # 서버에 센서값 전달
    r = requests.post(url, data={'insert': True, 'records': json.dumps(records)})

    print r.text

    # 서버의 응답을 가져옴
    response = r.json()
    if response['response_code'] == 201:
      print response['success_message']
    else:
      print response['error_message']
    
    # 1초 대기
    time.sleep(3600)
