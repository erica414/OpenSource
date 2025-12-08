import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
IMG_DIR = BASE_DIR / "img"


class RestaurantDetail(tk.Toplevel):
    """
    식당 하나에 대한 상세 정보를 보여주는 창.
    - 리스트/추천 쪽에서 호출
    - 자기 자신(Toplevel)만 띄우고, 닫힐 때는 부모창 deiconify()
    """

    CSV_PATH = BASE_DIR / "restaurant_info.csv"  # 템플릿 CSV 위치

    def __init__(self, parent_window, data: dict):
        super().__init__(parent_window)
        self.parent_window = parent_window
        self.title(data.get("name", "국밥집 정보"))
        self.geometry("1400x750")
        self.configure(bg="white")

        # 창 닫을 때 → 이전 창 다시 보이게
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # CSV 데이터와 머지
        merged = self._merge_with_csv(data)
        self.data = merged
        self._photo = None  # 이미지 참조 유지용

        self._build()

    # ---------- CSV 로더 ----------
    @staticmethod
    def load_from_csv(name: str, csv_path: str | None = None) -> dict:
        """
        주어진 상호명(name)에 해당하는 정보를 CSV 에서 읽어 dict 로 반환.
        없으면 {} 반환.
        """
        if not name:
            return {}

        if csv_path is None:
            csv_path = RestaurantDetail.CSV_PATH

        path = Path(csv_path)
        if not path.is_absolute():
            path = BASE_DIR / path

        if not path.exists():
            return {}

        # CSV 로드
        try:
            df = pd.read_csv(path, encoding="utf-8-sig")
        except Exception:
            df = pd.read_csv(path)

        # --- 이름 컬럼 정리 (name / 상호명 둘 다 허용) ---
        if "name" not in df.columns:
            if "상호명" in df.columns:
                df = df.rename(columns={"상호명": "name"})
            else:
                return {}

        # 공백 제거 후 이름 매칭
        df["name"] = df["name"].astype(str).str.strip()
        target_name = str(name).strip()

        # ---- 기타 컬럼 alias 처리 ----
        # 이미지: image_file / photo / image / img / 사진 / 이미지 등 허용
        if "photo_path" not in df.columns:
            for cand in ("image_file", "photo", "image", "img", "사진", "이미지"):
                if cand in df.columns:
                    df["photo_path"] = df[cand]
                    break

        # 전화번호: call / 전화번호 / 전화
        if "phone" not in df.columns:
            for cand in ("call", "전화번호", "전화"):
                if cand in df.columns:
                    df["phone"] = df[cand]
                    break

        # 영업 시간: opening_hours / 영업시간 / 운영시간
        if "hours_str" not in df.columns:
            for cand in ("opening_hours", "영업시간", "운영시간"):
                if cand in df.columns:
                    df["hours_str"] = df[cand]
                    break

        row = df.loc[df["name"] == target_name]
        if row.empty:
            return {}

        return row.iloc[0].to_dict()

    def _merge_with_csv(self, base: dict) -> dict:
        """
        추천/리스트 쪽에서 전달한 data 와 CSV 데이터(headline, 메뉴, 링크 등)를 합침.
        base 가 우선권을 갖고, 비어 있는 값은 CSV 로 채움.
        """
        name = base.get("name")
        csv_data = RestaurantDetail.load_from_csv(name) if name else {}

        merged = dict(csv_data)
        merged.update({k: v for k, v in base.items() if v is not None})

        # keywords, tags 는 문자열 or 리스트 모두 처리
        for key in ("keywords", "tags"):
            val = merged.get(key)
            if isinstance(val, float):  # NaN 같은 것
                merged[key] = ""

        return merged

    # ---------- UI ----------
    def _build(self):
        # 스크롤 가능한 전체 영역
        root_frame = tk.Frame(self, bg="white")
        root_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(root_frame, bg="white", highlightthickness=0)
        scroll_y = ttk.Scrollbar(root_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll_y.set)

        canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        main = tk.Frame(canvas, bg="white")
        canvas_window = canvas.create_window((0, 0), window=main, anchor="nw")

        main.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

        # ===== 헤더 (이미지 + 이름 + 키워드 요약 + 버튼) =====
        header = tk.Frame(main, bg="white")
        header.pack(fill="x", padx=20, pady=(15, 10))

        # 이미지 썸네일
        thumb = tk.Canvas(header, width=150, height=110, bg="#f7f7f7", highlightthickness=0)
        thumb.pack(side="left", padx=(0, 20))

        photo_path = self.data.get("photo_path")
        if isinstance(photo_path, str) and photo_path.strip():
            try:
                from PIL import Image, ImageTk
                p = Path(photo_path)

                # 절대 경로가 아니면 우리 프로젝트 기준으로 다시 해석
                if not p.is_absolute():
                    # 1) img/ 안에서 파일명 기준으로 찾기
                    candidate = IMG_DIR / p.name
                    if candidate.exists():
                        p = candidate
                    else:
                        # 2) 예전처럼 상대 경로가 들어온 경우 대비
                        p = (BASE_DIR / p).resolve()

                img = Image.open(p)
                img = img.resize((150, 110))
                self._photo = ImageTk.PhotoImage(img)
                thumb.create_image(75, 55, image=self._photo)
            except Exception as e:
                print("디테일 이미지 로드 오류:", e)
                thumb.create_text(75, 55, text="이미지\n표시불가", font=("맑은 고딕", 10))
        else:
            thumb.create_rectangle(1, 1, 149, 109, outline="#cccccc")
            thumb.create_text(75, 55, text="IMAGE", font=("맑은 고딕", 11, "bold"))

        # 텍스트 정보
        info = tk.Frame(header, bg="white")
        info.pack(side="left", fill="x", expand=True)

        name = self.data.get("name", "가게 이름")
        tk.Label(info, text=name, font=("맑은 고딕", 18, "bold"), bg="white").pack(anchor="w")

        # 상단 키워드 요약
        tags = self.data.get("tags") or self.data.get("keywords") or ""
        if isinstance(tags, str):
            tag_list = [t for t in tags.split("|") if t.strip()]
        elif isinstance(tags, list):
            tag_list = tags
        else:
            tag_list = []

        tag_text = " · ".join(tag_list)
        tk.Label(
            info,
            text=tag_text if tag_text else "키워드 정보 없음",
            font=("맑은 고딕", 10),
            fg="#555555",
            bg="white",
            wraplength=600,
            justify="left"
        ).pack(anchor="w", pady=(4, 0))

        # 링크 버튼들
        btn_row = tk.Frame(info, bg="white")
        btn_row.pack(anchor="w", pady=(8, 0))

        tk.Button(
            btn_row,
            text="지도 열기",
            font=("맑은 고딕", 9),
            bg="#f5f5f5",
            relief="groove",
            command=self.open_map
        ).pack(side="left", padx=(0, 5))

        tk.Button(
            btn_row,
            text="SNS / 카페",
            font=("맑은 고딕", 9),
            bg="#f5f5f5",
            relief="groove",
            command=self.open_sns
        ).pack(side="left", padx=(0, 5))

        # ===== 기본 정보 =====
        self._build_basic_info(main)
        self._build_menu(main)
        self._build_keywords(main)

    # ---------- 섹션들 ----------
    def _build_basic_info(self, parent):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", padx=20, pady=(10, 5))

        tk.Label(frame, text="기본 정보", font=("맑은 고딕", 12, "bold"),
                 bg="white").pack(anchor="w", pady=(0, 4))

        info_box = tk.Frame(frame, bg="#fafafa", bd=1, relief="solid")
        info_box.pack(fill="x")

        def row(label, key):
            val = self.data.get(key)
            text = "-" if not isinstance(val, str) or not val.strip() else val.strip()
            r = tk.Frame(info_box, bg="#fafafa")
            r.pack(fill="x", padx=10, pady=2)
            tk.Label(r, text=f"{label} ", width=6,
                     anchor="w", bg="#fafafa",
                     font=("맑은 고딕", 9, "bold")).pack(side="left")
            tk.Label(r, text=text, anchor="w", bg="#fafafa",
                     font=("맑은 고딕", 9)).pack(side="left")

        row("전화", "phone")
        row("주소", "address")
        row("주차", "parking")
        row("영업", "hours_str")
        if "memo" in self.data:
            row("비고", "memo")

    def _build_menu(self, parent):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", padx=20, pady=(10, 5))

        tk.Label(frame, text="메뉴", font=("맑은 고딕", 12, "bold"),
                 bg="white").pack(anchor="w", pady=(0, 4))

        menu_box = tk.Frame(frame, bg="#fafafa", bd=1, relief="solid")
        menu_box.pack(fill="x")

        menu_str = self.data.get("menu")
        if not isinstance(menu_str, str) or not menu_str.strip():
            tk.Label(
                menu_box,
                text="등록된 메뉴가 없습니다.",
                bg="#fafafa",
                font=("맑은 고딕", 9),
                fg="#666666"
            ).pack(anchor="w", padx=10, pady=6)
            return

        """
        menu 형식 예시 (CSV 에 이렇게 넣으면 됨)
        돼지국밥:9000:대표 메뉴|순대국밥:9500:보통|수육백반:12000:
        -> 이름:가격:설명 (설명은 없어도 됨)
        """

        for item in menu_str.split("|"):
            item = item.strip()
            if not item:
                continue
            parts = item.split(":")
            name = parts[0].strip()
            price = parts[1].strip() if len(parts) > 1 else ""
            desc = parts[2].strip() if len(parts) > 2 else ""

            row = tk.Frame(menu_box, bg="#fafafa")
            row.pack(fill="x", padx=10, pady=2)

            left = tk.Label(row, text=name, bg="#fafafa",
                            font=("맑은 고딕", 9, "bold"))
            left.pack(side="left")

            if price:
                tk.Label(
                    row,
                    text=f"{price}원",
                    bg="#fafafa",
                    font=("맑은 고딕", 9)
                ).pack(side="left", padx=(8, 0))

            if desc:
                tk.Label(
                    row,
                    text=f"- {desc}",
                    bg="#fafafa",
                    font=("맑은 고딕", 9),
                    fg="#666666"
                ).pack(side="left", padx=(6, 0))

    def _build_keywords(self, parent):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", padx=20, pady=(10, 20))

        tk.Label(frame, text="리뷰 키워드", font=("맑은 고딕", 12, "bold"),
                 bg="white").pack(anchor="w", pady=(0, 4))

        box = tk.Frame(frame, bg="#fafafa", bd=1, relief="solid")
        box.pack(fill="x")

        kw_raw = self.data.get("keywords") or ""
        if isinstance(kw_raw, str):
            keywords = [k.strip() for k in kw_raw.split("|") if k.strip()]
        elif isinstance(kw_raw, list):
            keywords = kw_raw
        else:
            keywords = []

        if not keywords:
            tk.Label(
                box,
                text="아직 정리된 키워드가 없습니다.",
                bg="#fafafa",
                font=("맑은 고딕", 9),
                fg="#666666"
            ).pack(anchor="w", padx=10, pady=6)
            return

        chips = tk.Frame(box, bg="#fafafa")
        chips.pack(fill="x", padx=8, pady=6)

        for k in keywords:
            lbl = tk.Label(
                chips,
                text=f"#{k}",
                bg="white",
                bd=1,
                relief="solid",
                font=("맑은 고딕", 9),
                padx=6, pady=2
            )
            lbl.pack(side="left", padx=3, pady=3)

    # ---------- 링크 열기 ----------
    def open_map(self):
        url = self.data.get("map_url")
        if isinstance(url, str) and url.strip():
            webbrowser.open(url.strip())
        else:
            messagebox.showinfo("안내", "등록된 지도 링크가 없습니다.")

    def open_sns(self):
        url = self.data.get("sns_url")
        if isinstance(url, str) and url.strip():
            webbrowser.open(url.strip())
        else:
            messagebox.showinfo("안내", "등록된 SNS/카페 링크가 없습니다.")

    # ---------- 창 닫기 ----------
    def on_close(self):
        """디테일 창을 닫을 때 → 부모(리스트 or 추천) 다시 보이게."""
        self.parent_window.deiconify()
        self.destroy()


