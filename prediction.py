# -*- coding: utf-8 -*-
"""Prediction v1.0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12bBYYZyPZVfDKLeBNBPkqLCLuTmQnD7d

# 모델 사용하기 & 평가하기

## 토크나이저와 모델 준비하기

로컬에서 가져오기 / 허깅페이스에서 가져오기 중에서 필요한 것 하나만 실행하기
"""

"""# 도커에 필요한 코드"""
import argparse 
p = argparse.ArgumentParser() 
p.add_argument('--model_route', required=True)
p.add_argument('--sample', required=True)
config=p.parse_args()

import torch

# 로컬에서 토크나이저와 모델 가져오기
from transformers import BertTokenizerFast
from transformers import MBartForConditionalGeneration
import os

path = './model_final'

tokenizer = BertTokenizerFast.from_pretrained(path, strip_accents=False, 
                                              lowercase=False) 
model = MBartForConditionalGeneration.from_pretrained(config.model_route)  # 기존 베이스 모델
model.load_state_dict(torch.load(path + "/pytorch_model.bin"))  # 파인튜닝한 weight

"""## 모델이 cuda 쓸 수 있게 하기 """

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # cuda가 사용 가능하다면 cuda를 사용하고 사용 불가하면 cpu 사용하도록

model.to(device)  # 모델을 디바이스에 불러오기
model.eval()  # elal()은 evaluation 과정에서 사용하지 않아야 하는 layer들을 알아서 off 시키도록 하는 함수

"""## 결과 예측 함수 """

# 텍스트 넣어서 결과 예측하는 함수 
def get_prediction(text):
    embeddings = tokenizer(text, max_length=256, truncation="longest_first", return_attention_mask=False,
                           return_token_type_ids=False, return_tensors='pt')  # 토크나이징
    embeddings.to(device)  # 토큰을 디바이스에 불러오기 
    output = model.generate(**embeddings, max_length=256, bos_token_id=tokenizer.cls_token_id, 
                            eos_token_id=tokenizer.sep_token_id)[0, 0:-1].cpu()  # 모델로 예측 
                                                                # tensor에서 토큰만 가져오기, [sep] 토큰 제외하기 
    result = tokenizer.decode(output[1:])  # 토큰을 글자로 디코딩
    if '[CLS]' in result:
        result = result[6:]
    return result  

# 함수로 예측하기 
print(get_prediction(config.sample))


