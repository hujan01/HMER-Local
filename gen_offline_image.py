'''
Author: sigmoid
Description: 生成离线图片和符号的矩形框
Email: 595495856@qq.com
Date: 2020-11-27 10:48:29
LastEditTime: 2021-02-26 14:45:50
'''

import os, glob, shutil
from datetime import datetime
from utils.inkml2img import inkml2img_getbbox, inkml2img

def createDirectory(dirPath):
    if not os.path.exists(dirPath): 
        os.makedirs(dirPath)
  
if __name__ == "__main__": 

    dataset = 'train' # 数据集类型
    bbox_out_path = 'bbox/' # bbox路径
    bbox_out_path = os.path.join(bbox_out_path, dataset)
    createDirectory(bbox_out_path)
        
    data_root = 'data/DataInkml' # inkml文件根路径
    dataPath = os.path.join(data_root, dataset) 
    targetFolder = os.path.join('offline', dataset) 
    createDirectory(targetFolder)

    listFiles = glob.glob(os.path.join(dataPath, '*.inkml'))
    numberOfFile = len(listFiles)

    for fileInkml in listFiles:
        fileName = os.path.basename(fileInkml)
        fileName =  os.path.splitext(fileName)[0] 
        if fileName == 'MfrDB3088' :
            continue
        imagePath = os.path.join(targetFolder, fileName+'.png')
        # inkml2img_getbbox(fileInkml, imagePath, bbox_out_path)
        inkml2img(fileInkml, imagePath)