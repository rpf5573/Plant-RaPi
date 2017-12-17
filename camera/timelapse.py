# -*- coding: utf-8 -*-

from picamera import PiCamera
import errno
import os
import sys
import threading
from datetime import datetime
import time
import upload
import shutil


class Timelapse:
  def __init__(self, config):
    self.video_dir = config['video_dir']
    self.config = config
    self.image_number = config['image_number']

  def create_timestamped_dir(self):
    # 먼저 폴더를 지우고 시작하자
    self.remove_video_folder()
    try:
      os.makedirs(self.video_dir)
    except OSError as e:
      if e.errno != errno.EEXIST:
        raise

  def set_camera_options(self, camera, config):
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

  def capture_image(self, config):
    print "Let's take a picture"
    try:
      if (self.image_number < (config['total_images'] - 1)):
        # 사진 찍고 저장
        self.camera.capture(self.video_dir + '/image{0:05d}.jpg'.format(self.image_number))

        # 정해진 시간 이후에 또 사진을 찍는다
        threading.Timer(config['interval'], self.capture_image, args=[config] ).start()

        self.image_number += 1
      else:
        print '\n timelapse capture complete!'

        print "\n let's make timelapse video"

        self.make_video()

        # thread = threading.Timer(5, self.make_video).start()

    except KeyboardInterrupt, SystemExit:
      sys.exit()
      print '\n timelapse capture cancelled'      

  def make_video(self):
    now = datetime.now()
    nowDate = now.strftime('%Y-%m-%d_%H_%M_%S')
    video_path = self.video_dir + '/timelapse' + nowDate + '.mp4'
    os.system('avconv -r 20 -i ' + self.video_dir + '/image%05d.jpg -vf format=yuv420p ' + video_path)
    print 'make video complete'
    self.upload_video(video_path)

  def upload_video(self, path):
    print path
    rpfVideoUploader = upload.RPFVideoUploader(path)
    if rpfVideoUploader.upload_init() == 201:
      print 'video upload start'
      # 업로드 완료후에, 이미지 및 동영상을 라즈베리파이에서 삭제 시킨다
      if self.config['remove_folder_after_make_timelapse'] == True:
        rpfVideoUploader.upload(self.restart)
      else:
        rpfVideoUploader.upload(None)

  def restart(self):
    self.remove_video_folder()
    self.image_number = 0
    self.start()

  def remove_video_folder(self):
      print 'remvoe video folder'
      shutil.rmtree(self.video_dir, ignore_errors=True)
      print 'did remove video folder'

  def start(self):
    print 'timelapse start!'
    if self.config['create_new_folder'] == True :
      self.create_timestamped_dir()
    
    self.camera = PiCamera()
    self.set_camera_options(self.camera, self.config)
    self.capture_image(self.config)