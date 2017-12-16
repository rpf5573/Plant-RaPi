# -*- coding: utf-8 -*-
import os
import sys
from sensor import Sensor
from camera.timelapse import Timelapse
import yaml
from multiprocessing import Process, Queue
import time

print "라즈베리파이 센서&카메라 테스트를 시작합니다."
# 끝에 &를 붙여주면, 백그라운드에서 진행됩니다~
# os.system("python sensor/all_upload.py &") 
# os.system("python camera/timelapse.py")

# Server Url
URL = 'http://deepmind.dothome.co.kr/controller.php'

# config.yml에서 설정한것들을 가져옴
config = yaml.safe_load(open('camera/config.yml'))
video_dir = os.path.join(
  sys.path[0],
  'camera/video'
)
config['video_dir'] = video_dir

sensor = Sensor(URL)
timelapse = Timelapse(config)

sensor.start()
timelapse.start()


# queue = Queue()
# processes = {
#   'sensor': Process(target=sensor.start),
#   'timelapse': Process(target=timelapse.start)
# }

# processes['timelapse'].start()
# processes['sensor'].start()