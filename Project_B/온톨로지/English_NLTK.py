import nltk

def Make_text():
    nltk.download('punkt')                       # 토큰화를 위한 모듈
    nltk.download('averaged_perceptron_tagger')  # 형태소 분석 모듈
    word =['NN','NNS','NNP','NNPS','PRP','PRPS','WDT','WP','WPS','WRB']
    verb =['VB','VBD','VBG','VBN','VBP','VBZ']
    
# NN     : 단수 명사 
# NNS    : 복수 명사
# NNP    : 고유 명사 / 대명사-단수형
# NNPS   : 고유 명사 / 대명사-복수형
# PRP    : 인칭 대명사
# PRPS   : 인칭 대명사 소유격,소유격 대명사
# VB     : 동사 원형
# VBD    : 동사 과거형
# VBG    : 동사-동명사 /진행형,동명사(동사에 -ing 붙여 만든 명사)
# VBN    : 동사 - 과거분사형
# VBP    : 동사 - 복수명사
# VBZ    : 동사 - 3인칭 단수
# WDT    : wh-한정사, 한정적 관계 대명사, 문장 맨 앞에 등장하지 않는 what, which
# WP     : wh-대명사 / 주격 대명사
# WPS    : 소유 대명사 / 소유격 관계 대명사
# WRB    : wh-부사 / 소부사격 관계 대명사 

    path = 'D:/이어달리기사업/vscode/준비중/22.02.15/data/data/'
    #file = open('D:/이어달리기사업/vscode/준비중/22.02.15/English_verb_ToJson_text.txt','a',encoding='utf-8') # 제이슨 만드는 파일
    file_r = open('D:/이어달리기사업/vscode/준비중/22.02.15/English_verb.txt','a',encoding='utf-8') # 보여주기 파일
    with open(path+'english.txt','r',encoding='utf-8') as f:
        for i in f:
            text = i
            tokens=nltk.word_tokenize(text)
            prin =nltk.pos_tag(tokens) #NLTK가 현재 권장하는 품사 태거(tagger)를 사용하여 주어진 개별 토큰에 태그(tag)를 지정한다.
            #print(prin[0][1])
            print(len(prin))
            #print(prin[0][1])
            for o in range(len(prin)):
                if prin[o][1] in word:
                    print(f"명사={prin[o][0]},문장 ={i}")
                    file_r.write(f"명사 = {prin[o][0]} 문장 = {i}")
                elif prin[o][1] in verb:
                    print(f"동사={prin[o][0]}, 문장 = {i}")
                    #file.write(f"{prin[o][0]}|{i}")
                    file_r.write(f"동사 = {prin[o][0]} 문장 = {i}")     
                        
                else:
                    pass
                
    #file.close()        
    file_r.close()        




