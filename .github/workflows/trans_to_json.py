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


def en_to_file(shuru_file,type=0):
    mubiao_file=re.sub(".[a-z]{0,}$","_en.json",shuru_file)
    mubiao_file=re.sub("gcs_master_library","gcs_master_library_en_json",mubiao_file)
    skilljson=getdict(shuru_file)
    newskill=[]
    nnewskill={}
    for i in skilljson['rows']:
        
        newskilline={}
        #newskilline['id']=i['id']
        newskilline['name']=i['name']
        if 'tags' in i:
            newskilline['tags']=i['tags']
        if 'specialization' in i:
            newskilline['specialization']=i['specialization']
        if 'notes' in i:
            newskilline['notes']=i['notes']
        if 'defaults' in i:
            defaultline=[]
            for ii in i['defaults']:
                nnewskilline={}
                nnewskilline['type']=ii['type']
                if 'name' in ii:
                    nnewskilline['name']=ii['name']
                if 'specialization' in ii:
                    nnewskilline['specialization']=ii['specialization']
                defaultline.append(nnewskilline)
            newskilline['defaults']=defaultline
        nnewskill[i['id']]=newskilline
    
    outjson(nnewskill,mubiao_file)
en_to_file(sys.argv[1])

