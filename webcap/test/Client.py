#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 客户端放在Web 服务端
import shlex
import socket
from threading import Thread
import time
import sys
import subprocess

from PIL import Image


class ACTION(object):
    BEGIN = "begin"
    FINISH = "finish"
    SERVICE_BEGIN_FLAG = "Service begin"
    VIDEO = "video"
    PHOTO = "photo"
    SERVICE_FINISH_FLAG = "Service finish"
    CONNECTION_ERROR = "Connection error"
    TRANSFORM_ERROR = "Transform error"
    CONNECTION_DROP = "Connection drop"


server_address = ('localhost', 10218)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(5)

data_buffer = 1024 * 10

is_need = True


def stop():
    global is_need
    time.sleep(5)
    is_need = False


def begin():
    while True:
        client_socket.sendto(ACTION.BEGIN, server_address)
        try:
            message, address = client_socket.recvfrom(data_buffer)
            if message == ACTION.SERVICE_BEGIN_FLAG:
                print message
                break
        except socket.timeout:
            print ACTION.CONNECTION_DROP
            continue
        except:
            print ACTION.CONNECTION_ERROR
            sys.exit(1)


def end():
    client_socket.sendto(ACTION.FINISH, server_address)


def _get_video():
    client_socket.sendto(ACTION.VIDEO, server_address)
    with open('1.txt', 'a') as f:
        Thread(target=stop, ).start()
        while is_need:
            try:
                data, address = client_socket.recvfrom(data_buffer)
            except socket.timeout:
                print ACTION.TRANSFORM_ERROR
                continue

            print(data)
            f.write(data)


def save_file(file_name):
    with open(file_name, 'wb') as f:
        while True:
            try:
                data, address = client_socket.recvfrom(data_buffer)
            except socket.timeout:
                print ACTION.TRANSFORM_ERROR
                continue
            if data == ACTION.SERVICE_FINISH_FLAG:
                end()
                break
            f.write(data)


def kill(proc):
    """
    关闭子进程
    :param proc:
    :return:
    """
    while True:
        if proc.poll() is not None:
            proc.terminate()
            break


res = (250, 156)


def get_photo(photo_path, thumbnail_path):
    begin()
    client_socket.sendto(ACTION.PHOTO, server_address)
    save_file(photo_path)
    # 获取缩略图
    img = Image.open(photo_path)
    img.resize(res, Image.ANTIALIAS).save(thumbnail_path)


def get_video(video_path, thumbnail_path, second):
    begin()
    data = "%s:%d" % (ACTION.VIDEO, second)
    client_socket.sendto(data, server_address)
    save_file(video_path)

    cmd = 'ffmpeg -y -i %s -f image2 -t 0.001 -s 300x200 %s ' % (video_path, thumbnail_path)

    kill(subprocess.Popen(shlex.split(cmd, posix=False), shell=True))


def do_task():
    # get_photo("2.jpeg", "thumbnail.jpeg")
    get_video("jj.mp4", "thumbnail.jpeg", 8)
    # end()


th = Thread(target=do_task)
th.start()
th.join()

client_socket.close()
