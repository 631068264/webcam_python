#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'
import subprocess
import shlex


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
# def get_src_path(device):
#     """
#     创建个人目录
#     :param device:
#     :return:
#     """
#     root_path = os.path.dirname(os.path.dirname(os.getcwd()))
#     download_path = os.path.join(root_path, "download")
#     personal_path = os.path.join(download_path, device)
#
#     if not os.path.exists(personal_path):
#         os.makedirs(personal_path)
#
#     return personal_path


# device = 'd1cc4dfcd4145a0a2ecd44cb3'
# real_device = get_real_device(device)
# path = get_src_path(device)
# src = os.path.join(path, 'dump.mp4')
# thumbnail = os.path.join(path, 'dump.jpg')
import time


def kill(proc):
    while True:
        if proc.poll() is not None:
            print("7")
            proc.terminate()
            break


def kill2(proc, dur):
    print(1)
    time.sleep(dur)
    print(2)
    proc.kill()
    print(3)


def kill3(proc):
    proc.wait()
    proc.terminate()


# video = "ffmpeg -y -i rtsp://218.204.223.237:554/live/1/66251FC11353191F/e7ooqwcfbqjoo80j.sdp -c copy -t 5 dump.mp4"
video = 'ffmpeg -y -i rtsp://192.168.1.163:554/0d0b0e608af645a0590d0c425.sdp -c:v libx264 -c:a libvo_aacenc -t 5 dump.mp4'
# change = 'ffmpeg -y -i dump.mp4 -c:v libx264 -c:a libvo_aacenc dump.mp4'
# thumb = 'ffmpeg -i ' + real_device + ' -f image2 -t 0.001 -s 352x240 ' + thumbnail
# proc1 = subprocess.Popen(shlex.split(thumb), shell=True)
# kill(proc1)
kill2(subprocess.Popen(shlex.split(video, posix=False), shell=True), 9)
# kill(subprocess.Popen(shlex.split(change, posix=False), shell=True))
