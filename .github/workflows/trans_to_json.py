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
    containDict={'modifier':'adm','trait':'adq'}


    def __init__(self,info_dict,info_type,into_list_type='rows') -> None:

        self.dict=info_dict
        self.type=info_type
        self.list_type=into_list_type
        if into_list_type in info_dict:
            self.list=info_dict[into_list_type]


    def __getContainType(self,containInfo:str)->str:
        '''
        输入从dict中获取的type信息，输出一个三字母的type缩写.缩写规则在containDict中
        modifier -> adm; trait->adq
        '''
        for i in self.containDict:
            if i in containInfo:
                return self.containDict[i]

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
            match self.type:
                case "skl":
                    out_dict[i['id']]=self.getSklJson(i)
                case "adq":
                    out_dict[i['id']]=self.getAdqJson(i)
                case "adm":
                    out_dict[i['id']]=self.getAdmJson(i)
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

    def getSklJson(self,i:dict)->dict:
        '''
        self仅作为参数传递用
        i为主要输入，为一个dict，输出翻译dict
        '''
        newskilline={}
        #newskilline['id']=i['id']
        for skilL in self.sklList:
            if skilL in i:
                newskilline[skilL]=i[skilL]
            if 'prereqs' in i:
                newskilline['prereqs']=self.__getPrereqs(i['prereqs'])
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
    def getAdqJson(self,i:dict)->dict:
        '''
        self仅作为参数传递用
        i为主要输入，为一个dict，输出翻译dict
        '''
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
                        newmodifiersline['features']=self.__getfeature(ii['features'])
                    if 'children' in ii:
                        childrenAdm=infoDict(ii,self.__getContainType(ii['type']),into_list_type='children')
                        newmodifiersline['children']=childrenAdm.getChildren()
                    modifiersline.append(newmodifiersline)
                newadvine['modifiers']=modifiersline
                if 'features' in i:
                    newadvine['features']=self.__getfeature(i['features'])
        return(newadvine)
    def getAdmJson(self,i:dict)->dict:
        '''
        self仅作为参数传递用
        i为主要输入，为一个dict，输出翻译dict
        '''
        newadmline={}
        for admL in self.admList:
            if admL in i:
                newadmline[admL]=i[admL]
        if 'features' in i:
            newadmline['features']=self.__getfeature(i['features'])
        if ('children' in i ):
            childrenAdm=infoDict(i,self.__getContainType(i['type']),into_list_type='children')
            newadmline['children']=childrenAdm.getChildren()
        return(newadmline)
    
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
    new_json=Info.getChildren()
    outjson(new_json,mubiao_file)
    
en_to_file(sys.argv[1])
