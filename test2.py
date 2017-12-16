# -*- coding: utf-8 -*-
import os
import sys
from multiprocessing import Process, Queue
import threading

class Test:
  def __init__(self):
    print '__init__ is called'
  
  def say_hello_again_and_again(self):
    print 'Hello :D'
    threading.Timer(1, self.say_hello_again_and_again).start()


test = Test()
#test.say_hello_again_and_again()
process = Process(target=test.say_hello_again_and_again)
process.start()
process.join()
