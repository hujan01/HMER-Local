'''
Author: sigmoid
Description: 
Email: 595495856@qq.com
Date: 2021-01-29 17:29:23
LastEditTime: 2021-01-29 19:57:23
'''
from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.font_manager import FontProperties
import csv


# 创建一个绘图窗口
"""读取txt文件"""
def read_file(filePath):
    with open(filePath, 'r') as fr:
        line = fr.readline()
        spt = line.split()
        spt = [round(float(x), 2) for x in spt]
        return spt
 
'''读取csv文件，文件可以在tensorboard下载'''
def readcsv(files):
    csvfile = open(files, 'r')
    plots = csv.reader(csvfile, delimiter=',')
    head = next(plots) # 表头
    x = []
    y = []
    #读取csv文件中2,3列的数据，且转化为float类型
    for row in plots:
        y.append(float(row[2])) 
        x.append(float(row[1]))
    return x ,y
 
plt.figure()
 
x, y=readcsv("csv/run-trf_no-tag-loss.csv")
plt.plot(x, y, color='#FF7C80', label='no teacher force')
 
x1, y1=readcsv("csv/run-baseline-48p17-80-tag-loss.csv")
plt.plot(x1, y1, color='#C8D8FB', label='tfr=0.8')
 
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

# plt.ylim(0, 2)
# plt.xlim(0, 80)

plt.xlabel('Epoch', fontsize=10)
plt.ylabel('Loss', fontsize=10)
plt.legend(fontsize=8)
plt.show()
