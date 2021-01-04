'''
Author: sigmoid
Description: 
Email: 595495856@qq.com
Date: 2021-01-04 19:37:22
LastEditTime: 2021-01-04 21:15:23
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

def parse_inkml(inkml_file_abs_path):
    """ 返回二维坐标 """
    if inkml_file_abs_path.endswith('.inkml'):
        tree = ET.parse(inkml_file_abs_path)
        root = tree.getroot()
        doc_namespace = "{http://www.w3.org/2003/InkML}"
        'Stores traces_all with their corresponding id'
	    # MM: multiple all integers and floats by 10K
        traces_all_list = [{'id': trace_tag.get('id'),
    					'coords': [[round(float(axis_coord)) if float(axis_coord).is_integer() else round(float(axis_coord) * 10000) \
    									for axis_coord in coord[1:].split(' ')] if coord.startswith(' ') \
    								else [round(float(axis_coord)) if float(axis_coord).is_integer() else round(float(axis_coord) * 10000) \
    									for axis_coord in coord.split(' ')] \
    							for coord in (trace_tag.text).replace('\n', '').split(',')]} \
    							for trace_tag in root.findall(doc_namespace + 'trace')]

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
    
def get_min_coords(traces):
    x_coords = [coord[0] for coord in traces]
    y_coords = [coord[1] for coord in traces]
    min_x_coord=min(x_coords)
    min_y_coord=min(y_coords)
    max_x_coord=max(x_coords)
    max_y_coord=max(y_coords)
    return min_x_coord, min_y_coord, max_x_coord, max_y_coord

'shift pattern to its relative position'
def shift_trace(traces, min_x, min_y):
    shifted_trace = [[coord[0] - min_x, coord[1] - min_y] for coord in traces]
    return shifted_trace

'Scaling: Interpolates a pattern so that it fits into a box with specified size'
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

def inkml2img(input_path, output_path):
    traces = parse_inkml(input_path)
    selected_tr = get_traces_data(traces)
    im = convert_to_imgs(selected_tr)
    imsave(output_path, im)
    
if __name__ == "__main__":
    # inkml_file_abs_path = "D:\毕设\数据集\CROHME2019\onlineRec\MainTask_formula\\train\INKMLs\Train_2014\\3_em_18.inkml" # 136*73 722*308
    inkml_file_abs_path = "D:/DataSet/DataInkml/test2014/505_em_47.inkml" # 74*59 202*144

    traces = parse_inkml(inkml_file_abs_path) 

    selected_tr = get_traces_data(traces)

    im = convert_to_imgs(selected_tr)
    # im = ndimage.gaussian_filter(im, sigma=(.5, .5), order=0)
    outImagePath = os.path.join("results", "504.png")
    imsave(outImagePath, im)
    print("generate image success!")