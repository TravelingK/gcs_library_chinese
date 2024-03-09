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

def  mergeDict(olddict,newdict):
    for i in olddict:
        if isinstance(olddict[i],list):
            num=len(olddict[i])
            for ii in range(num):
                
                if isinstance(ii,dict):
                    if i in newdict:
                        mergeDict(olddict[i][ii],newdict[i][ii])
                else:
                    if i in newdict:
                        while(len(olddict[i])>len(newdict[i])):
                            newdict[i].append({})
                        if isinstance(olddict[i][ii],dict):
                            olddict[i][ii].update(newdict[i][ii])
                        else:
                            olddict[i][ii]=newdict[i][ii]
            
        else:
            if i in newdict:
                if isinstance(olddict[i],dict):
                    olddict[i].update(newdict[i])
                else:
                    olddict[i]=newdict[i]
    return(olddict)

def zh_to_file(mobanwenjian):
    input_file=re.sub(r"master_library","master_library_en_json",mobanwenjian)
    mubiao_file=re.sub(".[a-z]{0,}$","_zh.skl",mobanwenjian)
    type=re.findall('(?<=.)[a-z]{0,}$',mobanwenjian)
    match type[0]:
        case "skl":
            input_file=re.sub(r".skl","_zh_Hans.json",input_file)
            mubiao_file=re.sub("gcs_master_library","gcs_chinese_library",mubiao_file)
            skilljson=getdict(input_file)
            mobanjson=getdict(mobanwenjian)
            for i in skilljson:
                for ii in mobanjson['rows']:
                    if (ii['id']==i):
                        #print(i)
                        ii=mergeDict(ii,skilljson[i])
    outjson(mobanjson,mubiao_file)
            

zh_to_file(sys.argv[1])
