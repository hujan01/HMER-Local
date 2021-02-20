'''
Author: sigmoid
Description: 绘制矩形框
Email: 595495856@qq.com
Date: 2021-01-13 21:14:04
LastEditTime: 2021-02-19 01:41:16
'''
import os
import json
from PIL import Image
import cv2

image_path = 'offline/train'
bbox_path = 'bbox/train'

out_image_path = 'examples/'

images = os.listdir(image_path)
for image in images:
    # image = '70_leo.png'
    txt_name = os.path.splitext(image)[0]+'.txt'
    txt_path = os.path.join(bbox_path, txt_name)
    img = cv2.imread(os.path.join(image_path, image))
    with open(txt_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            spt = line.split()
            sym = spt[0]
            x_min, y_min, x_max, y_max = spt[1:]
            cv2.rectangle(img, (int(x_min),int(y_min)), (int(x_max),int(y_max)), (0,255,0), 4)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, sym, (int(x_min)+3, int(y_min)), font, 1, (0, 0, 255), 1)
            cv2.imwrite(out_image_path + image, img)
    print('success draw %s'%(image))