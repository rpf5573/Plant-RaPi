# -*- coding: utf-8 -*-
import os

print "라즈베리파이 센서&카메라 테스트를 시작합니다."
# 끝에 &를 붙여주면, 백그라운드에서 진행됩니다~
os.system("python ../sensor/all_upload.py &") 
os.system("python ../camera/timelapse.py &")