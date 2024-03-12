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
    sklList=['name','tags','notes','specialization','vtt_notes']
    advList=['name','tags','notes','vtt_notes']
    admList=['name','tags','notes','vtt_notes']

    def __init__(self,info_dict,info_type) -> None:

        self.dict=info_dict
        self.type=info_type

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

    def getfeature(self,featureList:list):
        featuresline=[]
        featureInfoList=['name','usage','tags','specialization']
        for feature in featuresline:
            newfeaturesline={}
            for featureInfo in featureInfoList:
                if (featureInfo in feature) and ('qualifier' in feature[featureInfo]):
                    newfeaturesline[featureInfo]={}
                    newfeaturesline[featureInfo]['qualifier']=feature[featureInfo]['qualifier']
                    featuresline.append(newfeaturesline)
        return(featuresline)

    def getSklJson(self,i):
        newskilline={}
        #newskilline['id']=i['id']
        for skilL in self.sklList:
            if skilL in i:
                newskilline[skilL]=i[skilL]
            if 'prereqs' in i:
                newskilline['prereqs']=getPrereqs(i['prereqs'])
            if 'default' in i:
                newskilline['default']={}
                if 'type' in i['default']:
                    newskilline['default']['type']=i['default']['type']
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
        return newskilline
    def getAdqJson(self,i):
        newadvine={}
        for advlL in self.advList:
            if advlL in i:
                newadvine[advlL]=i[advlL] 
            if 'modifiers' in i:
                modifiersline=[]
                for ii in i['modifiers']:
                    newmodifiersline={}
                    if 'name' in ii:
                        newmodifiersline['name']=ii['name']
                    if 'notes' in ii:
                        newmodifiersline['notes']=ii['notes']
                    if 'situation' in ii:
                        newmodifiersline['situation']=ii['situation']
                    if 'specialization' in ii:
                        newmodifiersline['specialization']=ii['specialization']
                    if 'features' in ii:
                        newmodifiersline['features']=getfeature(ii['features'])
                    if 'children' in ii:
                        childrenline=[]
                        for iii in ii['children']:
                            newchildrenline={}
                            if ('name' in iii):
                                newchildrenline['name']=iii['name']
                            if ('notes' in iii):
                                newchildrenline['notes']=iii['notes']
                            childrenline.append(newchildrenline)
                        newmodifiersline['children']=childrenline
                    modifiersline.append(newmodifiersline)
                newadvine['modifiers']=modifiersline
                if 'features' in i:
                    newadvine['features']=getfeature(i['features'])
        return(newadvine)
    def getAdmJson(self,i):
        newadmline={}
        for admL in self.admList:
            if admL in i:
                newadmline[admL]=i[admL]
        if 'features' in i:
            newadmline['features']=getfeature(i['features'])
        if ('children' in i ) and ('container' in i["type"]):
            iiadmline={}
            for ii in i['children']:
                childrenAdm=infoDict(ii,self.type)
                iiadmline[ii['id']]=childrenAdm.getAdmJson(ii)
            newadmline['children']=iiadmline
        return(newadmline)


    def getJson(self):
        out_dict={}
        for i in self.dict['rows']:
            match self.type:
                case "skl":
                    out_dict[i['id']]=self.getSklJson(i)
                case "adq":
                    out_dict[i['id']]=self.getAdqJson(i)
                case "adm":
                    out_dict[i['id']]=self.getAdmJson(i)
        return out_dict
    
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
    Info=infoDict(raw_json,type[0])
    new_json=Info.getJson()
    outjson(new_json,mubiao_file)
    
en_to_file(sys.argv[1])
