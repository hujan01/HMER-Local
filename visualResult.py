'''
Author: sigmoid
Description: 
Email: 595495856@qq.com
Date: 2020-12-31 15:08:27
LastEditTime: 2021-01-10 18:19:48
'''
import os 
import cv2
from matplotlib import pyplot as plt

root     = 'D:/DataSet/CROHME2016/test' # 测试图片路径
gt_path   = '' 
pred_path = "amend.txt"

real_dict = {}
with open('results/correct_497.txt') as fr:
    lines = fr.readlines()
    for l in lines:
        spt = l.strip().split('\t')
        imgName = spt[0]
        real_label = spt[1:]
        real_label = "".join(real_label)
        real_dict[imgName] = real_label


def read_txt(txtPath):
    res_dict = {}
    with open(txtPath) as fr:
        lines = fr.readlines()
        for l in lines:
            spt = l.strip().split('\t')
            img_name = spt[0]
            latex = spt[1:]
            latex = "".join(latex)
            res_dict[img_name] = latex
    return res_dict

def visual_result(txt1, txt2):
    """
        txt1: latex结果显示在第2行
        txt1: latex结果显示在第3行
    """
    print('recognize>>>>>>>>>>')
    latex_dict1 = read_txt(txt1)
    latex_dict2 = read_txt(txt2)

    for k in latex_dict1.keys():
        latex1 = latex_dict1[k]
        latex2 = latex_dict2[k]
        img_name = k + '.bmp'

        print(k)
        img_path = os.path.join(root, img_name)
        img = cv2.imread(img_path)
        try:
            print("latex1: ", latex1)
            print("latex2: ", latex2)
            plt.subplot(311)
            plt.imshow(img)
            plt.subplot(312)
            plt.text(0.2, 0.5, r"${}$".format(latex1), fontsize=20) # 真实
            plt.subplot(313)
            plt.text(0.2, 0.5, r"${}$".format(latex2), fontsize=20) # 预测
            plt.show()
        except:
            print("latex error!!!")
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