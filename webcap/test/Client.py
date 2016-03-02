#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 客户端放在Web 服务端
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
    CONNECTION_ERROR = "Connection error"
    TRANSFORM_ERROR = "Transform error"


server_address = ('localhost', 10218)

data_buffer = 1024 * 1024
is_need = True

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)


def stop():
    global is_need
    time.sleep(5)
    is_need = False


def begin():
    while True:
        client_socket.send(ACTION.BEGIN)
        data = client_socket.recv(2048)
        if data == ACTION.SERVICE_BEGIN_FLAG:
            print data
            break


def end():
    client_socket.send(ACTION.FINISH)


def get_photo():
    client_socket.send(ACTION.PHOTO)
    is_stop = False
    with open("demo.jpg", "wb") as f:
        while not is_stop:
            try:
                data = client_socket.recv(data_buffer)
            except socket.error:
                print ACTION.TRANSFORM_ERROR
                continue
            is_stop = True if data else False
            f.write(data)


def get_video():
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


def do_task():
    begin()
    get_photo()
    # get_video()
    end()


th = Thread(target=do_task)
th.start()
th.join()

client_socket.close()
