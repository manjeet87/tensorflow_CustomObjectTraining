import xml.etree.ElementTree as ET
import pickle
import os
import glob
from os import listdir, getcwd
from os.path import join

sets=[('2012', 'train'), ('2012', 'val'), ('2007', 'train'), ('2007', 'val'), ('2007', 'test')]

classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
classes2 = ["buddha"]

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(img_xml, img_txt):
    in_file = open(img_xml)
    out_file = open(img_txt, 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes2 or int(difficult) == 1:
            continue
        cls_id = classes2.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()
print(wd)

def extract_filenames(folder_path):
    allfiles = glob.glob(os.path.join(folder_path, "*.xml"))
    return allfiles

folder_path = 'buddha_label'
imagexml_list = extract_filenames(folder_path)


if not os.path.exists(folder_path+'Text'):
    os.makedirs(folder_path+'Text')
#list_file = open('%s_%s.txt'%(year, image_set), 'w')
ftrain = open('train.txt','w')
ftest = open('test.txt','w')

i = 0
for img_xml in imagexml_list:
    i+=1
    if i<=70:
        ftrain.write('data\\obj\\' + img_xml.replace('xml','jpg').replace('_label','train')+'\n')
        img_txt = img_xml.replace('xml', 'txt').replace('_label', 'train')
    else:
        ftest.write('data\\obj\\'+ img_xml.replace('xml', 'jpg').replace('_label', 'test') + '\n')
        img_txt = img_xml.replace('xml','txt').replace('_label','test')
    #list_file.write('%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg\n'%(wd, year, image_id))
    convert_annotation(img_xml, img_txt)
#list_file.close()
ftrain.close()
ftest.close()