
from base64 import encode
from pickle import FALSE
from xml.etree import cElementTree
from numpy import block
import torch 
from torch.utils.data import DataLoader
from datasets import load_dataset
from sentence_transformers import SentenceTransformer, LoggingHandler, losses, models, util
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from sentence_transformers.readers import InputExample
from transformers import AutoModel, AutoTokenizer
#############################################################################
import urllib3
import json
import pandas as pd
#docs = 'D:\이어달리기사업\4차 미팅\준비중\data'

import re
import sys
from google.cloud import speech
#from google.cloud.speech import enums
#from google.cloud.speech import types
import pyaudio
from six.moves import queue
from threading import Thread
import time
import os
import tts
import html
import os
from google.cloud import texttospeech
from playsound import playsound
import pygame 
import datetime

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'D:/이어달리기사업/4차 미팅/준비중/data/gcp_key/smiling-destiny-326000-e96b1ffc8847.json'
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms
cnt=1
# STT
class MicrophoneStream(object):
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk #일정한 크기로 잘라내는 
        self._buff = queue.Queue() # queue = FIFO 
        self.closed = True
        self.isPause = False
        
    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )
        self.closed = False
        return self

    def __exit__(self, type, value, traceback): 
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def pause(self):
        if self.isPause == False:
            self.isPause = True
            
    def resume(self):
        if self.isPause == True:
            self.isPause = False
            
    def status(self):
        return self.isPause

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        if self.isPause == False:
            self._buff.put(in_data)
        return None, pyaudio.paContinue
    
    def generator(self): # 대용량 반복을 수행할 때, 메모리를 더욱 효과적으로 사용하기 위한 도구 = generator
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return

            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b''.join(data) # 호출 시 원하는 결과를 리턴하고 실행 흐름을 일시 정지하여 함수를 재활용 가능 
            
class Gspeech(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.language_code = 'ko-kr'  #'en-US' ko-kr # a BCP-47 language tag
        self._buff = queue.Queue()
        self.client = speech.SpeechClient()
        self.config = speech.RecognitionConfig(
            profanity_filter=True,  # 욕설 필터링
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            use_enhanced=True, 
            language_code=self.language_code)
        self.streaming_config = speech.StreamingRecognitionConfig(
            config=self.config,
            interim_results=True)
        self.mic = None
        self.status = True
        self.daemon = True
        self.start()

    def __eixt__(self):
        self._buff.put(None)

    def run(self):
        with MicrophoneStream(RATE, CHUNK) as stream: # 클래스를 열고 그 안에서만 사용하기 위해, 그리고 FIFO이므로 with 사용함. 
            self.mic = stream
            audio_generator = stream.generator()
            requests = (speech.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)
            responses = self.client.streaming_recognize(self.streaming_config, requests)
            self.listen_print_loop(responses, stream)
        self._buff.put(None)
        self.status = False
    def pauseMic(self):
        if self.mic is not None:
            self.mic.pause()
    def resumeMic(self):
        if self.mic is not None:
            self.mic.resume()
    def getText(self, block = True):
        return self._buff.get(block=block)
    def listen_print_loop(self, responses, mic):
        num_chars_printed = 0
        try:
            for response in responses:
                if not response.results:
                    continue

                result = response.results[0]
                if not result.alternatives:
                    continue
                transcript = result.alternatives[0].transcript # alternatives : 심볼릭 링크를 관리해주는 명령어.
                overwrite_chars = ' ' * (num_chars_printed - len(transcript))
                if not result.is_final:
                    sys.stdout.write(transcript + overwrite_chars + '\r') # stdout :출력버퍼, 출력버퍼가 지정되어 있지 않으면 터미널 출력(표준 출력)
                    sys.stdout.flush()
                    num_chars_printed = len(transcript)
                else:
                    self._buff.put(transcript+overwrite_chars)
                    num_chars_printed = 0
        except:
            return
# def main():
#     gsp = Gspeech()
#     while True:
#         stt = gsp.getText()
#         if stt is None:
#             break
#         print(stt)
#         time.sleep(0.01)
#         if ('끝내자' in stt):
#             break
#         elif ('the end' in stt):    
#             break
# if __name__ == '__main__':
#     main()            

# tts
def ssml_to_audio(ssml_text, outfile):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)
    print(synthesis_input)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR", # 한글 'ko-kr' 'en-US'
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config)
    with open(outfile, "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file " + outfile)
        out.close()
    
        

def text_to_ssml(inputfile):
    raw_lines = inputfile
    escaped_lines = html.escape(raw_lines)
    ssml = "<speak>{}</speak>".format(
         escaped_lines.replace("\n", '\n<break time="4s"/>')) # 기본 음성

#ssml = '<speak><say-as interpret-as="characters">can</say-as></speak>' # 한글자씩 말함 한글은 안 됨
   # ssml = '<p><s>This is sentence one.</s><s>This is sentence two.</s></p>' # 문장과 단락 
    return ssml        
        
        
        
        
        
# transformer
wordlist=[]
# sentencetransformer 는 입력된 문장 간 유사도를 빠르게 구할 수 있도록 설계됨
# 사전에 학습 되어있는 모델
model = SentenceTransformer("Huffon/sentence-klue-roberta-base")
#model = SentenceTransformer("jhgan/ko-sbert-sts")

# #model = "klue/roberta-base"
# model = AutoModel.from_pretrained("klue/roberta-large")
# tokenizer = AutoTokenizer.from_pretrained("klue/roberta-large")
model_eng = SentenceTransformer("distiluse-base-multilingual-cased")
#개채 분석 코드 (keep_robotics_project.py 파일 복사) - start
def word(doc):
    des = ["NNG","NNP"]
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU" # 언어 분석 기술(문어)
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU_spoken" # 언어 분석 기술(구어)
    accessKey = "31e6f9bb-3afc-48ba-90d8-fd988cf15f2e"
    analysisCode = "ner"
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

# 여기까지 - end 

# docs 한글버전

def trans_kor(stt):
    docs=[]
    

    for ii in range(1,10):
        i = str(ii)
        with open('D:/이어달리기사업/4차 미팅/준비중/data/json/word'+i+'.json',encoding='utf-8') as f:
            data = json.load(f)
            doc = data['talk']['content']['Utterance']
            docs.append(doc)
    
    print(docs)    
       
    # docs = [
    #     "테이블은 방에 3개 거실에 2개 있다.",
    #     "토끼 인형은 테이블 위에 고스란히 앉아있다.",
    #     "나는 오늘 바나나를 먹었다.",
    #     "오늘 아침에 오줌을 싸서 엄마한테 혼났다.",
    #     "호랑이 인형은 테이블 위에 있다.",
    #     "선생님 참 이뻐요",
    #     "곰돌이 인형은 교실에 있다.",
    #     "곰돌이 인형은 이쁘다",
    #     "토끼 인형은 어디에 있나요",
    # ]
    # 임베딩 과정
    
              
            
    document_embeddings = model.encode(docs)
    query = stt
    query_embedding = model.encode(query)

    top_k = min(1, len(docs))

    cos_scores = util.pytorch_cos_sim(query_embedding, document_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)
    print(f"입력 문장: {query}")
    print(f"\n<입력 문장과 유사한 {top_k} 개의 문장>\n")

    for i, (score, idx) in enumerate(zip(top_results[0], top_results[1])): # top_result[0]- 유사도 결과 값 , top_result[1] - 인덱스 값
        print(f"{i+1}: {docs[idx]} {'(유사도: {:.4f})'.format(score)}\n")
        #word(docs[idx])
        plaintext = docs[idx]
        ssml_text = text_to_ssml(plaintext)
        
        nowDate = datetime.datetime.now()
        date = nowDate.strftime("%Y-%m-%d_%H%M%S")
        print(date)
        cntt = '_'+str(cnt)
        ssml_to_audio(ssml_text, 'D:/sound/file'+date+cntt+'.wav')
        music_file = ('D:/sound/file'+date+cntt+'.wav')
        
        pygame.mixer.init()
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()
        
        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            clock.tick(30)
        pygame.mixer.quit()
        print("hh")    
        
        # playsound('D:/sound/file'+ii+'.wav')
        # play = multiprocessing.Process(target=playsound, args=('D:/sound/file'+ii+'.wav'))
        # play.start()
        
        
        

#docs 영어버전

def trans_eng():
    
    # docs = [
    #     "The rabbit doll is on the table.",
    #     "I ate banana for breakfast.",
    #     "Teacher is very pretty",
    #     "The teddy bear is in the classroom.",
    #     "The teddy bear is a girl",
    #     "There is cotton inside the teddy bear.",
    # ]
    docs=[]
    path = 'D:/이어달리기사업/vscode/준비중/22.02.15/영어Json/'
    fileName = os.listdir(path)
    for ii in range(1,len(fileName)):
        i = str(ii)
        with open('D:/이어달리기사업/vscode/준비중/22.02.15/영어Json/WordJson'+i+'.json',encoding='utf-8') as f:
            data = json.load(f)
            doc = data['talk']['content']['Utterance']
            docs.append(doc)
    
    
    # 임베딩 과정
    document_embeddings = model_eng.encode(docs)
    query = "What are your children's favorite dolls?"
    query_embedding = model_eng.encode(query)

    top_k = min(1, len(docs))

    cos_scores = util.pytorch_cos_sim(query_embedding, document_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)
    print(f"입력 문장: {query}")
    print(f"\n<입력 문장과 유사한 {top_k} 개의 문장>\n")

    for i, (score, idx) in enumerate(zip(top_results[0], top_results[1])): # top_result[0]- 유사도 결과 값 , top_result[1] - 인덱스 값
        print(f"{i+1}: {docs[idx]} {'(유사도: {:.4f})'.format(score)}\n")
        #word(docs[idx])
    print(wordlist)

trans_eng()
# def main():
#     print('hi')
    
#     gsp = Gspeech()
#     while True:
#         stt = gsp.getText()
#         if stt is None:
#             break
#         trans_kor(stt)
#         print(stt)

#         time.sleep(0.05)
#         if ('끝내자' in stt):
#             break
#         elif ('the end' in stt):    
#             break
# if __name__ == '__main__':
#     main()            
    

    
"""
    사전 학습된 모델 사용 
    영어버전 학습 필요
    TTS&STT 적용 


"""
# 라이선스 표시 !! 
# Apache Licence
# Version 2.0 