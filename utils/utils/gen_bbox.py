'''
Author: sigmoid
Description: 
Email: 595495856@qq.com
Date: 2021-01-04 19:37:22
LastEditTime: 2021-01-18 22:08:03
'''
import sys, os, argparse

from skimage.draw import line
from skimage.io import imread, imsave
import scipy.ndimage as ndimage
import pickle
import xml.etree.ElementTree as ET
import numpy as np
import warnings
warnings.filterwarnings('ignore')


def get_traces_data(inkml_file_abs_path):
    """ 返回二维坐标 """
    traces_data = []

    tree = ET.parse(inkml_file_abs_path)
    root = tree.getroot()
    doc_namespace = "{http://www.w3.org/2003/InkML}"

    'Stores traces_all with their corresponding id'
    traces_all = [{'id': trace_tag.get('id'),
                    'coords': [[round(float(axis_coord)) if float(axis_coord).is_integer() else round(float(axis_coord) * 10000) \
                                    for axis_coord in coord[1:].split(' ')] if coord.startswith(' ') \
                                else [round(float(axis_coord)) if float(axis_coord).is_integer() else round(float(axis_coord) * 10000) \
                                    for axis_coord in coord.split(' ')] \
                            for coord in (trace_tag.text).replace('\n', '').split(',')]} \
                            for trace_tag in root.findall(doc_namespace + 'trace')]

    'Sort traces_all list by id to make searching for references faster'
    traces_all.sort(key=lambda trace_dict: int(trace_dict['id']))

    'Always 1st traceGroup is a redundant wrapper'
    traceGroupWrapper = root.find(doc_namespace + 'traceGroup')

    if traceGroupWrapper is not None:
        for traceGroup in traceGroupWrapper.findall(doc_namespace + 'traceGroup'):

            label = traceGroup.find(doc_namespace + 'annotation').text

            'traces of the current traceGroup'
            traces_curr = []
            for traceView in traceGroup.findall(doc_namespace + 'traceView'):

                'Id reference to specific trace tag corresponding to currently considered label'
                traceDataRef = int(traceView.get('traceDataRef'))

                'Each trace is represented by a list of coordinates to connect'
                single_trace = traces_all[traceDataRef]['coords']
                traces_curr.append(single_trace)

            traces_data.append({'label': label, 'trace_group': traces_curr})
    else:
        'Consider Validation data that has no labels'
        [traces_data.append({'trace_group': [trace['coords']]}) for trace in traces_all]
    sym = trace_data['label']
    trace_group = trace_data['trace_group']
    
    return traces_data

def get_min_coords(traces):
    x_coords = [coord[0] for coord in traces]
    y_coords = [coord[1] for coord in traces]
    min_x_coord=min(x_coords)
    min_y_coord=min(y_coords)
    max_x_coord=max(x_coords)
    max_y_coord=max(y_coords)
    return min_x_coord, min_y_coord, max_x_coord, max_y_coord
    
def get_image_hw(traces, padding=10):
    all_coor = []
    for trace in traces:   
         trace_group = trace['trace_group']
         for t in trace_group:
            all_coor.append(t)
    
    min_x, min_y, max_x, max_y = get_min_coords([item for sublist in all_coor for item in sublist])
    trace_height, trace_width = max_y - min_y, max_x - min_x
    print("height: ", trace_height)
    print("width: ", trace_width)
    if trace_height == 0:
        trace_height += 1
    if trace_width == 0:
        trace_width += 1     
    img_h = trace_height + padding*2
    img_w = trace_width + padding*2    

    return img_h, img_w, min_x, min_y

def shift_trace(sym_traces, min_x, min_y):
    # 相对位置 sym_traces: [[[],[]],[[],[]]]
    traces = [item for sub_list in sym_traces for item in sub_list]

    shifted_trace = [[int(coord[0]) - min_x, int(coord[1]) - min_y] for coord in traces]
    return shifted_trace

def center_pattern(traces, padding=5):
    center_trace = [[int(coord[0]) + padding, int(coord[1]) +padding] for coord in traces]
    return center_trace

def get_bbox(inkml_path, traces, txt_out_path, padding=10):
    img_name = os.path.splitext(os.path.basename(inkml_path))[0] 
    file_name = "%s.txt"%(img_name)
    file_path = os.path.join(txt_out_path, file_name) # 保存bbox文件路径
    fw = open(file_path, 'w')
    traces = get_sym(inkml_path)
    # 获取所有笔划坐标点 返回格式[[[],[]], [[],[]]]
    img_h, img_w, img_min, img_max = get_image_hw(traces, padding=padding)

    pattern_drawn = np.zeros(shape=(img_h, img_w), dtype=np.float32)
    for trace in traces:
        sym = trace['label']
        if sym=='\sqrt': # 不对根号进行分割
            continue
        fw.write(sym+'\t')
        sym_coor = trace['trace_group'] # [[[],[]],[[],[]]]这种格式，因为每个字符可能不止一个笔画
        # 相对左上角点的坐标
        relative_coor = shift_trace(sym_coor, img_min, img_max)
        
        # 算上填充部分，获取最终的坐标点位置
        coor = center_pattern(relative_coor, padding)

        # 生成txt文件
        min_x, min_y, max_x, max_y =  get_min_coords(coor)
        
        fw.write(str(min_x) + ' ' + str(min_y) + ' ' + str(max_x) + ' ' + str(max_y))
        fw.write('\n')
    
    fw.close()
    print("success generate {}".format(img_name))

if __name__ == "__main__":
    root_path = 'D:/DataSet/DataInkml/test2014'
    txt_out_path = 'txt/'
    img_out_path = 'offline/'
    dataset = 'test2014'
    img_out_path = os.path.join(img_out_path, dataset)
    txt_out_path = os.path.join(txt_out_path, dataset)
    if not os.path.exists(img_out_path):
        os.makedirs(img_out_path)
    if not os.path.exists(txt_out_path):
        os.makedirs(txt_out_path)

    inkml_list = os.listdir(root_path)
    for inkml in inkml_list:
        inkml = '18_em_1.inkml'
        inkml_path = os.path.join(root_path, inkml)
        get_bbox(inkml_path, img_out_path, txt_out_path)