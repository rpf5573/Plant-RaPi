import RPi.GPIO as GPIO
import os
import time
import Adafruit_DHT as dht

# GPIO는 두가지 버전으로 설정 가능합니다. 그 중, 기능별로 포트 번호를 구분해 놓은 BCM을 사용합니다.
GPIO.setmode(GPIO.BCM)

while True:
    h,t = dht.read_retry(dht.DHT22, 4)
    print 'Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(t,h)
    time.sleep(1)