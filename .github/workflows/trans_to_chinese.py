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


def  mergeDict(olddict:dict,newdict:dict)->dict:
    for i in olddict:
        if isinstance(olddict[i],list):
            num=len(olddict[i])
            if i in newdict:
                while(len(olddict[i])>len(newdict[i])):
                    newdict[i].append({})
            for ii in range(num):
                if isinstance(olddict[i][ii],dict):
                    if (i in newdict) and (i != 'children'):
                        mergeDict(olddict[i][ii],newdict[i][ii])
                    elif (i == 'children'):
                        for ti in olddict[i]:
                            for tii in newdict[i]:
                                print(ti,newdict[i][tii])
                                if (ti['id']==tii):
                                    ti=mergeDict(ti,newdict[i][tii])
                else:
                    if i in newdict:
                        if isinstance(olddict[i][ii],dict):
                            olddict[i][ii].update(newdict[i][ii])
                        else:
                            olddict[i][ii]=newdict[i][ii]
        elif isinstance(olddict[i],dict):
            for ii in olddict[i]:
                if (i in newdict) and ( ii in newdict[i]):

                    mergeDict(olddict[i],newdict[i])
        else:
            if i in newdict:
                    olddict[i]=newdict[i]
    return(olddict)






def zh_to_file(mobanwenjian):  
    input_file=re.sub(r"master_library","master_library_en_json",mobanwenjian)
    type=re.findall('(?<=.)[a-z]{0,}$',mobanwenjian)
    match type[0]:
        case "skl":
            input_file=re.sub(r".skl","_zh_Hans.json",input_file)
            mubiao_file=re.sub(".[a-z]{0,}$","_zh.skl",mobanwenjian)
            mubiao_file=re.sub("gcs_master_library","gcs_chinese_library",mubiao_file)
            chinesejson=getdict(input_file)
            mobanjson=getdict(mobanwenjian)
            for i in chinesejson:
                for ii in mobanjson['rows']:
                    if (ii['id']==i):
                        ii=mergeDict(ii,chinesejson[i])
        case 'adq':
            input_file=re.sub(r".adq","_zh_Hans.json",input_file)
            mubiao_file=re.sub(".[a-z]{0,}$","_zh.adq",mobanwenjian)
            mubiao_file=re.sub("gcs_master_library","gcs_chinese_library",mubiao_file)
            chinesejson=getdict(input_file)
            mobanjson=getdict(mobanwenjian)
            for i in chinesejson:
                for ii in mobanjson['rows']:
                    if (ii['id']==i):
                        ii=mergeDict(ii,chinesejson[i])
        case 'adm':
            input_file=re.sub(r".adm","_zh_Hans.json",input_file)
            mubiao_file=re.sub(".[a-z]{0,}$","_zh.adm",mobanwenjian)
            mubiao_file=re.sub("gcs_master_library","gcs_chinese_library",mubiao_file)
            chinesejson=getdict(input_file)
            mobanjson=getdict(mobanwenjian)
            for i in chinesejson:
                for ii in mobanjson['rows']:
                    if (ii['id']==i):
                        ii=mergeDict(ii,chinesejson[i])
    outjson(mobanjson,mubiao_file)
            

zh_to_file(sys.argv[1])
