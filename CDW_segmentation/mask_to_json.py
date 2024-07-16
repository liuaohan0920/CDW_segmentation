#!/usr/bin/env python3
#功能批量将多个同类mask 转单个json 
 
import datetime
import json
import os
import io
import re
import fnmatch
import json
from PIL import Image
import numpy as np
from pycococreatortools import pycococreatortools
from PIL import Image
import base64
from base64 import b64encode
 
ROOT_DIR = 'hah'
IMAGE_DIR = os.path.join(ROOT_DIR, "pic")
ANNOTATION_DIR = os.path.join(ROOT_DIR, "mask")
 
def img_tobyte(img_pil):
# 类型转换 重要代码
    # img_pil = Image.fromarray(roi)
    ENCODING='utf-8'
    img_byte=io.BytesIO()
    img_pil.save(img_byte,format='PNG')
    binary_str2=img_byte.getvalue()
    imageData = base64.b64encode(binary_str2)
    base64_string = imageData.decode(ENCODING)
    return base64_string
 
 
annotation_files=os.listdir(ANNOTATION_DIR)
for annotation_filename in annotation_files:
    coco_output = {
        "version": "3.16.7",
        "flags": {},
   "fillColor": [255, 0,0,128],
  "lineColor": [0,255,0, 128],
  "imagePath": {},
  "shapes": [],
  "imageData": {} }
    
    print(annotation_filename)
    class_id = 1
    name = annotation_filename.split('.',3)[0]
    name1=name+'.jpg'
    coco_output["imagePath"]=name1 
 
    image = Image.open(IMAGE_DIR+'/'+ name1)
    imageData=img_tobyte(image)
    coco_output["imageData"]= imageData 
    
    binary_mask = np.asarray(Image.open(ANNOTATION_DIR+'/'+annotation_filename)
        .convert('1')).astype(np.uint8)
    segmentation=pycococreatortools.binary_mask_to_polygon(binary_mask, tolerance=3)
    #筛选多余的点集合
    for item in segmentation:
        if(len(item)>10):
 
            list1=[]
            
            for i in range(0, len(item), 2):
                list1.append( [item[i],item[i+1]])
            
            seg_info = {'points': list1, "fill_color":'null'  ,"line_color":'null' ,"label": "1", "shape_type": "polygon","flags": {}}
            coco_output["shapes"].append(seg_info)
    coco_output[ "imageHeight"]=binary_mask.shape[0]
    coco_output[ "imageWidth"]=binary_mask.shape[1]
    
 
    full_path='{}/'+name+'.json'
 
    with open( full_path.format(ROOT_DIR), 'w') as output_json_file:
        json.dump(coco_output, output_json_file)
 
 
      