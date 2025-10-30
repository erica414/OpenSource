import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

# ---------------- 색상 팔레트 ----------------
BG_COLOR       = "#F6F1E7"   # 크림톤 한지색
CARD_BG        = "#FBF7EE"
WOOD_BROWN     = "#8B5E34"   # 갈색
ACCENT_BRICK   = "#B85C38"   # 벽돌색 포인트
SUBTEXT        = "#4A4036"
PLACEHOLDER    = "키워드를 선택하세요"

# ---------------- 키워드 목록 ----------------
keywords = [
    "가성비", "24시간", "부산역", "광안리", "혼밥", "전통",
    "맑은국물", "진한국물", "현지인 맛집", "진한 육수", "양 푸짐한", "혼밥하기 좋은"
]
keywords = list(dict.fromkeys(keywords))  # 중복 제거

# ---------------- 함수 ----------------
def recommend():
    selected = keyword_var.get()
    if selected == PLACEHOLDER:
        result_label.config(text="⚠️ 키워드를 먼저 선택해주세요.")
        return
    result_label.config(
        text=f"‘{selected}’ 키워드에 맞는 국밥집 추천 중..."
    )

# ---------------- 폰트 자동 선택 ----------------
def pick_korean_font(root):
    candidates = ["나눔명조", "본고딕", "Noto Serif CJK KR", "서울남산체", "맑은 고딕"]
    available = set(tkfont.families(root))
    for f in candidates:
        if f in available:
            return f
    return "TkDefaultFont"

# ---------------- GUI ----------------
root = tk.Tk()
root.title("🍲 부산 국밥집 추천기")
root.geometry("480x340")
root.configure(bg=BG_COLOR)
root.eval('tk::PlaceWindow . center')

base_font = pick_korean_font(root)

# 카드 프레임
card = tk.Frame(root, bg=CARD_BG, bd=2, relief="ridge")
card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=250)

# 제목
tk.Label(card, text="부산 국밥집 추천기", bg=CARD_BG, fg=WOOD_BROWN,
         font=(base_font, 18, "bold")).pack(pady=(20, 8))

# 안내문
tk.Label(card, text="다음 키워드 중 원하는 것을 선택하세요:",
         bg=CARD_BG, fg=SUBTEXT, font=(base_font, 11)).pack(pady=(0, 8))

# 콤보박스
keyword_var = tk.StringVar(value=PLACEHOLDER)
combo = ttk.Combobox(card, textvariable=keyword_var, state="readonly", width=28)
combo["values"] = [PLACEHOLDER] + keywords
combo.current(0)
combo.pack(pady=5)

# 추천 버튼
btn = tk.Button(card, text="추천 🍚", command=recommend,
                bg=ACCENT_BRICK, fg="white", activebackground="#8C3A25",
                activeforeground="white", relief="raised",
                font=(base_font, 11, "bold"), padx=10, pady=4)
btn.pack(pady=10)

# 결과 라벨
result_label = tk.Label(card, text="", bg=CARD_BG, fg=ACCENT_BRICK,
                        font=(base_font, 12, "bold"), wraplength=360, justify="center")
result_label.pack(pady=(10, 5))

# 푸터
tk.Label(card, text="따뜻~하게 한 그릇 하고 가이소 😊", bg=CARD_BG,
         fg=SUBTEXT, font=(base_font, 9)).pack(side="bottom", pady=8)

root.mainloop()
