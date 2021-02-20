'''
Author: sigmoid
Description: 最终版
Email: 595495856@qq.com 
Date: 2021-01-16 21:35:37
LastEditTime: 2021-02-04 22:07:31
'''
import os, json, math
from math import cosh
from io import StringIO

from skimage.draw import line
from skimage.io import imread, imsave
import scipy.ndimage as ndimage
import pickle
import xml.etree.ElementTree as ET
import numpy as np

import warnings

def parse_inkml(inkml_file_abs_path):
    """ 返回二维坐标 """
    if inkml_file_abs_path.endswith('.inkml'):
        tree = ET.parse(inkml_file_abs_path)
        root = tree.getroot()
        doc_namespace = "{http://www.w3.org/2003/InkML}"
        'Stores traces_all with their corresponding id'
        traces_all_list = []
        for trace_tag in root.findall(doc_namespace+'trace'):
            trace_dict = {}
            trace_dict.update({'coords': []})
            trace_dict.update({'id': trace_tag.get('id')})
            for coord in (trace_tag.text).replace('\n', '').split(','):

                if coord.startswith(' '):   
                    coord_list = []           
                    for axis_coord in coord[1:].split(' '):
                        if float(axis_coord).is_integer() :#or float(axis_coord)>8 :
                            axis_coord = round(float(axis_coord))
                        else :
                            axis_coord = round(float(axis_coord)*10000)
                        coord_list.append(axis_coord)
                else:
                    coord_list = []
                    for axis_coord in coord.split(' '):
                        if float(axis_coord).is_integer() :#or float(axis_coord)>8:
                            axis_coord = round(float(axis_coord))
                        else :
                            axis_coord = round(float(axis_coord)*10000)
                        coord_list.append(axis_coord)
                trace_dict['coords'].append(coord_list)
            traces_all_list.append(trace_dict)
        'convert in dictionary traces_all  by id to make searching for references faster'
        traces_all = {}
        for t in traces_all_list:
            traces_all[t["id"]] = t["coords"]
        return traces_all
    else:
        print('File ', inkml_file_abs_path, ' does not exist !')
        return {}

def get_traces_data(traces_dict, id_set = None):
    'Accumulates traces_data of the inkml file'
    traces_data_curr_inkml=[]
    if id_set == None:
        id_set = traces_dict.keys()
    # this range is specified by values specified in the lg file
    for i in id_set: # use function for getting the exact range
        traces_data_curr_inkml.append(traces_dict[i])
    return traces_data_curr_inkml

def get_min_max_coords(traces):
    traces = [item for sublist in traces for item in sublist]
    x_coords = [coord[0] for coord in traces]
    y_coords = [coord[1] for coord in traces]
    min_x_coord=min(x_coords)
    min_y_coord=min(y_coords)
    max_x_coord=max(x_coords)
    max_y_coord=max(y_coords)
    return min_x_coord, min_y_coord, max_x_coord, max_y_coord

def get_min_coords(traces):
    x_coords = [coord[0] for coord in traces]
    y_coords = [coord[1] for coord in traces]
    min_x_coord=min(x_coords)
    min_y_coord=min(y_coords)
    max_x_coord=max(x_coords)
    max_y_coord=max(y_coords)
    return min_x_coord, min_y_coord, max_x_coord, max_y_coord

def shift_trace(traces, min_x, min_y):
    shifted_trace = [[coord[0] - min_x, coord[1] - min_y] for coord in traces]
    return shifted_trace

def scaling(traces, scale_factor=1.0):
    interpolated_trace = []
    'coordinate convertion to int type necessary'
    interpolated_trace = [[round(coord[0] * scale_factor), round(coord[1] * scale_factor)] for coord in traces]
    return interpolated_trace

def center_pattern(traces, padding=5):
    return shift_trace(traces, min_x= -padding, min_y= -padding)

def draw_pattern(traces, pattern_drawn, box_axis_size):
    ' SINGLE POINT TO DRAW '
    if len(traces) == 1:
            x_coord = traces[0][0]
            y_coord = traces[0][1]
            pattern_drawn[y_coord, x_coord] = 0.0 #0 means black
    else:
        ' TRACE HAS MORE THAN 1 POINT '
        'Iterate through list of traces endpoints'
        for pt_idx in range(len(traces) - 1):
                'Indices of pixels that belong to the line. May be used to directly index into an array'
                linesX = linesY = []
                # 返回直线上点的所有坐标
                oneLineX, oneLineY = line(r0=traces[pt_idx][1], c0=traces[pt_idx][0],
                                   r1=traces[pt_idx + 1][1], c1=traces[pt_idx + 1][0])
                 
                # 这里对笔画进行了加粗
                linesX = np.concatenate(
                    [ oneLineX, oneLineX, oneLineX+1, oneLineX+1])
                linesY = np.concatenate(
                    [ oneLineY+1, oneLineY, oneLineY, oneLineY+1])

                # linesX = np.concatenate(
                #     [ oneLineX, oneLineX, oneLineX+1])
                # linesY = np.concatenate(
                #     [ oneLineY+1, oneLineY, oneLineY])
                    
                linesX[linesX<0] = 0
                linesX[linesX>=box_axis_size[1]] = box_axis_size[1]-1

                linesY[linesY<0] = 0
                linesY[linesY>=box_axis_size[0]] = box_axis_size[0]-1
                pattern_drawn[linesX, linesY] = 1.0

    return pattern_drawn

def convert_to_imgs(traces_data, padding=10): 
    min_x, min_y, max_x, max_y = get_min_coords([item for sublist in traces_data for item in sublist])
    
    trace_height, trace_width = max_y - min_y, max_x - min_x
    print("height: ", trace_height)
    print("width: ", trace_width)
    if trace_height == 0:
        trace_height += 1
    if trace_width == 0:
        trace_width += 1
        
    img_h = trace_height + padding*2
    img_w = trace_width + padding*2
    
    pattern_drawn = np.zeros(shape=(img_h, img_w), dtype=np.float32)
    scale_factor = 1.0
    # 如果没有笔迹坐标，生成纯黑色图片
    if len(traces_data) == 0:
        return np.matrix(pattern_drawn * 255, np.uint8)

    for traces_all in traces_data:
        'shift pattern to its relative position'
        shifted_trace= shift_trace(traces_all, min_x, min_y)
        'Interpolates a pattern so that it fits into a box with specified size'
        'method: LINEAR INTERPOLATION'
        # try:
        #     scaled_trace = scaling(shifted_trace, scale_factor)
        # except Exception as e:
        #     print(e)
        #     print('This data is corrupted - skipping.')
        box_axis_size = [img_w, img_h]
        'Get min, max coords once again in order to center scaled patter inside the box'
        centered_trace = center_pattern(shifted_trace, padding)
        'Center scaled pattern so it fits a box with specified size'
        
        pattern_drawn = draw_pattern(centered_trace, pattern_drawn, box_axis_size=box_axis_size)
    
    return np.matrix(pattern_drawn * 255, np.uint8)

def shrinkPixels(traces):
    minx = 2**31
    miny = 2**31
    for trace in traces: # 笔画
        for p in trace: # 笔画中的一个点
            minx = min(minx, p[0])
            miny = min(miny, p[1])
    for trace in traces:
        for idx in range(len(trace)):
            trace[idx] = [trace[idx][0]-minx, trace[idx][1]-miny]
    return traces

def removeRedundantPoints(traces_all):
    new_stroke_data = []
    for stroke in traces_all:
        new_stroke = [stroke[0]]
        # add the stroke if it only contains one point
        if len(stroke) == 1:
            new_stroke_data.append(new_stroke)
            continue
        if (new_stroke[-1][1] - stroke[1][1]) == 0: 
            last_cos = 100
        else:
            last_cos = - cosh((new_stroke[-1][0] - stroke[1][0]) / (new_stroke[-1][1] - stroke[1][1]))

        for i in range(1, len(stroke)-1):
            # save the stroke if it represents a large euclidean change
            dx = new_stroke[-1][0] - stroke[i][0]
            dy = new_stroke[-1][1] - stroke[i][1]
            if dy == 0: 
                this_cos = 100
            else: 
                this_cos = cosh(dx/dy)
            if dx**2 + dy **2 > 100 or abs(this_cos - last_cos) > 0.2:
                new_stroke.append(stroke[i])
            last_cos = this_cos

        new_stroke.append(stroke[-1])
        for i in range(len(stroke)):
            new_v = (int(stroke[i][0]), int(stroke[i][1]))
            stroke[i] = new_v
        new_stroke_data.append(new_stroke)
    return new_stroke_data

def get_projection(p1, p2):
    """
        输入:坐标点
        输出:两个坐标点的距离以及在x轴和y轴的投影长度
    """
    x1, y1 = p1[:]
    x2, y2 = p2[:]
    lenL = math.sqrt((x2-x1)**2+(y2-y1)**2)
    pxL  = (lenL*(x1+x2))/2
    # pxL = abs(x1-x2)
    # pyL = abs(y1-y2)
    pyL  = (lenL*(y1+y2))/2
    return lenL, pxL, pyL

def get_param(traces):
    """
        输入:同一个笔划的坐标点
        格式:traces: [[], [], []]
        输出:归一化参数
    """
    lenL_sum = 0
    pxL_sum  = 0
    pyL_sum  = 0
    for i in range(1, len(traces)):
        lenL, pxL, pyL = get_projection(traces[i-1], traces[i])
        lenL_sum += lenL
        pxL_sum  += pxL
        pyL_sum  += pyL
    ux = pxL_sum/lenL_sum
    uy = pyL_sum/lenL_sum

    dxL_sum = 0
    for i in range(1, len(traces)):
        lenL, _, _ = get_projection(traces[i-1], traces[i])
        x1, y1 = traces[i-1][:]
        x2, y2 = traces[i][:]
        dxL_sum += (((x2-ux)**2+(x1-ux)**2+(x1-ux)*(x2-ux))*lenL)/3
    sx = math.sqrt(dxL_sum/lenL_sum)
    return ux, uy, sx
    
def get_distance(traces):
    """
        正则化相同笔划
        traces: [[], [], []]
    """
    new_traces = []
    DL_sum = 0
    for trace in traces:
        dl_sum = 0
        for i in range(1, len(trace)):
            x1, y1 = trace[i-1][:2]
            x2, y2 = trace[i][:2]
            dl_sum += math.sqrt((x2-x1)**2+(y2-y1)**2)
        dl_sum /= 30    
        DL_sum += dl_sum
    DL_sum /= len(traces)
    print(DL_sum)
    return DL_sum/2

def distance_normalize(traces):
    distance = get_distance(traces)
    new_traces = []
    for trace in traces:
        new_trace = []
        for p in trace:
            new_x = p[0]/distance
            new_y = p[1]/distance
            new_trace.append([new_x, new_y])
        new_traces.append(new_trace)
    return new_traces

def sym_id_traces(inkml_file_abs_path):
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
    sym_id = {} # 符号对应的id
    if traceGroupWrapper is not None:
        for traceGroup in traceGroupWrapper.findall(doc_namespace + 'traceGroup'):
            try:
                label = traceGroup.find(doc_namespace + 'annotationXML').get('href')
            except :
                label =  traceGroup.find(doc_namespace + 'annotation').text+'_1'
            # .get('traceDataRef')
            sym_id[label] = []
            'traces of the current traceGroup'
            traces_curr = []
            for traceView in traceGroup.findall(doc_namespace + 'traceView'):

                'Id reference to specific trace tag corresponding to currently considered label'
                traceDataRef = int(traceView.get('traceDataRef'))

                'Each trace is represented by a list of coordinates to connect'
                single_trace = traces_all[traceDataRef]['coords']
                trace_id = traces_all[traceDataRef]['id']
                sym_id[label].append(trace_id)
                traces_curr.append(single_trace)

            traces_data.append({'label': label, 'trace_group': traces_curr})
    else:
        'Consider Validation data that has no labels'
        [traces_data.append({'trace_group': [trace['coords']]}) for trace in traces_all]
    return sym_id     

def get_bbox(inkml_path, sym_dict, img_h, img_w, min_r, min_c, txt_out_path, padding=10):
    img_name = os.path.splitext(os.path.basename(inkml_path))[0] 
    file_name = "%s.txt"%(img_name)
    file_path = os.path.join(txt_out_path, file_name) # 保存bbox文件路径
    fw = open(file_path, 'w')
    for label in sym_dict.keys():
        sym = label
        if sym == '\sqrt':
            continue
        fw.write(sym+'\t')
        sym_coor = sym_dict[label]
        relative_coor = shift_trace([item for sublist in sym_coor for item in sublist], min_r, min_c)
        coor = center_pattern(relative_coor, padding)
        min_x, min_y, max_x, max_y =  get_min_coords(coor)
        
        fw.write(str(min_x) + ' ' + str(min_y) + ' ' + str(max_x) + ' ' + str(max_y))
        fw.write('\n')
    fw.close()
    print("success generate {}".format(img_name))

def inkml2img(inkml_path, outImagePath):
    sym_id = sym_id_traces(inkml_path)
    traces_all_dict = parse_inkml(inkml_path)
    traces = get_traces_data(traces_all_dict)
    traces = distance_normalize(traces)
    traces = [[[round(v) for v in p] for p in trace] for trace in traces]

    im = convert_to_imgs(traces)    
    imsave(outImagePath, im)  

def inkml2img_getbbox(inkml_path, outImagePath, txt_out_path):
    sym_id = sym_id_traces(inkml_path)
    traces_all_dict = parse_inkml(inkml_path)
    traces = get_traces_data(traces_all_dict)

    traces = distance_normalize(traces)
    traces = [[[round(v) for v in p] for p in trace] for trace in traces]
    # 生成label对应的trace
    sym_dict = {}
    labels = sym_id.keys()
    for label in labels:
        trace_id_list = sym_id[label]
        sym_trace_list = []
        for id_ in trace_id_list:
            sym_trace_list.append(traces[int(id_)])
        if label in sym_dict.keys():
            sym_dict[label].append(sym_trace_list)
        else:
            sym_dict.update({label:sym_trace_list})
    im = convert_to_imgs(traces)    
    img_h, img_w = im.shape[:2]
    min_r, min_c, _, _ = get_min_coords([item for sublist in traces for item in sublist]) 
    get_bbox(inkml_path, sym_dict, img_h, img_w, min_r, min_c, txt_out_path)
    imsave(outImagePath, im)        
    
if __name__ == "__main__":
    inkml_path = 'D:/DataSet/DataInkml/test2016/UN_463_em_912.inkml'
    # 获取坐标点并进行归一化
    traces_all_dict = parse_inkml(inkml_path)
    traces = get_traces_data(traces_all_dict)
    traces = distance_normalize(traces)
    traces = [[[round(v) for v in p] for p in trace] for trace in traces]

    im = convert_to_imgs(traces)    
    outImagePath = os.path.join("examples", "UN_463_em_912.png")
    imsave(outImagePath, im)
    print("generate image success!") 