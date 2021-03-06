'''
Author: sigmoid
Description: 生成中心掩码图片
Email: 595495856@qq.com
Date: 2021-01-18 21:02:37
LastEditTime: 2021-02-26 15:16:22
'''
import os
import cv2
import numpy as np

def gen_center_mask(input_path, images_path, output_path, r=0.5):
    """ 
        input_path: 存放bbox标签数据文件夹
        images_path: 对应离线图片的路径
        output_path: 输出掩码图像的路径
    """
    files = os.listdir(input_path)
    for fname in files:
        fname = '200922-947-80.txt'
        file_name = os.path.splitext(fname)[0]
        image_path = os.path.join(images_path, file_name+'.png') 
        img = cv2.imread(image_path, 0)
        mask_img = np.zeros(img.shape[:])
        mask_img_path = os.path.join(output_path, file_name+'_mask.png') # 掩码图片保存路径
        file_path = os.path.join(input_path, fname)
        with open(file_path, 'r') as fr:
            lines = fr.readlines()
            for l in lines:
                spt = l.split()
                sym = spt[0]
                minx, miny, maxx, maxy = spt[1:]
                minx = int(minx)
                miny = int(miny)
                maxx = int(maxx)
                maxy = int(maxy)
                w = maxx-minx
                h = maxy-miny
                xmin_m = round((minx+maxx-w*r)/2)
                ymin_m = round((miny+maxy-h*r)/2)
                xmax_m = round((minx+maxx+w*r)/2)
                ymax_m = round((miny+maxy+h*r)/2)
                mask_img[ymin_m:ymax_m+1, xmin_m:xmax_m+1] = 255
        cv2.imwrite(mask_img_path, mask_img)
        print('get {} success!'.format(file_name))
        
if __name__ == "__main__":
    input_path = 'bbox/train'
    images_path = 'offline/train'
    output_path = 'maskImage'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    gen_center_mask(input_path, images_path, output_path)    
