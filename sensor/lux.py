# -*- coding: utf-8 -*-

import smbus
import time

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

while True:
    time.sleep(1)
    data = bus.read_i2c_block_data(0x39, 0x0c | 0x80, 2)
    data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)
    ch0 = data[1] * 256 + data[0]
    ch1 = data[1] * 256 + data1[1]
    print "Full Spectrum(IR + Visible) : %d lux" %ch0
    