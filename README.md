# 구글 리뷰 데이터를 이용한 부산 로컬 국밥 맛집 찾기

## 🔑 프로젝트 소개
> 구글 리뷰 데이터 기반 사용자 선호도 맞춤 '실패 없는' 부산 국밥 맛집 추천 데스크톱 GUI 애플리케이션

## 💡 계획 의도
부산에는 수많은 국밥집이 있고, 관광객과 지역 주민 모두 *"어디가 내 취향과 가장 잘 맞는지"* 파악하기 어렵습니다.  
따라서 이 프로젝트는 **Google Maps 리뷰 데이터에서 키워드를 추출하여**,  
사용자 취향(국물 타입, 특색 메뉴, 위치, 편의 요소 등)에 따라 최적의 국밥집을 추천하는= 시스템을 개발하고자 하였습니다.

## ✨ 주요 기능 (Features)

### 🔍 1. 취향 기반 키워드 선택
- 맑은/뽀얀 국물  
- 라멘, 오소리감투, 겉절이 등 특색 메뉴  
- 역세권, 주차장 등 교통 편의  
- 경성대·부경대 / 광안리 / 사상 등 위치 기반  
- 싼 가격, 고기양 많음, 24시간 등 기타 요소  

### 🤖 2. 사용자 맞춤 추천 알고리즘
- 동일 카테고리 키워드 = **OR 조건**
- 서로 다른 카테고리 = **AND 조건**
- CSV의 키워드(O/X) 정보를 기반으로 DataFrame 필터링
- 필터링 엔진: `GukbapRecommender` 클래스

### 🖥 3. 직관적인 GUI
- Tkinter 기반의 데스크톱 GUI  
- 키워드 버튼 & 선택된 키워드 칩(Chip) UI  
- 스크롤 가능한 메인 화면 & 추천 화면  
- 로고 포함 상단 헤더 UI  

### 📸 4. 식당 상세 정보 제공
- 이미지(썸네일 및 상세 이미지)
- 전화번호 / 주소 / 주차 / 영업시간  
- 메뉴(이름:가격:설명 형식 파싱)
- 리뷰 기반 키워드 태그
- 지도 or SNS 링크 버튼으로 외부 연결

---

## 🛠 기술 스택 (Tech Stack)

| 분야 | 기술 |
|------|------|
| Language | Python 3.x |
| GUI Framework | Tkinter |
| Data Handling | Pandas, CSV |
| Image Processing | Pillow(PIL) |
| External Source | Google Maps 리뷰 데이터 기반 키워드 |

<div>
  <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Selenium-3D424C?style=for-the-badge&logo=selenium&logoColor=white">
  <img src="https://img.shields.io/badge/PyInstaller-404040?style=for-the-badge&logo=python&logoColor=white">
</div>

### ✨Collaboration Tools✨
<div>
  <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
  <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white">
</div>

---

## 📁 프로젝트 구조 (Project Structure)
```
├── gui_main.py # 메인 화면 (키워드 선택) 
├── gui_recommended.py # 추천 결과 화면
├── gui_restaurant_list.py # 전체 리스트 화면
├── gui_detail.py # 상세 정보 화면
├── keyword.csv # 키워드 O/X 데이터
├── restaurant_info.csv # 식당 상세 정보
├── img/
  ├── bonjeon.png
  ├── subyeon.png
  ├── hapcheon_1.png
  ├── yeongjin.png
  ├── deundeun_logo.png
  ├── ...
```

---

## 🔧 구현 상세 (Implementation Details)

### ✔ 추천 알고리즘 (`GukbapRecommender`)
- `keyword.csv` → DataFrame 로딩
- 키워드 컬럼은 ‘O’ 또는 ‘X’
- 화면 키워드와 CSV 컬럼명을 매핑 (`keyword_map`)
- 카테고리 단위(국물/특색 메뉴/교통/위치/기타)로 그룹 필터링

**동작 방식**
1. 사용자가 선택한 키워드를 카테고리별로 그룹화  
2. 카테고리 내부는 OR 조건  
3. 카테고리 간에는 AND 조건  
4. 최종 필터링된 식당 리스트를 추천 결과 화면에 카드 형태로 출력  

---

### ✔ 메인 화면 (`gui_main.py`)
- 키워드를 카테고리별로 버튼 UI로 제공  
- 클릭한 키워드는 칩 형태로 상단에 표시  
- 스크롤 가능한 메인 Canvas  
- “추천” 버튼 클릭 시 추천창으로 이동  

---

### ✔ 추천 결과 화면 (`gui_recommended.py`)
- 조건에 맞는 식당 수 출력
- 추천 식당 카드 UI  
- 키워드 태그 표시  
- “자세히 보기” 클릭 시 상세 정보 창 열기  

---

### ✔ 전체 리스트 화면 (`gui_restaurant_list.py`)
- 등록된 모든 식당의 목록을 카드 형태로 표시  
- 썸네일 이미지 자동 로드  
- 카드 클릭 또는 버튼 클릭 시 상세 페이지 이동  

---

### ✔ 상세 정보 화면 (`gui_detail.py`)
- 이미지 로딩(상대경로 → img 폴더 자동 탐색)
- 전화/주소/주차/영업시간 표시  
- 메뉴 문자열 파싱  
- 키워드 태그  
- 지도 / SNS 링크 버튼  
- 스크롤 가능한 상세 UI 구성  

---

## 📘 사용 방법 (How to Use)

### 1) 필수 모듈 설치
```
pip install pillow pandas
```
- `pillow` → 이미지 로딩 (Image, ImageTk)
- `pandas` → CSV 데이터 처리

### 2) 실행
```bash
python gui_main.py
```
### 3) 원하는 키워드 선택
- GUI에서 원하는 특징을 선택합니다.
- 예) `맑은국물`, `역세권`, `고기양 많음`

### 4) "추천" 버튼 클릭
- 조건에 맞는 맛집 목록이 카드 형태로 나타납니다.

### 5) "자세히 보기" 클릭
- 해당 식당의 상세 정보를 확인할 수 있습니다.

### 6) 지도 링크로 위치 바로 확인
- 원하면 SNS/카페 링크도 열기 가능!

---

## 👥 기여자

<table>
  <tr>
    <th>강정완</th>
    <th>신하윤</th>
    <th>이연주</th>
  </tr>
  <tr>
    <td align="center">
      <img src="https://avatars.githubusercontent.com/Jeongwan2" width="100" />
    </td>
    <td align="center">
      <img src="https://avatars.githubusercontent.com/erica414" width="100" />
    </td>
    <td align="center">
      <img src="https://avatars.githubusercontent.com/JJUKKUMMI" width="100" />
    </td>
  </tr>
  <tr>
    <td align="center"><span style="color:lightgray;">리더</span> </td>
    <td align="center"><span style="color:lightgray;">커미터</span> </td>
    <td align="center"><span style="color:lightgray;">메인테이너</span> </td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/Jeongwan2">@Jeongwan2</a> </td>
    <td align="center"><a href="https://github.com/erica414">@erica414</a> </td>
    <td align="center"><a href="https://github.com/JJUKKUMMI">@JJUKKUMMI</a> </td>
  </tr>
</table>
