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
import threading
import spidev
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


class Sensor:
  def __init__(self, server_url):

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

    # SPI를 사용해서 ADC로부터 PH측정값을 읽어오기위한 설정
    SPI_PORT = 0
    SPI_DEVICE = 0
    self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
    self.sampling_length = 20
    self.sampling_interval = 50

  def sense_dht(self):
    h,t = dht.read_retry(dht.DHT22, 4)
    return {'humidity' : h, 'temperature' : t}

  def sense_light(self):
    data = self.bus.read_i2c_block_data(0x39, 0x0c | 0x80, 2)
    data1 = self.bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)
    ch0 = data[1] * 256 + data[0]
    ch1 = data[1] * 256 + data1[1]
    return ch0

  def sense_ph(self):
    sum = 0
    count = 0
    for i in range(0, self.sampling_length):
      reading = self.mcp.read_adc(0)
      voltage = reading*5.0 / 1024
      phValue = 3.3*voltage
      sum += phValue
      time.sleep(self.sampling_interval)

    return sum/self.sampling_length

  def get_time(self):
    now = datetime.datetime.now()
    record_time = now.strftime('%Y-%m-%d %H:%M:%S')
    return record_time
  
  def current_milli_time():
    return int(round(time.time() * 1000))

  def send_to_server(self, records):
    r = requests.post(self.server_url, data={'insert': True, 'records': json.dumps(records)})
    print r.text
    response = r.json()
    if response['response_code'] == 201:
      print response['success_message']
    else:
      print response['error_message']
      sys.exit()

  def start(self):
    try:
      record_time = self.get_time()
      t_h = self.sense_dht()
      # 서버에 전달할 센서값들을 한데 모은다
      records = {
        'temperature': format(t_h['temperature'], '.2f'),
        'humidity': format(t_h['humidity'], '.2f'),
        'light': self.sense_light(),
        'ph': self.sense_ph(),
        'time': record_time
      }
      print records
      self.send_to_server(records)
      threading.Timer( 3600, self.start ).start()
    except KeyboardInterrupt, SystemExit:
      print '\n timelapse capture cancelled'
      sys.exit()