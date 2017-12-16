# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import os
import sys
import time
import datetime
import smbus
import random
import requests
import json
import Adafruit_DHT as dht


class Sensor:
  def __init__(self, server_url):

    server_url = 'http://deepmind.dothome.co.kr/controller.php'

    # GPIO는 두가지 버전으로 설정 가능합니다. 그 중, 기능별로 포트 번호를 구분해 놓은 BCM을 사용합니다.
    GPIO.setmode(GPIO.BCM)

    # 센서값을 저장할 서버 url을 받는다
    self.server_url = server_url

    # i2C 버스를 가져옵니다. 최신버전이라서 1을 입력. 구버전은 0.
    self.bus = smbus.SMBus(1)

    # TSL2561 address, 0x39(57)
    # Select `control register`, 0x00(00) with command register, 0x80(128)
    # Power ON mode => 0x03(03)
    self.bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)

    # TSL2561 address, 0x39(57)
    # Select `timing register`, 0x01(01) with command register, 0x80(128)
    # Norminal integration time = 402ms 0x02(02)
    self.bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)


  def sense_dht():
    h,t = dht.read_retry(dht.DHT22, 4)
    return {'humidity' : h, 'temperature' : t}

  def sense_lux():
    data = self.bus.read_i2c_block_data(0x39, 0x0c | 0x80, 2)
    data1 = self.bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)
    ch0 = data[1] * 256 + data[0]
    ch1 = data[1] * 256 + data1[1]
    return ch0

  def sense_ph():
    size = 100
    sum = 0
    for i in range(0, size):
      ph = random.randint(5,15)
      sum += ph

    return sum/size

  def get_time():
    now = datetime.datetime.now()
    record_time = now.strftime('%Y-%m-%d %H:%M:%S')

  def send_to_sever(records):
    r = requests.post(self.server_url, data={'insert': True, 'records': json.dumps(records)})
    print r.text
    response = r.json()
    if response['response_code'] == 201:
      print response['success_message']
    else:
      print response['error_message']
      sys.exit()