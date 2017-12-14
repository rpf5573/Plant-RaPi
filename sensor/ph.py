# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import os
import time
import Adafruit_ADS1x15 as ADS
adc = ADS.ADS1115(address=0x48, busnum=1)
GAIN = 1

url = 'http://deepmind.dothome.co.kr/controller.php'
GPIO.setmode(GPIO.BCM)

# 평균값을 내기 위해서 저장할 값이 담길 박스를 만듭니다
phArray = []

while True:
  # 센서로부터 값을 가져옵니다
  adc0 = adc.read_adc(0, gain=GAIN)

  #가져온 값 변환
  voltage = (adc0 * 6.144) / 32767
  print voltage
  phValue = 3.5 * voltage
  print phValue

  # 변환된 값을 저장
  phArray.append(voltage)

  # data가 100개 쌓이면
  if len(phArray) == 100:
    sum = 0

    # 평균을 냅니다
    for i in range(len(phArray)):
      sum += phArray[i]
    print "ph Array SUM --> " + str(sum/len(phArray))
    
    # 다시 비웁니다
    phArray = []

time.sleep(1)
