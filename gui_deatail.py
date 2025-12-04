import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from pathlib import Path

class RestaurantDetail(ttk.Frame):
    def __init__(self, parent, data: dict):
        super().__init__(parent, padding=12)
        self.data = data
        self._photo = None  # 이미지 참조 유지용
        self._build()

    def _build(self):
        # 스크롤 가능한 영역 기본 구조
        canvas = tk.Canvas(self, highlightthickness=0)
        scroll_y = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)

        inner = ttk.Frame(canvas)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)

        canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        # 헤더: 이미지 + 기본정보
        header = ttk.Frame(inner)
        header.pack(fill="x", pady=(0, 10))

        # 썸네일 영역
        thumb = tk.Canvas(header, width=150, height=110, bd=0,
                          highlightthickness=1, relief="ridge")
        thumb.pack(side="left", padx=(0, 12))

        img_path = self.data.get("photo_path")
        if img_path and Path(img_path).exists():
            try:
                # Tk 기본 PhotoImage (PNG/GIF)
                self._photo = tk.PhotoImage(file=img_path)

                # 비율 맞추기 (대충 중앙에 배치)
                thumb.create_image(75, 55, image=self._photo)
            except Exception:
                thumb.create_text(75, 55, text="이미지\n표시불가",
                                  font=("맑은 고딕", 10))
        else:
            thumb.create_rectangle(1, 1, 149, 109, outline="#cccccc")
            thumb.create_text(75, 55, text="IMAGE",
                              font=("맑은 고딕", 11, "bold"))

        # 텍스트 정보 영역
        info = ttk.Frame(header)
        info.pack(side="left", fill="x", expand=True)

        name = self.data.get("name", "가게 이름")
        ttk.Label(info, text=name, font=("맑은 고딕", 16, "bold")).pack(anchor="w")

        # 태그
        tags = self.data.get("tags", [])
        if tags:
            ttk.Label(info, text=" · ".join(tags),
                      foreground="#666666").pack(anchor="w", pady=(2, 0))

        # 평점
        rating = self.data.get("rating")
        review_count = self.data.get("review_count")
        price_range = self.data.get("price_range")

        rating_line = []
        if isinstance(rating, (int, float)):
            stars = "★" * int(round(rating)) + "☆" * (5 - int(round(rating)))
            rating_line.append(f"{stars} {rating:.1f}")
        if review_count:
            rating_line.append(f"({review_count:,}명)")
        # if price_range:
        #     rating_line.append(price_range)

        if rating_line:
            ttk.Label(info, text="  ".join(rating_line),
                      foreground="#f39c12").pack(anchor="w", pady=(2, 0))

        # 버튼 영역
        actions = ttk.Frame(inner)
        actions.pack(fill="x", pady=(0, 12))

        def _open(url, label):
            if url:
                webbrowser.open(url)
            else:
                messagebox.showinfo("알림", f"{label} 링크가 없습니다.")

        ttk.Button(
            actions,
            text="지도 열기",
            command=lambda: _open(self.data.get("map_url"), "지도")
        ).pack(side="left", padx=(0, 6))

        ttk.Button(
            actions,
            text="SNS / 카페",
            command=lambda: _open(self.data.get("sns_url"), "SNS/카페")
        ).pack(side="left", padx=6)

        # 기본 정보 섹션
        info_frame = ttk.LabelFrame(inner, text="기본 정보")
        info_frame.pack(fill="x", pady=(0, 10))

        def row(label, value):
            r = ttk.Frame(info_frame)
            r.pack(fill="x", pady=1)
            ttk.Label(r, text=label, width=8, anchor="w").pack(side="left")
            ttk.Label(r, text=value or "-", anchor="w").pack(side="left")

        row("전화", self.data.get("phone"))
        row("주소", self.data.get("address"))
        row("주차", "가능" if self.data.get("parking") else "불가")
        row("영업", self.data.get("hours_str"))

        # 메뉴 섹션 (Treeview 테이블)
        menu_frame = ttk.LabelFrame(inner, text="메뉴")
        menu_frame.pack(fill="x", pady=(0, 10))

        menu_list = self.data.get("menu", [])

        if not menu_list:
            ttk.Label(menu_frame, text="등록된 메뉴가 없습니다.",
                      foreground="#666666").pack(anchor="w", padx=6, pady=6)
        else:
            tv = ttk.Treeview(
                menu_frame,
                columns=("name", "price", "desc"),
                show="headings",
                height=6,
            )
            tv.heading("name", text="메뉴")
            tv.heading("price", text="가격")
            tv.heading("desc", text="설명")

            tv.column("name", width=160, anchor="w")
            tv.column("price", width=90, anchor="e")
            tv.column("desc", width=320, anchor="w")

            for m in menu_list:
                tv.insert(
                    "",
                    "end",
                    values=(
                        m.get("name", ""),
                        m.get("price", ""),
                        m.get("desc", ""),
                    ),
                )

            tv.pack(fill="x", padx=4, pady=4)

        # 리뷰 키워드 섹션
        kw_frame = ttk.LabelFrame(inner, text="리뷰 키워드")
        kw_frame.pack(fill="x", pady=(0, 10))

        keywords = self.data.get("keywords", [])
        if keywords:
            chips = ttk.Frame(kw_frame)
            chips.pack(fill="x", padx=4, pady=4)
            for k in keywords[:12]:
                chip = ttk.Label(
                    chips,
                    text=f"#{k}",
                    relief="groove",
                    padding=(6, 2)
                )
                chip.pack(side="left", padx=3, pady=2)
        else:
            ttk.Label(kw_frame, text="아직 정리된 키워드가 없습니다.",
                      foreground="#666666").pack(anchor="w", padx=6, pady=6)


