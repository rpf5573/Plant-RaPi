# -*- coding: utf-8 -*-
import os

print "라즈베리파이 센서&카메라 테스트를 시작합니다."
os.system("python ../sensor/all_upload.py")
os.system("python ../camera/timelapse.py")