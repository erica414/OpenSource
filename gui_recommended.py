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

        # 3. 화면에서 쓰는 키워드 → CSV 실제 컬럼명 매핑
        self.keyword_map = {
            "맑은 국물": "맑은 국물", "뽀얀 국물": "뽀얀 국물",
            "라멘": "라멘", "오소리감투": "오소리감투", "겉절이": "겉절이",
            "명란젓": "명란젓", "멍게김치": "멍게김치", "항정국밥": "항정국밥",
            "우동국밥": "우동",      # 예시, 실제 CSV 컬럼명에 맞게 수정
            "두부김치": "두부김치",
            "역세권": "역세권", "주차장": "주차장",
            "경성대·부경대": "경성대부경대", "광안리": "광안리", "사상": "사상",
            "신평": "신평", "수영": "수영", "용호동": "용호동", "서면": "서면",
            "싼 가격": "싼 가격", "24시간": "24시간", "미슐랭": "미슐랭",
            "웨이팅어플": "웨이팅 어플", "고기양 많음": "고기양 많음",
            "한약느낌": "한약 느낌", "마늘빻기": "마늘 빻기", "다이닝코드1위": "다이닝코드 1위"
        }

        # 4. 키워드 → 카테고리 매핑 (같은 카테고리는 OR, 서로 다른 카테고리는 AND 처리용)
        self.category_map = {
            "맑은 국물": "국물", "뽀얀 국물": "국물",
            "라멘": "특색 메뉴", "오소리감투": "특색 메뉴", "겉절이": "특색 메뉴",
            "명란젓": "특색 메뉴", "멍게김치": "특색 메뉴", "항정국밥": "특색 메뉴",
            "우동국밥": "특색 메뉴", "두부김치": "특색 메뉴",
            "역세권": "교통", "주차장": "교통",
            "경성대·부경대": "위치", "광안리": "위치", "사상": "위치",
            "신평": "위치", "수영": "위치", "용호동": "위치", "서면": "위치",
            "싼 가격": "기타", "24시간": "기타", "미슐랭": "기타", "웨이팅어플": "기타",
            "고기양 많음": "기타", "한약느낌": "기타", "마늘빻기": "기타", "다이닝코드1위": "기타"
        }

    def _load_and_preprocess(self):
        """CSV를 읽어 '상호명 + 키워드 컬럼들(O/X)' 형태의 DataFrame으로 반환"""
        if not os.path.exists(self.csv_path):
            # 파일이 없으면 빈 DataFrame
            return pd.DataFrame(columns=['상호명'])
        try:
            # 원본 CSV는 행: 키워드, 열: 식당일 가능성이 높으므로 transpose
            raw_df = pd.read_csv(self.csv_path, index_col=0)
            df = raw_df.transpose()
            # NaN은 'X'로 채우기
            df.fillna('X', inplace=True)
            df = df.reset_index().rename(columns={'index': '상호명'})
            return df
        except Exception as e:
            print("CSV 로드 중 오류:", e)
            return pd.DataFrame(columns=['상호명'])

    def get_recommendations(self, selected_keywords):
        """
        selected_keywords: 화면에서 선택된 키워드 리스트
        규칙:
         - 같은 카테고리(예: 국물, 특색 메뉴 등) 안에서는 OR
         - 서로 다른 카테고리는 AND
        """
        if not selected_keywords:
            # 아무 키워드도 선택 안 했으면 전체 반환
            return self.df

        filtered_df = self.df.copy()
        grouped_conditions = {}

        # 선택된 키워드를 카테고리 기준으로 묶기
        for kw in selected_keywords:
            cat = self.category_map.get(kw, "기타")
            grouped_conditions.setdefault(cat, []).append(kw)

        # 카테고리별로 OR, 카테고리 간에는 AND로 필터링
        for cat, kw_list in grouped_conditions.items():
            valid_cols = []
            for k in kw_list:
                csv_col = self.keyword_map.get(k)
                if csv_col and csv_col in filtered_df.columns:
                    valid_cols.append(csv_col)
            if not valid_cols:
                continue

            # 하나라도 'O'인 식당만 남기기 (OR 조건)
            mask = filtered_df[valid_cols].apply(
                lambda row: any(val == 'O' for val in row), axis=1
            )
            filtered_df = filtered_df[mask]

        return filtered_df


# =========================================================
# 추천 결과를 보여주는 GUI 윈도우
# =========================================================
class RecommendationWindow:
    def __init__(self, parent, selected_keywords):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("추천 결과")
        self.window.geometry("500x650")
        self.window.configure(bg="white")

        # 🔹 추천창 X 버튼 눌렀을 때 → 메인으로 복귀
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.selected_keywords = selected_keywords
        self.recommender = GukbapRecommender()
        self.results = self.recommender.get_recommendations(selected_keywords)

        self.build_ui()

    def on_close(self):
        """추천창 닫으면 메인창 다시 보이기"""
        self.window.destroy()
        if self.parent is not None:
            self.parent.deiconify()

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

        # 마우스 휠 스크롤
        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        )

        # 3. 결과 카드 생성
        if self.results.empty:
            tk.Label(
                self.scrollable_frame,
                text="선택하신 조건이 너무 까다로워요..\n조건을 하나만 줄여보시겠어요?",
                font=("맑은 고딕", 11),
                bg="white",
                fg="gray",
            ).pack(pady=50)
        else:
            for _, row in self.results.iterrows():
                self.create_restaurant_card(row)

    def create_restaurant_card(self, row):
        """각 식당 정보를 카드 형태로 표시"""
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
        tk.Label(
            card,
            text=feature_text,
            font=("맑은 고딕", 9),
            fg="#448aff",
            bg="white", 
            wraplength=420,
            justify="left"
        ).pack(anchor="w", padx=12, pady=(0, 8))

        # 🔍 자세히 보기 버튼 (여기서 open_detail_window 호출)
        tk.Button(
            card,
            text="자세히 보기",
            font=("맑은 고딕", 9, "bold"),
            bg="#f0f0ff",
            relief="ridge",
            command=lambda r=row: self.open_detail_window(r)
        ).pack(anchor="e", padx=12, pady=(0, 8))

    # =====================================================
    #  🔍 추천 결과 → 상세 화면으로 넘어가는 부분
    # =====================================================
    def open_detail_window(self, row):
        """추천 카드에서 선택한 식당의 상세창을 연다."""
        # 순환 참조 방지를 위해 여기서 import
        from gui_detail import RestaurantDetail

        name = row.get("상호명", "이름 없음")
        keywords = [col for col in row.index if col != "상호명" and row[col] == "O"]

        # 지금은 키워드 정보만 넘겨주고,
        # 추후 restaurant_info_template.csv 와 병합해서 주소/메뉴/평점 등을 채울 예정
        data = {
            "name": name,
            "keywords": keywords,
            "tags": keywords,
            "phone": None,
            "address": None,
            "parking": False,
            "hours_str": None,
            "map_url": None,
            "sns_url": None,
            "menu": [],
            "photo_path": None,
            "rating": None,
            "review_count": None,
            "price_range": None,
        }

        # 상세창 생성
        detail_win = tk.Toplevel(self.window)
        detail_win.title(name)
        detail_win.geometry("600x700")

        # 추천창은 잠시 숨겨서 "화면 전환" 느낌
        self.window.withdraw()

        def on_detail_close():
            # 상세창 닫으면 다시 추천창 보여주기
            detail_win.destroy()
            self.window.deiconify()

        detail_win.protocol("WM_DELETE_WINDOW", on_detail_close)

        detail = RestaurantDetail(detail_win, data)
        detail.pack(fill="both", expand=True)
