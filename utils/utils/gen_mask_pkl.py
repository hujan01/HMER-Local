'''
Author: sigmoid
Description: 
Email: 595495856@qq.com
Date: 2021-02-04 21:47:40
LastEditTime: 2021-02-04 22:17:35
'''
import os
import sys

import pickle as pkl
import cv2
from imageio import imread

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
    imagePath = "data/maskImage_p25"
    scpFile = 'data/label/train_caption_normal.txt'
    mask_pkl_out = 'data/train_mask.pkl'
    gen_mask_pkl(imagePath, scpFile, mask_pkl_out)