'''
Author: sigmoid
Description: 
Email: 595495856@qq.com
Date: 2020-12-31 15:08:27
LastEditTime: 2020-12-31 15:32:01
'''
import os 
import cv2
from matplotlib import pyplot as plt

root     = 'D:/DataSet/CROHME2016/test'
gtPath   = ''
predPath = "diff.txt"


real_dict = {}
with open('result/test_caption_2016_v1.txt') as fr:
    lines = fr.readlines()
    for l in lines:
        spt = l.strip().split('\t')
        imgName = spt[0]
        real_label = spt[1:]
        real_label = "".join(real_label)
        real_dict[imgName] = real_label
      

with open(predPath) as f:
    lines = f.readlines()
    for i, l in enumerate(lines) :
        print(i)
        spt = l.split('\t')
        imgName = spt[0]+'_0.bmp'
        latex = spt[1].strip()
        
        predlatex = ''.join(latex)
        reallatex = real_dict[spt[0]]
        
        print(imgName)
        imgPath = os.path.join(root, imgName)
        img = cv2.imread(imgPath)
        try:
            print("gt latex", reallatex)
            print("pred latex", predlatex)
            plt.subplot(311)
            plt.imshow(img)
            plt.subplot(312)
            plt.text(0.2, 0.5, r"${}$".format(reallatex), fontsize=20) # 真实
            plt.subplot(313)
            plt.text(0.2, 0.5, r"${}$".format(predlatex), fontsize=20) # 预测
            plt.show()

        except:
            print("latex error!!!")