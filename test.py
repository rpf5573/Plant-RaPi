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
config = yaml.safe_load(open(os.path.join(sys.path[0], "config.yml")))

image_number = 201

camera = PiCamera()

# 일단 깔끔하게 지우고 시작하자!
remove_video_folder();

dir = os.path.join(
  sys.path[0],
  'video'
)
create_timestamped_dir(dir)

camera = set_camera_options(camera)

# 시작한다
capture_image()

