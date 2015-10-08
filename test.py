#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'
import subprocess
import shlex
import os

# size = 'ffprobe -v error -show_entries format=size -of default=noprint_wrappers=1:nokey=1 dump.mp4 > file'
# proc = subprocess.Popen(shlex.split(size), shell=True)
# time.sleep(1)
# proc.kill()
# size = ""
# with open('file', 'r') as infile:
#     for line in infile.readlines():
#         size += line.strip()
#
# print(size)
# os.remove('file')
import time

video = "ffmpeg -y -i rtsp://218.204.223.237:554/live/1/66251FC11353191F/e7ooqwcfbqjoo80j.sdp -c copy -t 10 dump.mp4"
proc = subprocess.Popen(shlex.split(video), shell=True)
time.sleep(20)
proc.terminate()
os.remove('dump.mp4')
