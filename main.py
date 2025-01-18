import cv2
from PIL import Image
import imagehash
import os
import tkinter as tk
from tkinter import filedialog
import numpy as np
from configparser import ConfigParser

#解决cv.imread无法读取中文路径
def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
    return cv_img

# 获取选择文件路径
def file_choose():
    # 实例化
    root = tk.Tk()
    root.withdraw()
    # 获取文件夹路径
    f_path = filedialog.askopenfilename()
    # 返回文件路径
    return f_path

#读取ini文件信息
conf = ConfigParser()
conf.read('./config.ini')

# 判断操作 空路径则储存Hash
if_filepath = file_choose()
if if_filepath != '':
    # 读取图像并计算哈希值
    img1 = cv_imread(if_filepath)
    img1 = Image.fromarray(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    hash1 = imagehash.phash(img1)

    with open(conf['data']['hash_path'], 'r') as f:
        lines = f.readlines()
        for s in lines:
            hash_l = s.split('=')
            hash_str = hash_l[1].replace('\n','')
            if str(hash1) == str(hash_str):
                print(hash_l[0])
#储存Hash值
else:
    # 遍历文件夹内所有文件
    image_format = ['.png','.jpg','.jpeg','.webp','.tiff','.bmp','.heif','.raw']
    r_d_path_w = conf['data']['image_path']
    paths2 = os.walk(r_d_path_w)

    with open(conf['data']['hash_path'], 'w+') as f:
        for path, dir_lst, file_lst in paths2:
            for file_name in file_lst:
                f_e = os.path.splitext(file_name)[1] # 文件扩展名
                for format in image_format:
                    if f_e == format:
                        img_w = cv_imread(os.path.join(path, file_name))
                        img_w = Image.fromarray(cv2.cvtColor(img_w, cv2.COLOR_BGR2RGB))
                        hash_w = imagehash.phash(img_w)
                        str1 = os.path.join(path, file_name)
                        str2 = '='
                        str3 = str(hash_w)
                        str_w = str1 + str2 + str3 + '\n'
                        lines2 = f.readlines()
                        for j in lines2:
                            if str_w == j:
                                break
                        f.write(str_w)