#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'
from VideoCapture import Device
import os

cam = Device()
dir = "tmp"
if not os.path.exists(dir):
    os.makedirs(dir)
path = os.path.join(dir, "12.jpeg")
cam.saveSnapshot(path)
