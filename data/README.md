# 📊 데이터 수집 및 전처리 코드 안내 (Data Collection & Preprocessing)

본 문서는
「구글 리뷰 데이터를 이용한 부산 로컬 국밥 맛집 추천 프로그램」 개발 과정 중
키워드 추출을 위해 사용된 데이터 수집 및 전처리 코드에 대한 설명을 제공합니다.

> ⚠️ 본 디렉터리의 코드는 프로그램 실행에 필수는 아니며,
데이터 분석 및 키워드 설계 과정을 투명하게 공유하기 위한 목적의 부가 자료입니다.

## 📁 디렉터리 구성
```
data/
├── data_collection.py       # 구글 리뷰 데이터 수집 코드
├── data_preprocessing.py    # 리뷰 텍스트 전처리 및 키워드 추출 코드
└── README.md                # 데이터 수집·전처리 설명 문서 (현재 본 파일)
```

## 1️⃣ 데이터 수집 코드 (data_collection.py)
### 🔎 목적

- Google Maps에 등록된 국밥집 리뷰 데이터를 수집
- 리뷰 텍스트를 CSV 파일로 저장하여 이후 키워드 분석에 활용

### ⚠️ 현재 코드 실행 관련 안내 (중요)

본 프로젝트에서 사용된 data_collection.py는
Google Maps 웹 정책 변경으로 인해 현재 정상 작동하지 않습니다.

이유
- Google Maps 리뷰 페이지는 로그인 상태에서만 리뷰 전체 로딩이 가능
- Selenium 기반 크롤링 시 비로그인 환경에서는 리뷰 접근이 제한
- 로그인을 자동화할 경우:
    - Google 계정 정보 노출 위험
    - 오픈소스 프로젝트의 보안·윤리 문제 발생

👉 따라서 본 프로젝트에서는 해당 코드를 수정·보완하지 않고,
“과정 기록용 코드”로만 포함하였습니다.

### 🧠 참고 사항
- 실제 데이터 수집은 개인 로컬 환경 + 로그인 상태에서 제한적으로 수행
- 수집된 결과물(CSV)만 이후 전처리 및 추천 시스템에 사용

---

## 2️⃣ 데이터 전처리 및 키워드 추출 (data_preprocessing.py)
### 🔎 목적
- 리뷰 텍스트에서 불필요한 문자 제거
- 형태소 분석을 통해 의미 있는 키워드 추출
- 키워드 빈도 분석을 통해 추천 시스템의 기준 키워드 설계

### 🛠 사용 기술
- pandas : CSV 데이터 로딩
- KoNLPy : 한글 형태소 분석
- Okt
- Hannanum
- Kkma
- Komoran
- collections.Counter : 키워드 빈도 분석

### ⚠️ Python 버전 주의 사항
> ✅ Python 3.8 환경 사용을 권장합니다.

이유:
- `KoNLPy` 및 일부 형태소 분석기는
- Python 3.10 이상에서 설치/실행 문제가 발생할 수 있음

- 프로젝트 진행 당시 **Python 3.8 + Anaconda 환경**에서 안정적으로 동작 확인

### 🔧 실행 환경 준비 (권장)
✔ Anaconda 환경 (권장)
```
conda create -n text_analysis python=3.8
conda activate text_analysis
pip install pandas konlpy
```

> Java(JDK)가 별도로 필요할 수 있습니다.
> KoNLPy 설치 시 오류 발생하면 JDK 8 이상 설치 필요.

▶ 실행 방법
```
python data_preprocessing.py
```
- 입력: Google 리뷰 CSV 파일
- 출력: 키워드 및 빈도 분석 결과(DataFrame)

---

## 3️⃣ 가상환경에 대하여
본 프로젝트에서는 환경 충돌 방지를 위해 가상환경을 사용하였으나,
필수는 아닙니다.
- 로컬 Python 환경에서 실행 가능
- 단, 형태소 분석기 특성상 Python 3.8 이하 권장
- Anaconda 사용 시 환경 관리가 비교적 수월

---

## 📌 정리
- `data_collection.py`
    - Google 정책 변경으로 현재 실행 불가
    - 데이터 수집 과정 공유 목적의 참고 코드
- data_preprocessing.py
    - 실제 키워드 설계에 사용
    - Python 3.8 환경에서 실행 권장
- 본 디렉터리는 메인 프로그램 실행과는 독립적

## 📎 참고 자료
- KoNLPy 공식 문서: https://konlpy.org
