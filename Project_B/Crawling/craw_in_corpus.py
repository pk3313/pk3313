import json
from msilib.schema import Verb
from torch import equal
import urllib3
import os
import csv

verb =['벗다','하다','박다','사다','받다','주다','타다','먹다','접다','치다','잡다']
wordlist =[]
VerbList=[]
addr = 'D:/이어달리기사업/vscode/준비중/그림일기/'
fileList=os.listdir(addr)
openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU" # 언어 분석 기술(문어)
openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU_spoken" # 언어 분석 기술(구어)
accessKey = "31e6f9bb-3afc-48ba-90d8-fd988cf15f2e"
analysisCode = "ner"
analysisCode_verb= "morp"
final =[]

def Verb_def(doc):
    requestJson = {
        "access_key": accessKey,
        "argument": {
            "text": doc,
            "analysis_code": analysisCode_verb}}
    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson))
    responseToJson = json.loads(str(response.data,"utf-8"))
    for i in range(len(responseToJson["return_object"]["sentence"])):
        for j in range(len(responseToJson["return_object"]["sentence"][i]["morp"])):
            if responseToJson["return_object"]["sentence"][i]["morp"][j]["type"] == "VV":
                VerbList.append(responseToJson["return_object"]["sentence"][i]["morp"][j]["lemma"]+"다")

f_r=open('D:/이어달리기사업/vscode/준비중/22.02.15/verb_text.txt','a',encoding='utf-8')

                
def word(doc):
    des = ["NNG","NNP"]
    
    text = doc
    requestJson = {
        "access_key": accessKey,
        "argument": {
            "text": text,
            "analysis_code": analysisCode}}
    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson))
    responseToJson = json.loads(str(response.data,"utf-8"))
    for i in range(len(responseToJson["return_object"]["sentence"])):
        for j in range(len(responseToJson["return_object"]["sentence"][i]["morp"])):
            if responseToJson["return_object"]["sentence"][i]["morp"][j]["type"] in des:
                wordlist.append(responseToJson["return_object"]["sentence"][i]["morp"][j]["lemma"])



# for i in fileList:
#     print(f"파일명{i}")
    #f= open(addr+i,'r',encoding='utf-8')
    #f = open('D:/이어달리기사업/vscode/준비중/data/F_166747_8.csv', 'r',newline='',encoding='utf-8')
    
    # read Only
# Make Json
f_j=open('D:/이어달리기사업/vscode/준비중/22.02.15/verb_ToJson_text.txt','a',encoding='utf-8')
    #with open(addr+i,'r',encoding='utf-8') as file:
    
#with open('D:/이어달리기사업/vscode/준비중/data/F_166747_8.csv','r',encoding='cp949') as file:
with open('D:/이어달리기사업/vscode/준비중/그림일기/새 폴더/실수해도 괜찮아.txt','r',encoding='utf-8') as file:
    

    for ii in file:
        # if ii == '' or  ii == ' ' or  ii == '\n' or ii ==' \n' or ii == '  \n':
        #     pass
        # else :
        iii = ii.split('\n')
        
        
        Verb_def(iii[0])
        #print(VerbList)
    # 동사 처리 구간 
        for i in VerbList:
            if i in verb:
                final.append(ii)
                f_r.write(f"verb ={i} sentence={ii}'\n")
                f_j.write(f"{i}|{ii}\n")
                print("진행중")
        VerbList=[]
                
f_r.close()                
f_j.close()                
    
    
    
#구 코드    
#         for j in file:
#             jj=j.split('.')
#             for ii in jj:
#                 if ii == '' or  ii == ' ' or  ii == '\n' or ii ==' \n':
#                     pass
#                 else :
#                     Verb_def(ii)
#                     #print(VerbList)
#                 # 동사 처리 구간 
#                     for i in VerbList:
#                         if i in verb:
#                             final.append(ii)
#                             f_r.write(f"verb ={i} sentence={ii}'\n")
#                             f_j.write(f"{i}|{ii}\n")
#                     VerbList=[]
                    
# f.close()
# f_r.close()                
# f_j.close()                

