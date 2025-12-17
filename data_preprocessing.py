import pandas as pd
from konlpy.tag import Hannanum, Okt, Kkma, Komoran
from collections import Counter
import os

df = pd.read_csv("C:/Users/PKNU/Downloads/porksoup_review_data/sura_porksoup_google_review.csv")
df

tagger1 = Okt()
tagger2=Hannanum()
tagger3=Kkma()
tagger4=Komoran()

text =df['리뷰']
text

text_filtered = text.str.replace("[^a-zA-Zㄱ-ㅎㅏ-ㅣ가-힣\s]", "", regex=True)
text_filtered = text_filtered.str.replace("\s+", " ", regex=True)
text_filtered[0]

stopwords = "돼지국밥 부산 국밥 ㅠ ㅠㅠ ㅠㅠㅠ ㅋ ㅋㅋ ㅋㅋㅋ ㅋㅋㅋㅋ ㅎ ㅎㅎ ㅎㅎㅎ 돼지국밥집 국밥집 여기 방문 정도 이곳 nan"
stopwords = stopwords.split(' ')

tokenized_data_filtered2 = []

for i in text_filtered:
    temp = tagger3.nouns(str(i))
    temp =  [word for word in temp if len(word)>1] #1자리 글자 제거
    temp = [word for word in temp if word not in stopwords] #불용어제거
    tokenized_data_filtered2.append(temp)

print(tokenized_data_filtered2)

tokens = []

for k in tokenized_data_filtered2:
    tokens.extend(k) #k 하나마다 리스트들이니까 리스트들을 하나의 리스트로 합쳐줌

num_top_tokens = 100

counted_tokens = Counter(tokens)
top_keywords = dict(counted_tokens.most_common(num_top_tokens))

print(top_keywords)

top_keywords_df = pd.DataFrame(list(top_keywords.items()), columns = ["keywords", "freq"])

folder_path = "C:/Users/PKNU/Desktop/preprocessing_data"
os.makedirs(folder_path, exist_ok=True)

# 전처리 결과 저장
filename1 = "sura_keyword.txt"  # 전처리 결과 저장할 파일 이름
save_path = os.path.join(folder_path, filename1)

with open(save_path, "w", encoding="utf-8") as f:
    for doc in tokenized_data_filtered2:
        line = " ".join(doc)
        f.write(line + "\n")
        
        
# top100 저장
filename2 = "sura_keyword_top100.txt"   # top100 키워드 저장할 파일 이름
save_path2 = os.path.join(folder_path, filename2)

with open(save_path2, "w", encoding="utf-8") as f:
    for word, freq in top_keywords.items():
        f.write(f"{word}: {freq}\n")