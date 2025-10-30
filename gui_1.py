import tkinter as tk
from tkinter import ttk

def recommend():
    selected = keyword_var.get()
    if selected == PLACEHOLDER:
        result_label.config(text="⚠️ 키워드를 먼저 선택해주세요.")
        return
    # TODO: 여기서 실제 추천 로직 연결
    result_label.config(text=f"‘{selected}’ 키워드에 맞는 국밥집 추천 중...")

# ---- 설정 ----
PLACEHOLDER = "키워드를 선택하세요"

# 두 팀이 만든 키워드 합쳐서 정리
keywords = [
    "가성비", "24시간", "부산역", "광안리", "혼밥", "전통",
    "맑은국물", "진한국물",  # A안
    "현지인 맛집", "진한 육수", "양 푸짐한", "혼밥하기 좋은"  # B안
]
# 중복/공백 정리 + 보기 좋은 순서(임의)
keywords = list(dict.fromkeys(keywords))

# ---- GUI ----
root = tk.Tk()
root.title("부산 국밥집 추천기")

ttk.Label(root, text="원하는 키워드 선택:").pack(pady=(12, 6))

keyword_var = tk.StringVar(value=PLACEHOLDER)
combo = ttk.Combobox(root, textvariable=keyword_var, state="readonly", width=30)
combo["values"] = [PLACEHOLDER] + keywords
combo.current(0)
combo.pack(pady=6)

ttk.Button(root, text="추천", command=recommend).pack(pady=10)

result_label = ttk.Label(root, text="")
result_label.pack(pady=(6, 12))

root.mainloop()
