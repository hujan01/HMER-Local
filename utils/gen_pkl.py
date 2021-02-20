'''
Author: sigmoid
Description:  生成pkl文件
Email: 595495856@qq.com
Date: 2020-11-27 15:30:41
LastEditTime: 2021-02-19 01:33:10
'''
import os
import sys

import pandas as pd
import pickle as pkl
import numpy as np
import cv2
from imageio import imread

def gen_pkl(image_path, label_path, outfile_path, channels=1) :

    sentNum=0
    features={}

    scpFile = open(label_path)
    lines = scpFile.readlines()

    for l in lines:
        line = l.strip() # remove the '\r\n'
        if not line: 
            break
        else:
            key = line.split('\t')[0]
            image_file = os.path.join(image_path, key+'.png')
            im = cv2.imread(image_file)
            im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 

            mat = np.zeros([channels, im.shape[0], im.shape[1]], dtype='uint8')
            
            for channel in range(channels):
                image_file = os.path.join(image_path, key+'.png')
                im = cv2.imread(image_file)
                im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                mat[channel, :, :] = im
            sentNum = sentNum + 1
            features[key] = mat
            print('process sentences ', sentNum)

    print('load images done. sentence number ', sentNum)

    outPkl = open(outfile_path, 'wb')
    pkl.dump(features, outPkl)
    print('save file done')

def gen_mask_pkl(imagePath, scpFile, outFile):

    features = {}
    sentNum = 0
    
    scpFile = open(scpFile)
    lines = scpFile.readlines()
    for l in lines:
        line = l.strip()
        if not line: 
            break
        else:
            key = line.split('\t')[0]
            image_file = os.path.join(imagePath, key + '_mask.png')
            im = cv2.imread(image_file, 0)
            im = im/255
            features[key] = im
            sentNum += 1
            print('process sentences ', sentNum)
    print('load images done. sentence number ', sentNum)
    outpkl = open(outFile, 'wb')
    pkl.dump(features, outpkl)
    print("success generate pkl")

if __name__ == "__main__":
    image_path = 'offline/train' # 图片文件夹
    label_path = 'data/label/train_caption.txt' # 标签文件
    outfile_path = 'train_v3.pkl' # 生成的pkl文件
    gen_pkl(image_path, label_path, outfile_path)
 