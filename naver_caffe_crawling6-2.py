# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 11:56:38 2020
@author: juhyun.kim
@reference: https://stricky.tistory.com/108
"""


from konlpy.tag import Okt       #Twitter # pip install konlpy
from collections import Counter
from tqdm import tqdm
import pandas as pd

file = open("./preg_quest.csv", "r", encoding='cp949')
readline_list = file.readlines() 
file.close()

#읽은 파일을 konlpy Twitter를 통해서 단어 분석을 합니다.
#이건 명사고, 동사고, 특수문자이고, 외국어이고.. 뭐 그렇게 하나하나 분리해서 분석합니다.
twitter = Okt() #Twitter() 
morphs_list = []
#print(len(lists))

"""
for sentence in readline_list :
    #print(sentence)
    morphs_list.append(twitter.pos(sentence))
"""
for i in tqdm(range(0, len(readline_list)), mininterval=0.01):
    #print(sentence)
    morphs_list.append(twitter.pos(readline_list[i]))

#print(morphs_list)

#다음은 명사만 추출을 합니다.
#그중에서 필요 없는 tag들은 빼버립니다. 중간에 보이는 if 문에서 필요 없는 단어를 제외시켜 줍니다.
#보통은 한 글자짜리는 빼버리는데, 한글자 명사도 필요한 것이 있어서 전 if 문으로 하나하나 걸러 주었습니다.
noun_adj_adv_list = [] 
"""
for sentence in morphs_list : 
    for word, tag in sentence :
        if tag in ['Noun'] \
        and ("것" not in word) and ("저" not in word) and ("등" not in word) and ("전" not in word) \
        and ("요" not in word) and ("분" not in word) and ("시" not in word) and ("카" not in word) \
        and ("너" not in word) and ("및" not in word) and ("이" not in word) and ("거" not in word) \
        and ("좀" not in word) and ("제" not in word) and ("후" not in word) and ("비" not in word) \
        and ("내" not in word) and ("나" not in word) and ("수" not in word) and ("게" not in word) \
        and ("말"not in word): 
"""
for i in tqdm(range(0, len(morphs_list)), mininterval=0.01) : 
    for word, tag in morphs_list[i] :
        if tag in ['Noun'] \
        and ("것" not in word) and ("저" not in word) and ("시" not in word) and ("카" not in word) \
        and ("너" not in word) and ("및" not in word) and ("이" not in word) and ("거" not in word) \
        and ("좀" not in word) and ("제" not in word) and ("후" not in word) and ("비" not in word) \
        and ("내" not in word) and ("나" not in word) and ("수" not in word) and ("게" not in word) \
        and ("말"not in word):
            
            noun_adj_adv_list.append(word)
            
#print(noun_adj_adv_list)

#그런 다음, 명사 별로 빈도수를 카운트해서 출력해 봅니다.
#워드 클라우드의 바로 전 단계입니다.
count_counter = Counter(noun_adj_adv_list)
#print(count_counter)
words_dict = dict(count_counter.most_common())
#print(words_dict)

"""
words_list = list(zip(words_dict.keys(), words_dict.values()))
#print(words_list)
wdata_df = pd.DataFrame(words_list)
wdata_df.columns = ['word', 'frequency']
wdata_df.to_csv('./caffe_analysis.csv', encoding='cp949')
"""

#이젠 워드 클라우드를 할 차례가 왔습니다.
from wordcloud import WordCloud # pip install wordcloud
#import nltk                     # conda install nltk
#from nltk.corpus import stopwords
#import matplotlib 
import matplotlib.pyplot as plt
#from IPython.display import set_matplotlib_formats

#matplotlib.rc('font', family='Malgun Gothic')
#set_matplotlib_formats('retina')
#matplotlib.rc('axes', unicode_minus=False)

#그리고 마스킹을 위해서 라이브러리를 import 하고, 마스킹 이미지도 지정해 줍니다.
#주의할 점은 마스킹 이미지는 꼭 하얀 바탕에 검은 그림이어야 잘 된다는 겁니다.
#import numpy as np
#import random
#from PIL import Image

#r4_mask = np.array(Image.open("./image/twitter.png"))
wordcloud = WordCloud(background_color="white",
               font_path='./font/NanumBrush.ttf',
               colormap="prism",
               width=800,
               height=800,
               #mask=r4_mask
)

wordcloud_result = wordcloud.generate_from_frequencies(words_dict)

plt.figure(figsize=(20, 20))
plt.imshow(wordcloud_result, interpolation="bilinear")
plt.axis("off")
plt.show()