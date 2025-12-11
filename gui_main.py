import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # pip install pillow

from gui_recommended import RecommendationWindow
from gui_restaurant_list import RestaurantListWindow

from pathlib import Path   # ← 추가

# 프로젝트 기준 폴더 & img 폴더
BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "img"

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
        self.root.geometry("1400x750")  # 메인 화면 사이즈
        self.root.configure(bg="white")

        # 선택된 키워드: 순서를 유지하기 위해 list 사용
        self.selected_keywords = []
        # 키워드 → 버튼 위젯 매핑 (색 변경/hover용)
        self.keyword_buttons = {}
        # 키워드 → 카테고리 매핑
        self.keyword_to_category = self.build_keyword_category_map()

        self.build_header()
        self.build_center_area()     # 스크롤 가능한 중앙 영역
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

        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=0)
        header.columnconfigure(2, weight=1)

        # 메뉴 버튼
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

        # 로고 + 제목
        title_frame = tk.Frame(header, bg="white")
        title_frame.grid(row=0, column=1)

        try:
            logo_img = Image.open(IMG_DIR / "deundeun_logo.png").resize((100, 60), Image.LANCZOS)
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

        # 오른쪽 여백
        right_space = tk.Frame(header, bg="white")
        right_space.grid(row=0, column=2, sticky="e")

    def on_menu_click(self):
        RestaurantListWindow(self.root)
        self.root.withdraw()

    # ---------- 스크롤 가능한 가운데 영역 ----------
    def build_center_area(self):
        wrapper = tk.Frame(self.root, bg="white")
        wrapper.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(wrapper, bg="white", highlightthickness=0)
        vscroll = ttk.Scrollbar(wrapper, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vscroll.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        vscroll.pack(side="right", fill="y")

        self.center = tk.Frame(self.canvas, bg="white")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.center, anchor="nw")

        self.center.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        tk.Label(
            self.center,
            text="키워드를 선택하여 기호에 맞는 국밥집을 찾아보세요!",
            font=("맑은 고딕", 12),
            bg="white"
        ).pack(pady=(0, 10))

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ---------- 키워드 선택 영역 ----------
    def build_keyword_section(self):
        kw_outer = tk.Frame(self.center, bg="white")
        kw_outer.pack(pady=(0, 10), fill="x")

        for idx, (cat, kws) in enumerate(CATEGORY_KEYWORDS.items()):
            row = tk.Frame(kw_outer, bg="white")
            row.pack(fill="x", pady=6, padx=60)

            # 왼쪽 카테고리 박스
            color = CATEGORY_COLORS.get(cat, "#eeeeee")
            cat_box = tk.Frame(row, bg=color, width=120, height=40, bd=1, relief="solid")
            cat_box.pack(side="left", padx=(0, 20))
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
                    width=15,
                    font=("맑은 고딕", 10),
                    relief="groove",
                    bg="white",
                    activebackground="#e0e0ff",
                    command=lambda k=kw: self.toggle_keyword(k)
                )
                btn.pack(side="left", padx=4, pady=3)

                self.keyword_buttons[kw] = btn
                btn.bind("<Enter>", lambda e, k=kw: self.on_keyword_hover_in(k))
                btn.bind("<Leave>", lambda e, k=kw: self.on_keyword_hover_out(k))

    # ---------- 선택된 키워드 표시 영역 ----------
    def build_selected_section(self):
        box_outer = tk.Frame(self.center, bg="white")
        box_outer.pack(fill="x", padx=60, pady=(0, 15))

        top_row = tk.Frame(box_outer, bg="white")
        top_row.pack(fill="x")

        tk.Label(
            top_row,
            text="선택된 키워드:",
            font=("맑은 고딕", 11),
            bg="white"
        ).pack(side="left", pady=(0, 3))

        tk.Button(
            top_row,
            text="전체 삭제",
            font=("맑은 고딕", 9),
            bg="#f5f5f5",
            relief="groove",
            command=self.clear_all_keywords
        ).pack(side="right", padx=(0, 2))

        self.selected_box = tk.Frame(box_outer, bg="white", bd=1, relief="solid")
        self.selected_box.pack(fill="x", padx=2, pady=(4, 5))

        self.selected_container = tk.Frame(self.selected_box, bg="white")
        self.selected_container.pack(fill="x", padx=8, pady=6)

        self.refresh_selected_chips()

    # ---------- 추천 버튼 ----------
    def build_recommend_button(self):
        tk.Button(
            self.center,
            text="추천",
            font=("맑은 고딕", 13, "bold"),
            bg="#cfe2ff",
            activebackground="#cfe2ff",
            relief="ridge",
            padx=20, pady=8,
            command=self.on_recommend
        ).pack(pady=(0, 15))

    # ---------- hover 효과 ----------
    def on_keyword_hover_in(self, kw):
        btn = self.keyword_buttons.get(kw)
        if not btn:
            return
        if kw in self.selected_keywords:
            btn.configure(bg="#cccccc")
        else:
            btn.configure(bg="#e0e0ff")

    def on_keyword_hover_out(self, kw):
        btn = self.keyword_buttons.get(kw)
        if not btn:
            return
        if kw in self.selected_keywords:
            btn.configure(bg="#d9d9d9")
        else:
            btn.configure(bg="white")

    # ---------- 키워드 토글 / 칩 표시 ----------
    def toggle_keyword(self, kw):
        if kw in self.selected_keywords:
            self.selected_keywords.remove(kw)
        else:
            self.selected_keywords.append(kw)

        btn = self.keyword_buttons.get(kw)
        if btn:
            if kw in self.selected_keywords:
                btn.configure(bg="#d9d9d9")
            else:
                btn.configure(bg="white")

        self.refresh_selected_chips()

    def clear_all_keywords(self):
        self.selected_keywords.clear()
        for kw, btn in self.keyword_buttons.items():
            btn.configure(bg="white")
        self.refresh_selected_chips()

    def remove_keyword(self, kw):
        if kw in self.selected_keywords:
            self.selected_keywords.remove(kw)

        btn = self.keyword_buttons.get(kw)
        if btn:
            btn.configure(bg="white")

        self.refresh_selected_chips()

    def refresh_selected_chips(self):
        # 기존 칩 제거
        for w in self.selected_container.winfo_children():
            w.destroy()

        # 아무것도 없을 때
        if not self.selected_keywords:
            tk.Label(
                self.selected_container,
                text="키워드를 선택하세요.",
                bg="white",
                font=("맑은 고딕", 10),
                fg="gray"
            ).grid(row=0, column=0, sticky="w")
            return

        # 🔹 한 줄에 7개, "열 폭"을 통일해서 맞추기
        max_per_row = 9
        CHIP_WIDTH = 135  # 각 칩이 차지할 열 폭(픽셀 기준)

        # 열 설정: 모든 column에 같은 minsize를 줘서 폭 통일
        for c in range(max_per_row):
            self.selected_container.grid_columnconfigure(c, weight=0, minsize=CHIP_WIDTH)

        for i, kw in enumerate(self.selected_keywords):
            row = i // max_per_row
            col = i % max_per_row

            cat = self.keyword_to_category.get(kw)
            color = CATEGORY_COLORS.get(cat, "#eeeeee")

            # 폭은 열에서 관리하므로 여기선 width 안 줘도 됨
            chip = tk.Frame(
                self.selected_container,
                bg=color,
                bd=1,
                relief="solid",
                padx=6,
                pady=2,
            )
            chip.grid(row=row, column=col, padx=4, pady=3, sticky="nsew")

            lbl = tk.Label(
                chip,
                text=kw,
                bg=color,
                font=("맑은 고딕", 9),
                anchor="w"
            )
            lbl.pack(side="left", padx=(2, 0), fill="x", expand=True)

            tk.Button(
                chip,
                text="X",
                bg=color,
                bd=0,
                font=("맑은 고딕", 8, "bold"),
                width=2,
                command=lambda k=kw: self.remove_keyword(k)
            ).pack(side="right", padx=(4, 2))

    def on_recommend(self):
        RecommendationWindow(self.root, self.selected_keywords)
        self.root.withdraw()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
