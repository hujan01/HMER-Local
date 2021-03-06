'''
Author: sigmoid
Description: 得到数据集中数学符号的数目分布
Email: 595495856@qq.com
Date: 2021-01-08 15:25:49
LastEditTime: 2021-03-06 19:07:26
'''
from matplotlib import pyplot as plt
import random

label_path = "data/label/train_caption.txt"

classed = {}
with open(label_path) as fr:
    lines = fr.readlines()
    for l in lines:
        spt = l.strip().split()
        label = spt[1:]
        for c in label:
            if c=='\cdots':
                c = '\ldots'
            elif c=='\cdot':
                c = '.'
            elif c in ['_', '^', '\\frac', '{', '}', '\limits']:
                continue
    
            if c not in classed.keys():
                classed[c] = 1
            else :
                classed[c] += 1

classed = sorted(classed.items(), key=lambda x:x[1], reverse=True)  
ks = [x[0] for x in classed]
vs = [x[1] for x in classed]

plt.figure(figsize=(20, 10), dpi=80)

width = 0.7
plt.bar(ks, vs, width, label='num', color='#C8D8FB')

plt.xticks(rotation=270)
plt.xlim(-1)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

plt.xlabel('类别')
plt.ylabel('数目')
# plt.subplots_adjust(top=1, bottom=0, right=0.93, left=0, hspace=0, wspace=0)
# plt.margins(0, 0)
plt.savefig('C:/Users/1/Desktop/HMER2020/figures/class.pdf')
plt.show()