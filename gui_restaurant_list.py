import tkinter as tk
from tkinter import ttk
import os
import pandas as pd

from gui_detail import RestaurantDetail
from gui_recommended import GukbapRecommender


class RestaurantListWindow:
    """
    메인 화면의 메뉴(≡) 버튼에서 열리는 '전체 식당 리스트' 창.
    - 왼쪽 리스트박스에 식당 이름 나열
    - 더블클릭 or 버튼으로 상세창으로 이동
    """
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("든든한 국밥집 리스트")
        self.window.geometry("420x600")
        self.window.configure(bg="white")

        # 🔹 리스트창 X 버튼 → 메인으로 복귀
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # GukbapRecommender 재사용해서 식당 목록 가져오기
        self.recommender = GukbapRecommender()
        self.df = self.recommender.df  # '상호명' + 키워드 O/X 테이블

        self.build_ui()

    def on_close(self):
        """리스트창 닫으면 메인창 다시 보이기"""
        self.window.destroy()
        if self.parent is not None:
            self.parent.deiconify()

    def build_ui(self):
        # 헤더
        header = tk.Frame(self.window, bg="white")
        header.pack(fill="x", padx=15, pady=15)

        # 🔹 상단에 메뉴 버튼 추가 (추천 화면으로)
        menu_frame = tk.Frame(header, bg="white")
        menu_frame.pack(fill="x")

        tk.Button(
            menu_frame,
            text="≡  추천 화면",
            bg="white",
            bd=0,
            font=("맑은 고딕", 11, "bold"),
            command=self.on_close   # 눌렀을 때 메인으로 복귀
        ).pack(anchor="w")

        count = len(self.df)
        tk.Label(
            header,
            text=f"등록된 국밥집: {count}곳",
            font=("맑은 고딕", 14, "bold"),
            bg="white"
        ).pack(anchor="w", pady=(4, 0))

        tk.Label(
            header,
            text="식당을 선택하고 더블클릭 또는 아래 버튼을 눌러주세요.",
            font=("맑은 고딕", 9),
            fg="gray",
            bg="white"
        ).pack(anchor="w", pady=(2, 0))

        # 리스트 영역
        main = tk.Frame(self.window, bg="white")
        main.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.listbox = tk.Listbox(
            main,
            font=("맑은 고딕", 11),
            activestyle="none",
            height=20
        )
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(main, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.configure(yscrollcommand=scrollbar.set)

        # 리스트박스에 상호명 채우기
        if not self.df.empty and "상호명" in self.df.columns:
            for name in self.df["상호명"]:
                self.listbox.insert(tk.END, name)

        # 더블클릭 → 상세창
        self.listbox.bind("<Double-Button-1>", self.on_open_detail)

        # 하단 버튼
        bottom = tk.Frame(self.window, bg="white")
        bottom.pack(fill="x", padx=15, pady=(0, 12))

        ttk.Button(
            bottom,
            text="자세히 보기",
            command=self.on_open_detail
        ).pack(side="right")

    def on_open_detail(self, event=None):
        """선택된 식당의 상세창을 연다."""
        selection = self.listbox.curselection()
        if not selection:
            return

        index = selection[0]
        name = self.listbox.get(index)

        # df에서 해당 식당 행 찾기
        row = self.df[self.df["상호명"] == name].iloc[0]

        # 키워드 추출 (O인 컬럼들)
        keywords = [col for col in row.index if col != "상호명" and row[col] == "O"]

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

        win = tk.Toplevel(self.window)
        win.title(name)
        win.geometry("600x700")

        detail = RestaurantDetail(win, data)
        detail.pack(fill="both", expand=True)
