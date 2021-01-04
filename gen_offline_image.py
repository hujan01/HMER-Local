'''
Author: sigmoid
Description: 
Email: 595495856@qq.com
Date: 2020-11-27 10:48:29
LastEditTime: 2021-01-04 21:44:38
'''

import os, glob, shutil
from datetime import datetime

# import inkml2img as inkml2img
from inkml2img_v1 import inkml2img

dataset = 'train' # 需要转换的数据集

data_root = 'D:/DataSet/DataInkml'
dataPath = os.path.join(data_root, dataset) 
targetFolder = os.path.join('offline', dataset) 
logger = open('log.txt', 'w+')
    
def writeLog(message):
    logger.write("[" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "] " + str(message) + "\n")

def createDirectory(dirPath):
    if not os.path.exists(dirPath): 
        os.mkdir(dirPath)
        writeLog("Create " + dirPath)

if __name__ == "__main__": 
    writeLog("Start processing.")
    createDirectory(targetFolder)

    listFiles = glob.glob(os.path.join(dataPath, '*.inkml'))
    numberOfFile = len(listFiles)
    writeLog("There are " + str(numberOfFile) + " files in " + dataPath)
    cnt = 0

    for fileInkml in listFiles:
        cnt = cnt + 1
        fileName =  os.path.splitext(fileInkml.split('\\')[-1])[0] 
        print("Processing %s [%d/%d]" % (fileName, cnt, numberOfFile))
        writeLog("[" + str(cnt) + "/" + str(numberOfFile) + "]" + "Processed " + fileInkml + " --> " + targetFolder + "\\" + fileName + ".png")
        try:
            imagePath = os.path.join(targetFolder, fileName+'.png')
            inkml2img(fileInkml, imagePath)
        except:
            writeLog("Failed!")
            print("An error occured!")
        writeLog("Successful!")