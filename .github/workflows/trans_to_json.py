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

class infoDict:
    JsonList=['name','tags','notes','specialization','vtt_notes','situation']


    def __init__(self,info_dict,into_list_type='rows') -> None:

        self.dict=info_dict
        #self.type=info_type
        self.list_type=into_list_type
        if into_list_type in info_dict:
            self.list=info_dict[into_list_type]


    def __getPrereqs(self,prereqs:dict):
        dictprereqs={}
        PrereqsList=['name','notes',"specialization","qualifier"]
        if 'prereqs' in prereqs:
            endPrereqs=[]
            for i in prereqs['prereqs']:
                endPrereqs.append(self.__getPrereqs(i))
            dictprereqs['prereqs']=endPrereqs
        else:
            for i in PrereqsList:
                if (i in prereqs)and('qualifier' in prereqs[i]):
                    dictprereqs[i]={}
                    dictprereqs[i]['qualifier']=prereqs[i]['qualifier']
        return(dictprereqs)
    def getChildren(self)->dict:
        """
        输入一个self.list列表，列表中的每一项为带ID的字典；输出一个dict，dict中的每个key为ID，其值为翻译的json
        get方法由type决定，针对contain需要上级判断type类型后输入
        """
        out_dict={}
        for i in self.list:
            out_dict[i['id']]=self.getJson(i)
        return out_dict


    def __getfeature(self,featureList:list):
        featuresline=[]
        featureInfoList=['name','usage','tags','specialization']
        for feature in featureList:
            newfeaturesline={}
            for featureInfo in featureInfoList:
                if (featureInfo in feature) and ('qualifier' in feature[featureInfo]):
                    newfeaturesline[featureInfo]={}
                    newfeaturesline[featureInfo]['qualifier']=feature[featureInfo]['qualifier']
                    featuresline.append(newfeaturesline)
        return(featuresline)
    
    def getJson(self,i:dict)->dict:
        newjsonline={}
        for admL in self.JsonList:
            if admL in i:
                newjsonline[admL]=i[admL]
        if 'features' in i:
            newjsonline['features']=self.__getfeature(i['features'])
        if 'children' in i :
            childrenJson=infoDict(i,into_list_type='children')
            newjsonline['children']=childrenJson.getChildren()
        if 'modifiers' in i:
            JsonModifiersline=['modifiers']
            for ii in i['modifiers']:
                childrenJson=infoDict(i)
                newjsonlinemodifiers=childrenJson.getJson(ii)
                JsonModifiersline.append(newjsonlinemodifiers)
            newjsonline['modifiers']=JsonModifiersline
        if 'features' in i:
            newjsonline['features']=self.__getfeature(i['features'])
        if 'prereqs' in i:
            newjsonline['prereqs']=self.__getPrereqs(i['prereqs'])
        if 'default' in i:
            newjsonline['default']={}
            if 'name' in i['default']:
                newjsonline['default']['name']=i['default']['name']
        if 'defaults' in i:
            defaultline=[]
            for ii in i['defaults']:
                nnewskilline={}
                if 'name' in ii:
                    nnewskilline['name']=ii['name']
                if 'specialization' in ii:
                    nnewskilline['specialization']=ii['specialization']
                defaultline.append(nnewskilline)
            newjsonline['defaults']=defaultline
        return(newjsonline)
    
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
    raw_json=getdict(input_file)
    Info=infoDict(raw_json)
    new_json=Info.getChildren()
    outjson(new_json,mubiao_file)
    
en_to_file(sys.argv[1])
