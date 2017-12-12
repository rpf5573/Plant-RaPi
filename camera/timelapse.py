# -*- coding: utf-8 -*-

from picamera import PiCamera
import errno
import os
import sys
import threading
from datetime import datetime
from time import sleep
import yaml
import upload
import shutil

# config.yml에서 설정한것들을 가져옴
config = yaml.safe_load(open(os.path.join(sys.path[0], "config.yml")))

image_number = 0

camera = PiCamera()

dir = os.path.join(
  sys.path[0],
  'video'
)
create_timestamped_dir(dir)

camera = set_camera_options(camera)

# 시작한다
capture_image()

def create_timestamped_dir(dir):
  try:
    os.makedirs(dir)
  except OSError as e:
    if e.errno != errno.EEXIST:
      raise

def set_camera_options(camera):
  # 해상도 설정
  if config['resolution']:
    camera.resolution = (
      config['resolution']['width'],
      config['resolution']['height']
    )
  
  # ISO 설정
  if config['iso']:
    camera.iso = config['iso']
  
  # 밝기 설정
  if config['brightness']:
    camera.iso = config['brightness']

  # 셔터 스피드 설정.
  if config['shutter_speed']:
    camera.shutter_speed = config['shutter_speed']
    # 셔터스피드가 제대로 설정되도록 1초정도 기다려 준다
    sleep(1)
    camera.exposure_mode = 'off' # 뭔지 모르겠음

  # 색조 설정
  if config['white_balance']:
    camera.awb_mode = 'off'
    camera.awb_gains = (
      config['white_balance']['red_gain'],
      config['white_balance']['blue_gain']
    )

  # 카메라 회전 설정
  if config['rotation']:
    camera.rotation = config['rotation']

  # 카메라 설정 완료
  return camera

def capture_image():

  try:
    if (image_number < (config['total_images'] - 1)):
      # 사진 찍고 저장
      camera.capture(dir + '/image{0:05d}.jpg'.format(image_number))

      # 정해진 시간 이후에 또 사진을 찍는다
      thread = threading.Timer(config['interval'], capture_image).start()
      image_number += 1
    else:
      print '\n timelapse capture complete!'

      print "\n let's make timelapse video"

      thread = threading.Timer(5, make_video).start()

  except KeyboardInterrupt, SystemExit:
    print '\n timelapse capture cancelled'      

def make_video():
  now = datetime.now()
  nowDate = now.strftime('%Y-%m-%d_%H_%M_%S')
  video_path = dir + '/timelapse' + nowDate + '.mp4'
  os.system('avconv -r 20 -i ' + dir + '/image%05d.jpg -vf format=yuv420p ' + video_path)
  print 'make video complete'

  upload_video(video_path)

def upload_video(path):
  print path
  rpfVideoUploader = upload.RPFVideoUploader(path)
  if rpfVideoUploader.upload_init() == 201:
    print 'video upload start'
    # 업로드 완료후에, 이미지 및 동영상을 라즈베리파이에서 삭제 시킨다
    rpfVideo.upload(remove_video_folder)

def remove_video_folder():
  print 'remvoe photo/video folder'
  dest = 'video'
  shutil.rmtree(dest, ignore_errors=True)