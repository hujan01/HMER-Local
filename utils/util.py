'''
Author: sigmoid
Description: 统计正确预测的数目，可视化识别结果, 分析两个预测结果的差异
Email: 595495856@qq.com
Date: 2020-12-31 15:12:42
LastEditTime: 2021-02-04 17:17:16
'''
import os

import cv2
from matplotlib import pyplot as plt
# 图片路径
root = 'D:/DataSet/CROHME2016/valid'

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
    
def compare_diff(pred1, pred2):
    """
        比较两个正确预测结果之间的差异性
    """
    pred1_dict = read_txt(pred1)
    pred2_dict = read_txt(pred2)
    
    key1 = pred1_dict.keys()
    key2 = pred2_dict.keys()

    # 分析
    cor1 = len(pred1_dict)
    cor2 = len(pred2_dict)
    samepred = 0
    for k in key1:
        if k in key2: # 说明pred1 和 pred2 都预测正确了
            samepred += 1
        else:
            print(k) # pred1预测正确
            try:
                print(readLabel("v1", k))
                print(readLabel("v2", k))
            except:
                continue 
    print("===============")
    print("only pred1 right: {}".format(cor1-samepred))
    print("===============")
    print("only pred2 right: {}".format(cor2-samepred))
    print("===============")
    print("all right: {}".format(samepred))     

def get_correct_numbers(predPath, gtPath):
    """ 
        统计正确预测的公式序列，保存到txt文件中 
    """
    gt_dict = read_txt(gtPath)
    pred_dict = read_txt(predPath)
    
    fw_error = open('parser/error.txt', 'w+')
    correct = {} # 正确预测的公式
    for (img_name, gt_latex) in gt_dict.items():
        try:
            print(gt_latex) # gt
            pred_latex = pred_dict[img_name]
            print(pred_latex) # pred
            if gt_latex == pred_latex: # 预测正确的latex 保存在字典中
                correct[img_name] = gt_latex
            else:
                fw_error.write(img_name)
                fw_error.write('\t')
                fw_error.write("".join(pred_dict[img_name]))
                fw_error.write('\n')
        except:
            print("error")
    fw_error.close()

    right_num = len(correct)        
    with open('parser/correct_{}.txt'.format(right_num), 'w') as fw:
        for (k, v) in correct.items():
            fw.write(k)
            fw.write('\t')
            fw.write(''.join(v))
            fw.write('\n')
            
    print('{}/{}'.format(right_num, len(gt_dict)))

def visual_result(txt1, txt2):
    """
        可视化识别结果
        txt1: latex结果显示在第2行
        txt1: latex结果显示在第3行
    """
    print('recognize>>>>>>>>>>')
    latex_dict1 = read_txt(txt1)
    latex_dict2 = read_txt(txt2)

    for k in latex_dict1.keys():
        if k not in latex_dict2.keys():
            print(k)
            continue
        latex1 = latex_dict1[k]
        if len(latex1.split(' ')) < 20:
            continue
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

def fun1(rightPredPath, allPredPath):
    """
        哪些错误的案例被修正
    """
    right = {}
    with open(rightPredPath) as f1:
        lines = f1.readlines()
        for l in lines:
            spt = l.strip().split('\t')
            img_name = spt[0]
            latex = spt[1]
            right[img_name] = latex
    all_ = {}
    with open(allPredPath) as f2:
        lines = f2.readlines()
        for l in lines:
            spt = l.strip().split('\t')
            img_name = spt[0]
            latex = spt[1]
            all_[img_name] = latex 
    fw = open('amend.txt', 'w')
    for k in right.keys():
        if all_[k] != right[k]:
            fw.write(k+'\t'+all_[k])
            fw.write('\n')
    print("success!")   
    
if __name__ == "__main__":
    pred_path = 'results/recognition_baseline.txt'
    real_path = 'data/label/test_caption_2014.txt'

    pred1 = 'parser/correct_423.txt'
    pred2 = 'results/recognition_baseline.txt'
    # compare_diff(pred1, pred2)
    visual_result(pred1, pred2)
    # get_correct_numbers(pred_path, real_path)
    # visual_result(pred1, pred2)