#coding:utf-8
import json
import os
import string

import re
import sys



def getdict(docname):
    """
    1输入文件，读取json，输出dict
    """
    with open(docname) as skill:
        skillline=skill.read()
        skilljson=json.loads(skillline)
        return(skilljson)
def outjson(nnskillline,docname):
    """
    将dict写入指定的文件
    """
    path=re.sub("[^/]{0,}$","",docname)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(docname,mode='+w') as skill:
        skillline=json.dumps(nnskillline)
        skill.write(skillline)



def zh_to_file(shuru_file,type=0):
    mobanwenjian=re.sub(r"master_library_en_json","master_library",shuru_file)
    mobanwenjian=re.sub(r"_zh_Hans.json",".skl",mobanwenjian)
    mubiao_file=re.sub(".[a-z]{0,}$","zh.skl",mobanwenjian)
    mubiao_file=re.sub("gcs_master_library","gcs_chinese_library",mobanwenjian)
    skilljson=getdict(shuru_file)
    mobanjson=getdict(mobanwenjian)
    print(mobanjson)
    print(skilljson)
    for i in skilljson:
        for ii in mobanjson['rows']:
            if (ii['id']==i):
                #print(i)
                ii.update(skilljson[i])
    outjson(mobanjson,mubiao_file)
            

zh_to_file(sys.argv[1])
