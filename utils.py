'''
Author: sigmoid
Description: 
Email: 595495856@qq.com
Date: 2020-12-31 15:12:42
LastEditTime: 2020-12-31 17:37:09
'''
import os

# 图片路径
root = 'D:/DataSet/CROHME2016/test'

# 预测latex文件
predPath = 'results/recognition_47p21.txt'

# 真实latex文件
gtPath = 'data/label/test_caption_2016_v1.txt'

def gtDict():
    """ 真实latex """
    gt_dict = {} #图片名: 对应的latex
    with open(gtPath) as f:
        lines = f.readlines()
        for l in lines:
            spt = l.strip().split('\t')
            imgName = spt[0]
            latex = spt[1].split(' ')
            gt_dict[imgName] = latex
    return gt_dict

def get_correct_numbers():
    """ 统计正确预测的公式序列，保存到txt文件中 """
    gt_dict = gtDict()
    
    pred_dict = {}
    with open(predPath) as f:
        lines = f.readlines()
        for l in lines:
            spt = l.strip().split('\t')
            imgName = spt[0]
            latex = spt[1].split(' ')
            pred_dict[imgName] = latex
    
    fw_error = open("results/error.txt", 'w')
    correct = {} # 正确预测的公式
    for (imgName, gt_latex) in gt_dict.items():
        try:
            print(gt_latex) # real
            print(pred_dict[imgName]) # pred
            if gt_latex == pred_dict[imgName]: # 预测正确的latex 保存在字典中
                correct[imgName] = gt_latex
            else:
                fw_error.write(imgName+'\t')
                fw_error.write("".join(pred_dict[imgName]))
                fw_error.write('\n')
        except:
            print("error")
    fw_error.close()

    rightNum = len(correct)        
    with open('results/correct_{}.txt'.format(rightNum), 'w') as fw:
        for (k, v) in correct.items():
            fw.write(k)
            fw.write('\t')
            fw.write(' '.join(v))
            fw.write('\n')
            
    print('{}/{}'.format(rightNum, len(gt_dict)))

pred1Path = 'results\correct_497.txt'
pred2Path = 'results/recognition_48p50.txt'
def compare_diff():
    """
        比较两个正确预测结果之间的差异性
    """
    pred1_dict = {}
    with open(pred1Path) as fr:
        lines = fr.readlines()
        for l in lines:
            spt = l.strip().split('\t')
            imgName = spt[0]
            pred_label = spt[1]
            pred1_dict[imgName] = pred_label
    key1 = pred1_dict.keys()

    pred2_dict = {}
    with open(pred2Path) as fr:
        lines = fr.readlines()
        for l in lines:
            spt = l.strip().split('\t')
            imgName = spt[0]
            pred_label = spt[1]
            pred2_dict[imgName] = pred_label
    key2 = pred2_dict.keys()

    # 分析
    cor1 = len(pred1_dict)
    cor2 = len(pred2_dict)

    samepred = 0
    for k in key1:
        if k in key2: # 说明pred1 和 pred2 都预测正确了
            samepred += 1
        else:
            print(k)
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

if __name__ == "__main__":
    # get_correct_numbers()
    compare_diff()