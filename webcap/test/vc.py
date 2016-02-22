#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'wuyuxi'

# from VideoCapture import Device
#
# cam = Device()
# cam.getImage(timestamp=0).resize((500, 650)).save('demo.jpg', quality=80)
# cam.getImage(timestamp=0).resize((300, 200)).save('demo.jpg', quality=80)


# from VideoCapture import Device
# import sys
#
# import pygame
# from PIL import ImageEnhance
#
# res = (640, 480)
# pygame.init()
# cam = Device()
# screen = pygame.display.set_mode((640, 480))
# pygame.display.set_caption('Webcam')
# pygame.font.init()
# font = pygame.font.SysFont("Courier", 11)
#
#
# def disp(phrase, loc):
#     s = font.render(phrase, True, (200, 200, 200))
#     sh = font.render(phrase, True, (50, 50, 50))
#     screen.blit(sh, (loc[0] + 1, loc[1] + 1))
#     screen.blit(s, loc)
#
#
# brightness = 1.0
# contrast = 1.0
# shots = 100
#
# while 1:
#     camshot = ImageEnhance.Brightness(cam.getImage()).enhance(brightness)
#     camshot = ImageEnhance.Contrast(camshot).enhance(contrast)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT: sys.exit()
#     keyinput = pygame.key.get_pressed()
#
#     filename = "IMG_" + str(shots) + ".jpeg"
#     cam.saveSnapshot(filename, quality=80, timestamp=0)
#     shots += 1
#     camshot = pygame.image.frombuffer(camshot.tostring(), res, "RGB")
#     screen.blit(camshot, (0, 0))
#     disp("S:" + str(shots), (10, 4))
#     disp("B:" + str(brightness), (10, 16))
#     disp("C:" + str(contrast), (10, 28))
#     pygame.display.flip()

# import os
#
# root_path = os.getcwd()
# print(root_path)
#
# ll = []
# os.chdir(root_path)
# for file in os.listdir(root_path):
#     if file.endswith('.jpeg'):
#         ll.append(file)
#         os.remove(file)
# print(ll)
#
# print(os.getcwd())
