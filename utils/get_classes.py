'''
Author: sigmoid
Description: 得到数据集中符号的分布
Email: 595495856@qq.com
Date: 2021-01-08 15:25:49
LastEditTime: 2021-02-19 01:30:40
'''
label_path = "data/label/train_caption.txt"

classed = {}
with open(label_path) as fr:
    lines = fr.readlines()
    for l in lines:
        spt = l.strip().split()
        label = spt[1:]
        for c in label:
            if c not in classed.keys():
                classed[c] = 1
            else :
                classed[c] += 1
print(sorted(classed.items(), key = lambda kv:(kv[1], kv[0])))   