import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk

from gui_detail import RestaurantDetail
from gui_recommended import GukbapRecommender

BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "img"


class RestaurantListWindow:
    """
    메인화면의 메뉴(≡) 버튼에서 열리는 '전체 식당 리스트' 창.
    - 카드형 리스트
    - 이미지 자리 + 키워드 요약 + [자세히 보기] 버튼
    - 리스트 <-> 디테일, 한 화면만 보이도록 전환
    """
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("든든한 국밥집 리스트")
        self.window.geometry("1400x750")
        self.window.configure(bg="white")

        # X 눌렀을 때 → 리스트 닫고 메인 복귀
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # 데이터 로드 (추천에서 쓰는 df 재사용)
        self.recommender = GukbapRecommender()
        self.df = self.recommender.df  # '상호명' + 키워드 O/X

        self._thumb_images: list[ImageTk.PhotoImage] = []  # 썸네일 참조 유지용

        self._build_header()
        self._build_cards()

    # ----------------- 헤더 -----------------
    def _build_header(self):
        header = tk.Frame(self.window, bg="white")
        header.pack(side="top", fill="x", padx=10, pady=8)

        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=0)
        header.columnconfigure(2, weight=1)

        # 메뉴(=메인으로) 버튼
        menu_frame = tk.Frame(header, bg="white")
        menu_frame.grid(row=0, column=0, sticky="w")

        tk.Button(
            menu_frame,
            text="≡",
            bg="white",
            bd=0,
            font=("맑은 고딕", 20, "bold"),
            command=self.go_home
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
            text="든든한 국밥집 리스트",
            font=("맑은 고딕", 24, "bold"),
            bg="white"
        ).pack(side="left")

        # 오른쪽 여백
        right_space = tk.Frame(header, bg="white")
        right_space.grid(row=0, column=2, sticky="e")

        # 서브 텍스트
        info_frame = tk.Frame(self.window, bg="white")
        info_frame.pack(fill="x", padx=40, pady=(0, 5))

        count = len(self.df) if self.df is not None else 0
        tk.Label(
            info_frame,
            text=f"등록된 국밥집: {count}곳",
            font=("맑은 고딕", 12, "bold"),
            bg="white"
        ).pack(anchor="w")

        tk.Label(
            info_frame,
            text="카드를 클릭하거나 [자세히 보기] 버튼을 눌러 상세 정보를 확인해 보세요.",
            font=("맑은 고딕", 10),
            fg="gray",
            bg="white"
        ).pack(anchor="w")

    # ----------------- 카드 영역(스크롤) -----------------
    def _build_cards(self):
        wrapper = tk.Frame(self.window, bg="white")
        wrapper.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        canvas = tk.Canvas(wrapper, bg="white", highlightthickness=0)
        vscroll = ttk.Scrollbar(wrapper, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vscroll.set)

        canvas.pack(side="left", fill="both", expand=True)
        vscroll.pack(side="right", fill="y")

        self.card_area = tk.Frame(canvas, bg="white")
        self.canvas_window = canvas.create_window((0, 0), window=self.card_area, anchor="nw")

        # 스크롤 영역 자동 조정 + 폭 맞추기
        self.card_area.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(self.canvas_window, width=e.width)
        )

        # 카드들 생성
        if self.df is None or self.df.empty:
            tk.Label(
                self.card_area,
                text="등록된 국밥집이 없습니다.",
                font=("맑은 고딕", 12),
                bg="white"
            ).pack(pady=40)
            return

        # 키워드 O인 것만 뽑아서 한 줄 문자열로 만들어 사용
        keyword_cols = [c for c in self.df.columns if c != "상호명"]

        for _, row in self.df.iterrows():
            name = row["상호명"]
            keywords = [col for col in keyword_cols if str(row[col]).upper() == "O"]
            self._create_card(name, keywords)

    def _create_card(self, name, keywords):
        """식당 하나당 카드 1개 생성."""
        card = tk.Frame(
            self.card_area,
            bg="white",
            bd=1,
            relief="solid",
            highlightthickness=0
        )
        card.pack(fill="x", pady=6)

        card.columnconfigure(1, weight=1)  # 가운데 정보영역 늘어나도록

        # 썸네일 자리
        thumb = tk.Canvas(card, width=90, height=90, bg="#fafafa", highlightthickness=0)
        thumb.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        # restaurant_info.csv 에서 이미지 경로 가져오기
        info_data = RestaurantDetail.load_from_csv(name)
        photo_path = None
        if info_data:
            photo_path = info_data.get("photo_path")

        if isinstance(photo_path, str) and photo_path.strip():
            try:
                p = Path(photo_path)
                if not p.is_absolute():
                    candidate = IMG_DIR / p.name
                    if candidate.exists():
                        p = candidate
                    else:
                        p = (BASE_DIR / p).resolve()

                img = Image.open(p).resize((90, 90), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                thumb.create_image(45, 45, image=photo)
                self._thumb_images.append(photo)   # GC 방지
            except Exception as e:
                print("리스트 썸네일 로드 오류:", e)
                thumb.create_rectangle(5, 5, 85, 85, outline="#cccccc")
                thumb.create_text(45, 45, text="IMG", font=("맑은 고딕", 9))
        else:
            thumb.create_rectangle(5, 5, 85, 85, outline="#cccccc")
            thumb.create_text(45, 45, text="IMG", font=("맑은 고딕", 9))

        # 텍스트 정보
        info = tk.Frame(card, bg="white")
        info.grid(row=0, column=1, sticky="w", pady=(10, 0), padx=(5, 0))

        tk.Label(
            info,
            text=name,
            font=("맑은 고딕", 13, "bold"),
            bg="white"
        ).pack(anchor="w")

        kw_str = " · ".join(keywords) if keywords else "키워드 정보 없음"
        tk.Label(
            info,
            text=kw_str,
            font=("맑은 고딕", 10),
            fg="#555555",
            bg="white",
            wraplength=750,
            justify="left"
        ).pack(anchor="w", pady=(4, 0))

        # [자세히 보기] 버튼
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.grid(row=0, column=2, rowspan=2, sticky="e", padx=12, pady=10)

        tk.Button(
            btn_frame,
            text="자세히 보기",
            font=("맑은 고딕", 10),
            bg="#f5f5f5",
            relief="groove",
            command=lambda n=name: self.open_detail(n)
        ).pack()

        # 카드 전체를 클릭해도 열리게
        card.bind("<Button-1>", lambda e, n=name: self.open_detail(n))
        thumb.bind("<Button-1>", lambda e, n=name: self.open_detail(n))
        info.bind("<Button-1>", lambda e, n=name: self.open_detail(n))

    # ----------------- 화면 전환/닫기 -----------------
    def open_detail(self, name):
        """
        리스트창은 숨기고, 디테일 Toplevel 하나만 보이게.
        디테일에서 닫으면 다시 이 리스트창으로 복귀.
        """
        data = RestaurantDetail.load_from_csv(name)
        if not data:
            data = {"name": name, "keywords": []}

        self.window.withdraw()
        RestaurantDetail(self.window, data)

    def go_home(self):
        """메인(추천) 화면으로 돌아가기."""
        self.window.destroy()
        self.parent.deiconify()

    def on_close(self):
        """리스트 X 버튼 → 메인으로 복귀."""
        self.parent.deiconify()
        self.window.destroy()

        detail = RestaurantDetail(win, data)
        detail.pack(fill="both", expand=True)

