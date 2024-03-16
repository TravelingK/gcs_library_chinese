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
        if isinstance(olddict[i],dict) and (i in newdict):
            olddict[i]=mergeDict(olddict[i],newdict[i])
        elif isinstance(olddict[i],list) and (i in newdict):
            mDictlist=[]
            Dictnum=len(olddict[i])
            if (i=='children'):
                for ti in olddict[i]:
                    for tii in newdict[i]:
                        if ti['id']==tii:
                            mDictlist.append(mergeDict(ti,newdict[i][tii]))
                            olddict[i]=mDictlist
            elif (i=='modifiers'):
                for ti in olddict[i]:
                    for tii in newdict[i]:
                        for tiii in tii:
                            if ti['id']==tiii:
                                mDictlist.append(mergeDict(ti,tii[tiii]))
                                olddict[i]=mDictlist
            elif isinstance(olddict[i][0],dict):
                while(Dictnum>len(newdict[i])):
                    newdict[i].append({}) 
                for ii in range(Dictnum):
                    olddict[i][ii]=mergeDict(olddict[i][ii],newdict[i][ii])
            elif len(newdict[i])>0:
                for ii in range(len(newdict[i])):
                    olddict[i][ii]=newdict[i][ii]
        elif isinstance(olddict[i],str) and (i in newdict):
            olddict[i]=newdict[i]
    return(olddict)


def zh_to_file(mobanwenjian):  
    input_file=re.sub(r"master_library","master_library_en_json",mobanwenjian)
    type=re.findall('(?<=.)[a-z]{0,}$',mobanwenjian)
    input_file=re.sub(f".{type[0]}","_zh_Hans.json",input_file)
    mubiao_file=re.sub(".[a-z]{0,}$",f"_zh.{type[0]}",mobanwenjian)
    mubiao_file=re.sub("gcs_master_library","gcs_chinese_library",mubiao_file)
    chinesejson=getdict(input_file)
    mobanjson=getdict(mobanwenjian)
    for i in chinesejson:
        for ii in mobanjson['rows']:
            if (ii['id']==i):
                ii=mergeDict(ii,chinesejson[i])
    outjson(mobanjson,mubiao_file)

            

zh_to_file(sys.argv[1])
