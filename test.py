# -*- coding: utf-8 -*-
import os
import sys
import sensor
import camera.timelapse

print "라즈베리파이 센서&카메라 테스트를 시작합니다."
# 끝에 &를 붙여주면, 백그라운드에서 진행됩니다~
# os.system("python sensor/all_upload.py &") 
# os.system("python camera/timelapse.py")

# config.yml에서 설정한것들을 가져옴
config = yaml.safe_load(open(os.path.join(sys.path[0], "/camera/config.yml")))
video_dir = os.path.join(
  sys.path[0],
  'camera/video'
)
config['video_dir'] = video_dir

timelapse = Timelapse(config)
timelapse.remove_video_folder()
timelapse.create_timestamped_dir()
timelapse.start()

