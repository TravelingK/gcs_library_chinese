#coding:utf-8
import json
import os

import re
import sys

def getdict(docname):
    """
    输入文件，读取json，输出dict
    """
    if not os.path.exists(docname):
        print(f"Warning: {docname} 不存在，跳过该文件。")
        return {}
    with open(docname, encoding="utf-8") as skill:
        skillline = skill.read()
        skilljson = json.loads(skillline)
        return skilljson


def outjson(nnskillline,docname):
    """
    将dict写入指定的文件
    """
    path=re.sub("[^/]{0,}$","",docname)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(docname,mode='+w') as skill:
        skillline=json.dumps(nnskillline,ensure_ascii=False)
        skill.write(skillline)


def  mergeDict(olddict:dict,newdict:dict)->dict:
    for i in olddict:
        if isinstance(olddict[i],dict) and (i in newdict):
            olddict[i]=mergeDict(olddict[i],newdict[i])
        elif isinstance(olddict[i],list) and (i in newdict):
            mDictlist=[]
            Dictnum=len(olddict[i])
            if (i=='children')or(i=='modifiers')or(i=='weapons'):
                for ti in olddict[i]:
                    for tii in newdict[i]:
                        if ti['id']==tii:
                            mDictlist.append(mergeDict(ti,newdict[i][tii]))
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
    type=re.findall('(?<=.)[a-z]{0,}$',mobanwenjian)[0]
    input_file=re.sub(f".{type}","_zh_Hans.json",input_file)
    mubiao_file=re.sub(".[a-z]{0,}$",f"_zh.{type}",mobanwenjian)
    mubiao_file=re.sub("gcs_master_library","gcs_chinese_library",mubiao_file)
    chinesejson=getdict(input_file)
    mobanjson=getdict(mobanwenjian)
    if (type=='calendar'):
        mobanjson=mergeDict(mobanjson,chinesejson)
    elif (type=='gct'):
        for i2 in chinesejson:
            for i in chinesejson[i2]:
                for ii in mobanjson[i2]:
                    if (ii['id']==i):
                        ii=mergeDict(ii,chinesejson[i2][i])
    elif (type=='body'):
        mobanjson['name']=chinesejson['name']
        location_list=[]
        for i in mobanjson['locations']:
            for ii in chinesejson['locations']:
                if (i['table_name']==ii):
                    location_list.append(mergeDict(i,chinesejson['locations'][ii]))
        mobanjson['locations']=location_list

    else:
        for i in chinesejson:
            for ii in mobanjson['rows']:
                if (ii['id']==i):
                    ii=mergeDict(ii,chinesejson[i])
    outjson(mobanjson,mubiao_file)
            

zh_to_file(sys.argv[1])
