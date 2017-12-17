# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import requests
from datetime import datetime

URL = 'http://deepmind.dothome.co.kr/upload.php'

class RPFVideoUploader(object):
  def __init__(self, path):
    self.path = path
    self.file_name = os.path.basename(self.path)
    self.total_bytes = os.path.getsize(self.path)

  def upload_init(self):
    request_data = {
      'upload': True,
      'command': 'INIT',
      'media_type': 'video/mp4',
      'file_name': self.file_name,
      'total_bytes': self.total_bytes
    }
    req = requests.post(url=URL, data=request_data)
    print req.text
    return req.json()['response_code']

  def upload(self, callback):
    segment_id = 0
    bytes_sent = 0
    file = open(self.path, 'rb')
    while bytes_sent < self.total_bytes:
      chunk = file.read(1024*1024)
      print "\n append chunk"
      request_data = {
        'command': 'APPEND',
        'segment_index': segment_id,
        'file_name': self.file_name
      }
      files = {
        'media': chunk
      }
      req = requests.post(url=URL, data=request_data, files=files)
      print req.text
      if req.status_code < 200 or req.status_code > 299:
        print req.status_code
        print req.text
        sys.exit(0)

      segment_id += 1
      bytes_sent = file.tell()

      print "%s of %s bytes uploaded" % (str(bytes_sent), str(self.total_bytes))

    print "upload chunks complete!"
    if callback is not None {
      callback()
    }