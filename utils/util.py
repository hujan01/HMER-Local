'''
Author: sigmoid
Description: 统计正确预测的数目，可视化识别结果, 分析两个预测结果的差异
Email: 595495856@qq.com
Date: 2020-12-31 15:12:42
LastEditTime: 2021-02-26 16:52:54
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

def main1(rightPredPath, allPredPath):
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

def get_length_distribute(filePath, valid_uidlist) :
    dic = read_txt(filePath)

    length = {}
    for uid, latex in dic.items():
        if not uid in valid_uidlist: 
            continue
        latex_ls = latex.split()  
        latex_length = len(latex_ls) # 该latex长度 包括结构字符{}
        if latex_length<10 :
            n = length.setdefault('0', 1)
            n += 1
            length['0'] = n
        elif 10<=latex_length<20 :
            n = length.setdefault('1', 1)
            n += 1
            length['1'] = n
        elif 20<=latex_length<30  :
            n = length.setdefault('2', 1)
            n += 1
            length['2'] = n
        elif 30<=latex_length<40 :
            n = length.setdefault('3', 1)
            n += 1
            length['3'] = n
        elif 40<=latex_length<50 :
            n = length.setdefault('4', 1)
            n += 1
            length['4'] = n
        elif 50<=latex_length<60 :
            n = length.setdefault('5', 1)
            n += 1
            length['5'] = n
        elif 60<=latex_length<70 :
            n = length.setdefault('6', 1)
            n += 1
            length['6'] = n
    return length

def get_train_length_distribute() :
    dic = read_txt('data/label/train_caption.txt')
    
    valid_uidlist = []
    with open('results/valid_image_list.txt') as fr:
        valid_uidlist = [x.strip() for x in fr.readlines()]
    s = 0
    x = 0
    length = {}
    for uid, latex in dic.items():
        if not uid in valid_uidlist: 
            s += 1
            continue
        x += 1
        latex_ls = latex.split()  
        latex_length = len(latex_ls) # 该latex长度 包括结构字符{}
        
        if latex_length<10 :
            n0 = length.setdefault('0', 0)
            n0 += 1
            length['0'] = n0
        elif 10<=latex_length<20 :
            n1 = length.setdefault('1', 0)
            n1 += 1
            length['1'] = n1
        elif 20<=latex_length<30  :
            n2 = length.setdefault('2', 0)
            n2 += 1
            length['2'] = n2
        elif 30<=latex_length<40 :
            n3 = length.setdefault('3', 0)
            n3 += 1
            length['3'] = n3
        elif 40<=latex_length<50 :
            n4 = length.setdefault('4', 0)
            n4 += 1
            length['4'] = n4
        elif 50<=latex_length<60 :
            n5 = length.setdefault('5', 0)
            n5 += 1
            length['5'] = n5
        elif 60<=latex_length<70 :
            n6 = length.setdefault('6', 0)
            n6 += 1
            length['6'] = n6
    print(length)

if __name__ == "__main__":
    real_path = 'data/label/test_caption_2016_v2.txt'
    pred1_path = 'results/recognize_tree_2016.txt'
    pred2_path = 'results/recognize_MDA_2016.txt'
    
    correct1 = 'parser/correct_506.txt'
    correct2 = 'parser/correct_471.txt'

    main1(correct2, pred1_path)
    # compare_diff(pred1, pred2)
    # visual_result(pred1, pred2)
    # get_correct_numbers(pred2_path, real_path)
    # compare_diff(correct1, correct2)
    # visual_result(pred1, pred2)
    # get_train_length_distribute()
    # valid_uidlist = list(read_txt(pred2).keys())

    # gt_length_distr = get_length_distribute(real_path, valid_uidlist)
    # pred_length_distr = get_length_distribute(pred1, valid_uidlist)
    # for k, gt_length in gt_length_distr.items():
    #     if k not in pred_length_distr: 
    #         continue
    #     pred_length = pred_length_distr[k]
    #     print('{} ExpRate: {}'.format(k, pred_length/gt_length))