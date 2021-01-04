'''
Author: sigmoid
Description: 生成不同尺寸的图片 
Email: 595495856@qq.com
Date: 2020-11-26 19:03:43
LastEditTime: 2021-01-04 21:12:51
'''
import os
import json, math
from io import StringIO

import cv2
from skimage.draw import line
from skimage.morphology import thin
import matplotlib.pyplot as plt
import scipy.misc
from PIL import Image
import numpy as np
import xml.etree.ElementTree as ET

def get_label(inkml_file_abs_path):
	lebel = ""
	tree = ET.parse(inkml_file_abs_path)
	root = tree.getroot()
	doc_namespace = "{http://www.w3.org/2003/InkML}"

	for child in root:
		if (child.tag == doc_namespace + 'annotation') and (child.attrib == {'type': 'truth'}):
			return child.text

def get_traces_data(inkml_file_abs_path):

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

    	return traces_data
    
def inkml2img(input_path, output_path):
	traces = get_traces_data(input_path)
	plt.gca().invert_yaxis()
	plt.gca().set_aspect('equal', adjustable='box')
	plt.gcf().set_facecolor('black')
	plt.axes().get_xaxis().set_visible(False)
	plt.axes().get_yaxis().set_visible(False)
	plt.axes().spines['top'].set_visible(False)
	plt.axes().spines['right'].set_visible(False)
	plt.axes().spines['bottom'].set_visible(False)
	plt.axes().spines['left'].set_visible(False)
	plt.axes().set_facecolor('black')
	for elem in traces:
		ls = elem['trace_group']
		for subls in ls:
			data = np.array(subls)
			# 判断一下shape, 如果是3, 取前两个
			if data.shape[1]==3 :
				data = data[:, :2]
			
			# data = [aug(item[0], item[1]) for item in data]
			x, y = zip(*data) 
			
			plt.plot(x, y, linewidth=3, color='white')
	plt.savefig(output_path, bbox_inches='tight', dpi=100, pad_inches=0.2)
	plt.gcf().clear()

if __name__ == "__main__":
    img_root = 'D:/DataSet/DataInkml/test2014'
    input_path = os.path.join(img_root, '505_em_47.inkml')
    output_path = "results/src.png"
    inkml2img(input_path, output_path)
