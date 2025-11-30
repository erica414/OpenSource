import tkinter as tk
from tkinter import ttk
import pandas as pd
import os

# =========================================================
# 데이터 처리 및 추천 알고리즘
# =========================================================
class GukbapRecommender:
    def __init__(self, csv_filename='deundeun_keyword_ox_df.csv'):
        # 1. CSV 파일 경로 설정
        current_dir = os.getcwd()
        self.csv_path = os.path.join(current_dir, csv_filename)
        
        # 2. 데이터 로드
        self.df = self._load_and_preprocess()

        # 3. GUI 키워드 vs CSV 컬럼 매핑
        self.keyword_map = {
            "맑은 국물": "맑은 국물", "뽀얀 국물": "뽀얀 국물",
            "라멘": "라멘", "오소리감투": "오소리감투", "겉절이": "겉절이",
            "명란젓": "명란젓", "멍게김치": "멍게김치", "항정국밥": "항정국밥",
            "두부김치": "두부김치", 
            "역세권": "역세권", "주차장": "주차장",
            "경성대·부경대": "경성대부경대", "광안리": "광안리", "사상": "사상", 
            "신평": "신평", "수영": "수영", "용호동": "용호동", "서면": "서면",
            "싼 가격": "싼 가격", "24시간": "24시간", "미슐랭": "미슐랭",
            "웨이팅어플": "웨이팅 어플", "고기양 많음": "고기양 많음",
            "한약느낌": "한약 느낌", "마늘빻기": "마늘 빻기", "다이닝코드1위": "다이닝코드 1위"
        }

        # 4. 카테고리 매핑 (로직용)
        self.category_map = {
             "맑은 국물": "국물", "뽀얀 국물": "국물",
             "라멘": "특색 메뉴", "오소리감투": "특색 메뉴", "겉절이": "특색 메뉴", 
             "명란젓": "특색 메뉴", "멍게김치": "특색 메뉴", "항정국밥": "특색 메뉴", 
             "두부김치": "특색 메뉴",
             "역세권": "교통", "주차장": "교통",
             "경성대·부경대": "위치", "광안리": "위치", "사상": "위치", 
             "신평": "위치", "수영": "위치", "용호동": "위치", "서면": "위치",
             "싼 가격": "기타", "24시간": "기타", "미슐랭": "기타", "웨이팅어플": "기타",
             "고기양 많음": "기타", "한약느낌": "기타", "마늘빻기": "기타", "다이닝코드1위": "기타"
        }

    def _load_and_preprocess(self):
        """CSV 파일을 읽고 행/열을 뒤집어(Transpose) '식당'이 행이 되도록 변환"""
        if not os.path.exists(self.csv_path):
            return pd.DataFrame(columns=['상호명'])
        try:
            raw_df = pd.read_csv(self.csv_path, index_col=0)
            df = raw_df.transpose()
            df.fillna('X', inplace=True)
            df = df.reset_index().rename(columns={'index': '상호명'})
            return df
        except Exception:
            return pd.DataFrame(columns=['상호명'])

    def get_recommendations(self, selected_keywords):
        if not selected_keywords: return self.df
        
        filtered_df = self.df.copy()
        grouped_conditions = {}
        
        # 카테고리별 그룹화
        for kw in selected_keywords:
            cat = self.category_map.get(kw, "기타")
            if cat not in grouped_conditions: grouped_conditions[cat] = []
            grouped_conditions[cat].append(kw)

        # 필터링 (카테고리 내 OR, 카테고리 간 AND)
        for cat, kw_list in grouped_conditions.items():
            valid_cols = []
            for k in kw_list:
                csv_col = self.keyword_map.get(k)
                if csv_col and csv_col in filtered_df.columns:
                    valid_cols.append(csv_col)
            if not valid_cols: continue
            
            mask = filtered_df[valid_cols].apply(lambda row: any(val == 'O' for val in row), axis=1)
            filtered_df = filtered_df[mask]
            
        return filtered_df

# =========================================================
# 결과 표시 윈도우 UI
# =========================================================
class RecommendationWindow:
    def __init__(self, parent, selected_keywords):
        self.window = tk.Toplevel(parent)
        self.window.title("추천 결과")
        self.window.geometry("500x650")
        self.window.configure(bg="white")
        
        self.selected_keywords = selected_keywords
        self.recommender = GukbapRecommender()
        self.results = self.recommender.get_recommendations(selected_keywords)

        self.build_ui()

    def build_ui(self):
        # 1. 헤더 영역
        header = tk.Frame(self.window, bg="white")
        header.pack(fill="x", padx=20, pady=20)
        
        count = len(self.results)
        title_text = f"총 {count}개의 맛집 발견!" if count > 0 else "조건에 맞는 맛집이 없어요 ㅠㅠ"
        
        tk.Label(header, text=title_text, font=("맑은 고딕", 16, "bold"), bg="white").pack(anchor="w")
        
        kw_str = ", ".join(self.selected_keywords) if self.selected_keywords else "전체 보기"
        tk.Label(header, text=f"선택 조건: {kw_str}", font=("맑은 고딕", 10), fg="gray", bg="white").pack(anchor="w", pady=(5,0))

        # 2. 스크롤 가능한 리스트 영역
        container = tk.Frame(self.window, bg="white")
        container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="white")

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=450)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 마우스 휠 스크롤 연결
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # 3. 결과 카드 생성
        if self.results.empty:
            tk.Label(self.scrollable_frame, text="선택하신 조건이 너무 까다로워요..\n조건을 하나만 줄여보시겠어요?", 
                     font=("맑은 고딕", 11), bg="white", fg="gray").pack(pady=50)
        else:
            for idx, row in self.results.iterrows():
                self.create_restaurant_card(row)

    def create_restaurant_card(self, row):
        # 카드 프레임 (깔끔한 흰색 + 테두리)
        card = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="solid")
        card.pack(fill="x", pady=6, ipady=5)

        # 상호명
        name = row.get('상호명', '이름 없음')
        tk.Label(card, text=name, font=("맑은 고딕", 13, "bold"), bg="white").pack(anchor="w", padx=12, pady=(8, 2))
        
        # 특징 태그 (O 표시된 것들)
        features = [col for col in row.index if row[col] == 'O' and col != '상호명']
        feature_text = " | ".join(features)
        
        if not feature_text:
            feature_text = "기본 정보"

        # 파란색 텍스트로 특징 표시
        tk.Label(card, text=feature_text, font=("맑은 고딕", 9), fg="#448aff", bg="white", 
                 wraplength=420, justify="left").pack(anchor="w", padx=12, pady=(0, 8))