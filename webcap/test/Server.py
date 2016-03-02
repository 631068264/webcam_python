#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 服务端 发送视频/图片

# error: [Errno 10040] 转用TCP
# http://stackoverflow.com/questions/1447684/error-trying-to-pass-large-image-over-socket-in-python
from VideoCapture import Device
import os
import socket

from threading import Thread

import time


class ACTION(object):
    BEGIN = "begin"
    FINISH = "finish"
    SERVICE_BEGIN_FLAG = "Service begin"
    VIDEO = "video"
    PHOTO = "photo"
    SERVICE_FINISH_FLAG = "Service finish"


# 主机地址 和 端口
# host = socket.gethostbyname(socket.gethostname())
host = 'localhost'
port = 10218
data_buffer = 1024 * 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen(5)
client_socket, address = server_socket.accept()

is_sending = False
client_data = ""


# 接收线程
class UdpReceiver(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.thread_stop = False

    def run(self):
        while not self.thread_stop:
            global is_sending, client_data, client_socket
            data = client_socket.recv(data_buffer)
            if data == ACTION.BEGIN:
                is_sending = True
                client_socket.send(ACTION.SERVICE_BEGIN_FLAG)
            elif data == ACTION.FINISH:
                is_sending = False
                print ACTION.SERVICE_FINISH_FLAG
            else:
                is_sending = True
                client_data = data

    def stop(self):
        self.thread_stop = True
        print "UdpReceiver close"


receive_thread = UdpReceiver()
# 守护进程
receive_thread.setDaemon(True)
receive_thread.start()

loop = True
cam = Device()


# 处理线程
def do_handler():
    while loop:
        if is_sending:
            if client_data == ACTION.VIDEO:
                data = "1"
                client_socket.send(data)
                time.sleep(0.05)
            elif client_data == ACTION.PHOTO:
                cam.saveSnapshot('catch.jpg', quality=95)
                with open('catch.jpg', 'rb') as f:
                    while True:
                        data = f.read(data_buffer)
                        if not data:
                            break
                        client_socket.send(data)
                os.remove('catch.jpg')
                time.sleep(0.05)
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
client_socket.close()
print "Exit"
