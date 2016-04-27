#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 服务端 发送视频/图片
import os
import socket
from threading import Thread
from VideoCapture import Device
import time
import subprocess
import shlex
import traceback

from PIL import ImageEnhance


class ACTION(object):
    BEGIN = "begin"
    FINISH = "finish"
    SERVICE_BEGIN_FLAG = "Service begin"
    VIDEO = "video"
    PHOTO = "photo"
    SERVICE_FINISH_FLAG = "Service finish"


# 主机地址 和 端口
# host = socket.gethostbyname(socket.gethostname())
host = '0.0.0.0'
port = 10218

data_buffer = 1024 * 10

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))

is_sending = False
client_address = ('', 0)
client_data = ""
second = None


# 接收线程
class UdpReceiver(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.thread_stop = False

    def run(self):
        while not self.thread_stop:
            global is_sending
            global client_address
            global client_data
            global second
            try:
                data, address = server_socket.recvfrom(data_buffer)
            except:
                # traceback.print_exc()
                continue
            # 解析数据
            data = data.split(":")
            message = safe_get_list_data(data, 0)
            second = safe_get_list_data(data, 1)

            client_address = address

            if message == ACTION.BEGIN:
                is_sending = True
                print ACTION.SERVICE_BEGIN_FLAG
                server_socket.sendto(ACTION.SERVICE_BEGIN_FLAG, address)
            elif message == ACTION.FINISH:
                is_sending = False
                print ACTION.SERVICE_FINISH_FLAG
            else:
                is_sending = True
                client_data = message

    def stop(self):
        self.thread_stop = True
        print "UdpReceiver close"


receive_thread = UdpReceiver()
# 守护进程
receive_thread.setDaemon(True)
receive_thread.start()

loop = True

cam = Device()


def get_photo(photo_name):
    """
    图片微调
    :param photo_name:
    :return:
    """
    camshot = ImageEnhance.Brightness(cam.getImage(timestamp=1)).enhance(1.1)
    camshot = ImageEnhance.Contrast(camshot).enhance(1.0)
    camshot.save(photo_name, quality=95)


def send_file(file_name):
    """
    发送文件
    :param file_name:
    :return:
    """
    file_name = file_name.replace("\\", os.sep)
    with open(file_name, 'rb') as f:
        while True:
            data = f.read(data_buffer)
            if not data:
                server_socket.sendto(ACTION.SERVICE_FINISH_FLAG, client_address)
                break
            server_socket.sendto(data, client_address)
            time.sleep(0.05)


def remove(src):
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            traceback.print_exc()
    elif os.path.isdir(src):
        for f in os.listdir(src):
            path = os.path.join(src, f)
            remove(path)
        try:
            os.rmdir(src)
        except:
            traceback.print_exc()


def send_photo(photo_name):
    """
    截图
    :param photo_name:
    :return:
    """
    get_photo(photo_name)
    send_file(photo_name)
    remove(photo_name)


is_stop = False


def stop(sec):
    global is_stop
    time.sleep(float(sec))
    is_stop = True


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


temp_dir = "temp"


def send_video(video_name):
    """
    发送视频
    :param video_name:
    :return:
    """
    if second:
        global is_stop
        sequence = 100
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # 生成图片序列
        Thread(target=stop, args=(second,)).start()
        while not is_stop:
            file_name = "%d.jpeg" % sequence
            get_photo(os.path.join(temp_dir, file_name))
            sequence += 1

        # 生成视频
        video_seq = os.path.join(temp_dir, "%3d.jpeg")
        video_path = os.path.join(temp_dir, video_name)

        cmd = "ffmpeg -y -start_number 100 -r 25 -i %s -c:v libx264  " \
              "-pix_fmt yuv420p -r 30  %s " % (video_seq, video_path)

        kill(subprocess.Popen(shlex.split(cmd, posix=False), shell=True))

        send_file(video_path)

        remove(temp_dir)


def safe_get_list_data(data, index, default=None):
    try:
        return data[index]
    except IndexError:
        return default


# 处理线程
def do_handler():
    global is_sending
    while loop:
        if is_sending:
            if client_data == ACTION.VIDEO:
                send_video("temp.mp4")
            elif client_data == ACTION.PHOTO:
                send_photo("temp.jpeg")

        else:
            time.sleep(1)
    # 关闭接收线程
    receive_thread.stop()


handler_thread = Thread(target=do_handler)
handler_thread.start()

# 主线程 主要控制程序关闭
try:
    while True:
        time.sleep(3600)
except KeyboardInterrupt:
    # 实现完美退出
    loop = False

handler_thread.join()
server_socket.close()
print "Exit"
