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

def getPrereqs(prereqs:dict):
    dictprereqs={}
    PrereqsList=['name','notes',"specialization","qualifier"]
    if 'prereqs' in prereqs:
        endPrereqs=[]
        for i in prereqs['prereqs']:
            endPrereqs.append(getPrereqs(i))
        dictprereqs['prereqs']=endPrereqs
    else:
        for i in PrereqsList:
            if (i in prereqs)and('qualifier' in prereqs[i]):
                dictprereqs[i]={}
                dictprereqs[i]['qualifier']=prereqs[i]['qualifier']
    return(dictprereqs)


def en_to_file(input_file):
    """
    .adm 优劣势限制因子
    .adq 优劣势
    .ancestry 先祖：设定与种族搭配的名称、发色等特质的随机表
    .attr 角色的属性预设
    .body 躯体预设
    .calendar 日历预设
    .eqm 装备限制因子
    .eqp 装备物品
    .gcs 角色卡
    .gct 种族/元特质
    .md markdown文件
    .names 随机人名
    .not 规则
    .skl 技能
    .spl 法术
    """
    mubiao_file=re.sub(".[a-z]{0,}$","_en.json",input_file)
    mubiao_file=re.sub("gcs_master_library","gcs_master_library_en_json",mubiao_file)
    type=re.findall('(?<=.)[a-z]{0,}$',input_file)
    raw_json=getdict(input_file)
    print(input_file,mubiao_file)
    new_json={}
    match type[0]:
        case "skl":
            sklList=['name','tags','notes','specialization']
            for i in raw_json['rows']:
                newskilline={}
                #newskilline['id']=i['id']
                for skilL in sklList:
                    if skilL in i:
                        newskilline[skilL]=i[skilL]
                if 'prereqs' in i:
                    newskilline['prereqs']=getPrereqs(i['prereqs'])
                if 'default' in i:
                    newskilline['default']={}
                    if 'name' in i['default']:
                        newskilline['default']['name']=i['default']['name']
                if 'defaults' in i:
                    defaultline=[]
                    for ii in i['defaults']:
                        nnewskilline={}
                        if 'name' in ii:
                            nnewskilline['name']=ii['name']
                        if 'specialization' in ii:
                            nnewskilline['specialization']=ii['specialization']
                        defaultline.append(nnewskilline)
                    newskilline['defaults']=defaultline
                #print(newskilline)
                new_json[i['id']]=newskilline
        case "adq":
                new_json[i['id']]=newskilline
    outjson(new_json,mubiao_file)
    
en_to_file(sys.argv[1])
