'''
Author: sigmoid
Description: 
Email: 595495856@qq.com
Date: 2020-12-31 15:08:27
LastEditTime: 2021-03-06 19:15:42
'''
import os 
import cv2
from matplotlib import pyplot as plt

root = 'offline/test2016' # 测试图片路径

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
    '''
    description: 显示两种预测结果
    param {*}
    '''
    print('recognize>>>>>>>>>>')
    latex_dict1 = read_txt(txt1)
    latex_dict2 = read_txt(txt2)

    for k in latex_dict1.keys():
        latex1 = latex_dict1[k]
        latex2 = latex_dict2[k]
        img_name = k + '.png'

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

if __name__ == '__main__':
    pred1_path = 'parser/amend.txt'
    pred2_path = 'parser/correct_471.txt'

    visual_result(pred1_path, pred2_path)
