import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # pip install pillow

from gui_recommended import RecommendationWindow
from gui_restaurant_list import RestaurantListWindow

# 카테고리 & 키워드 정의
CATEGORY_KEYWORDS = {
    "국물": ["맑은 국물", "뽀얀 국물"],
    "특색 메뉴": ["라멘", "오소리감투", "겉절이", "명란젓", "멍게김치", "항정국밥", "우동국밥", "두부김치"],
    "교통": ["역세권", "주차장"],
    "위치": ["경성대·부경대", "광안리", "사상", "신평", "수영", "용호동", "서면"],
    "기타": ["싼 가격", "24시간", "미슐랭", "웨이팅어플", "고기양 많음", "한약느낌", "마늘빻기", "다이닝코드1위"],
}

CATEGORY_COLORS = {
    "국물": "#d6f0d6",      # 연녹
    "특색 메뉴": "#ffe0f0",  # 연분홍
    "교통": "#ffe8d6",      # 연살구
    "위치": "#d6e8ff",      # 연파랑
    "기타": "#eeeeee",      # 연회색
}


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("든든한 국밥 추천")
        self.root.geometry("1400x750")  # 전체 화면 크기
        self.root.configure(bg="white")

        # 선택된 키워드: 순서를 유지하기 위해 list 사용
        self.selected_keywords = []
        # 키워드 → 버튼 위젯 매핑 (색 변경용)
        self.keyword_buttons = {}
        # 키워드 → 카테고리 매핑
        self.keyword_to_category = self.build_keyword_category_map()

        self.build_header()
        self.build_center_area()
        self.build_keyword_section()
        self.build_selected_section()
        self.build_recommend_button()

    # 키워드 → 카테고리 역매핑
    def build_keyword_category_map(self):
        m = {}
        for cat, kws in CATEGORY_KEYWORDS.items():
            for kw in kws:
                m[kw] = cat
        return m

    # ----------------- 헤더 -----------------
    def build_header(self):
        header = tk.Frame(self.root, bg="white")
        header.pack(side="top", fill="x", padx=10, pady=8)

        # 3열 구성: [메뉴(왼쪽)] [로고+제목(정중앙)] [오른쪽 여백]
        header.columnconfigure(0, weight=1)   # 왼쪽
        header.columnconfigure(1, weight=0)   # 가운데
        header.columnconfigure(2, weight=1)   # 오른쪽

        # --- 1열: 메뉴 버튼 ---
        menu_frame = tk.Frame(header, bg="white")
        menu_frame.grid(row=0, column=0, sticky="w")

        tk.Button(
            menu_frame,
            text="≡",
            bg="white",
            bd=0,
            font=("맑은 고딕", 20, "bold"),
            command=self.on_menu_click
        ).pack()

        # --- 2열: 로고 + 제목 (가운데) ---
        title_frame = tk.Frame(header, bg="white")
        title_frame.grid(row=0, column=1)

        try:
            logo_img = Image.open("deundeun_logo.png").resize((100, 60), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            tk.Label(title_frame, image=self.logo_photo, bg="white").pack(side="left", padx=(0, 10))
        except Exception:
            tk.Label(title_frame, text="[로고]", bg="white",
                     font=("맑은 고딕", 14)).pack(side="left", padx=(0, 10))

        tk.Label(
            title_frame,
            text="든든한 국밥 추천",
            font=("맑은 고딕", 28, "bold"),
            bg="white"
        ).pack(side="left")

        # --- 3열: 오른쪽 여백 ---
        right_space = tk.Frame(header, bg="white")
        right_space.grid(row=0, column=2, sticky="e")

    def on_menu_click(self):
        # 리스트 창 띄우고 메인 창은 숨김 (식당 리스트 페이지로 전환)
        RestaurantListWindow(self.root)
        self.root.withdraw()

    # ---------- 가운데 정렬용 래퍼 ----------
    def build_center_area(self):
        wrapper = tk.Frame(self.root, bg="white")
        wrapper.pack(fill="both", expand=True)

        self.center = tk.Frame(wrapper, bg="white")
        self.center.pack(expand=True)  # 가운데 정렬

        tk.Label(
            self.center,
            text="큰 키워드를 보고, 원하는 세부 키워드를 선택해보세요!",
            font=("맑은 고딕", 12),
            bg="white"
        ).pack(pady=(0, 15))

    # ---------- 키워드 선택 영역 ----------
    def build_keyword_section(self):
        kw_outer = tk.Frame(self.center, bg="white")
        kw_outer.pack(pady=(0, 20))

        for cat, kws in CATEGORY_KEYWORDS.items():
            row = tk.Frame(kw_outer, bg="white")
            row.pack(fill="x", pady=5)

            # 왼쪽 색 박스 + 카테고리 이름
            color = CATEGORY_COLORS.get(cat, "#eeeeee")
            cat_box = tk.Frame(row, bg=color, width=120, height=40, bd=1, relief="solid")
            cat_box.pack(side="left", padx=(0, 10))
            cat_box.pack_propagate(False)

            tk.Label(
                cat_box,
                text=cat,
                bg=color,
                font=("맑은 고딕", 11, "bold")
            ).pack(expand=True)

            # 오른쪽 키워드 버튼들
            kw_frame = tk.Frame(row, bg="white")
            kw_frame.pack(side="left")

            for kw in kws:
                btn = tk.Button(
                    kw_frame,
                    text=kw,
                    width=18,          # 긴 키워드까지 넉넉하게
                    font=("맑은 고딕", 10),
                    relief="groove",
                    bg="white",
                    activebackground="#e0e0ff",
                    command=lambda k=kw: self.toggle_keyword(k)
                )
                btn.pack(side="left", padx=4, pady=3)

                # 키워드별 버튼 위젯 저장 (색 토글용)
                self.keyword_buttons[kw] = btn

    # ---------- 선택된 키워드 표시 영역 ----------
    def build_selected_section(self):
        box_outer = tk.Frame(self.center, bg="white")
        box_outer.pack(fill="x", pady=(0, 15))

        tk.Label(
            box_outer,
            text="선택된 키워드:",
            font=("맑은 고딕", 11),
            bg="white"
        ).pack(anchor="w", pady=(0, 3))

        self.selected_box = tk.Frame(box_outer, bg="white", bd=1, relief="solid")
        self.selected_box.pack(fill="x", padx=2, pady=(0, 5))

        self.selected_container = tk.Frame(self.selected_box, bg="white")
        self.selected_container.pack(fill="x", padx=8, pady=6)

        self.refresh_selected_chips()

    # ---------- 추천 버튼 ----------
    def build_recommend_button(self):
        tk.Button(
            self.center,
            text="추천",
            font=("맑은 고딕", 12, "bold"),
            bg="#cfe2ff",
            activebackground="#cfe2ff",
            relief="ridge",
            padx=20, pady=8,
            command=self.on_recommend
        ).pack(pady=(0, 10))

    # ---------- 키워드 토글 / 칩 표시 ----------
    def toggle_keyword(self, kw):
        # 이미 선택되어 있으면 제거
        if kw in self.selected_keywords:
            self.selected_keywords.remove(kw)
            if kw in self.keyword_buttons:
                self.keyword_buttons[kw].configure(bg="white")
        else:
            # 새로 선택 → 리스트 뒤에 추가 (선택 순서 유지)
            self.selected_keywords.append(kw)
            if kw in self.keyword_buttons:
                self.keyword_buttons[kw].configure(bg="#d9d9d9")  # 선택된 버튼 회색

        self.refresh_selected_chips()

    def remove_keyword(self, kw):
        if kw in self.selected_keywords:
            self.selected_keywords.remove(kw)
            # 칩에서 X 눌러도 위 버튼 색 복구
            if kw in self.keyword_buttons:
                self.keyword_buttons[kw].configure(bg="white")

        self.refresh_selected_chips()

    def refresh_selected_chips(self):
        # 기존 칩 제거
        for w in self.selected_container.winfo_children():
            w.destroy()

        if not self.selected_keywords:
            tk.Label(
                self.selected_container,
                text="키워드를 선택하세요.",
                bg="white",
                font=("맑은 고딕", 10),
                fg="gray"
            ).grid(row=0, column=0, sticky="w")
            return

        # 한 줄 최대 12개까지 가능 (1400px 기준 충분)
        max_per_row = 12

        for i, kw in enumerate(self.selected_keywords):
            row = i // max_per_row
            col = i % max_per_row

            cat = self.keyword_to_category.get(kw)
            color = CATEGORY_COLORS.get(cat, "#eeeeee")

            chip = tk.Frame(
                self.selected_container,
                bg=color,
                bd=1,
                relief="solid",
                padx=6,
                pady=2
            )
            chip.grid(row=row, column=col, padx=4, pady=3, sticky="w")

            # 텍스트
            tk.Label(
                chip,
                text=kw,
                bg=color,
                font=("맑은 고딕", 9)
            ).pack(side="left")

            # X 버튼
            tk.Button(
                chip,
                text="X",
                bg=color,
                bd=0,
                font=("맑은 고딕", 8, "bold"),
                command=lambda k=kw: self.remove_keyword(k)
            ).pack(side="left", padx=(4, 0))

        # column weight
        for c in range(max_per_row):
            self.selected_container.grid_columnconfigure(c, weight=0)

    def on_recommend(self):
        # 추천창 띄우고 메인창 숨기기 → 화면 전환 느낌
        RecommendationWindow(self.root, self.selected_keywords)
        self.root.withdraw()


root = tk.Tk()
app = MainApp(root)
root.mainloop()
