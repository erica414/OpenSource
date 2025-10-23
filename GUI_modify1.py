import tkinter as tk
from tkinter import ttk

# (기존) 추천 함수: 내부에서 entry.get() 대신 콤보박스의 선택값을 사용
def recommend():
    selected = keyword_var.get()
    if selected == "키워드를 선택하세요":
        result_label.config(text="⚠️ 키워드를 먼저 선택해주세요.")
    else:
        # 나중에 키워드 매칭 코드와 연결 예정
        result_label.config(text=f"'{selected}'에 맞는 국밥집 추천 중...")

root = tk.Tk()
root.title("부산 국밥집 추천기")

# 기존 라벨 유지
ttk.Label(root, text="원하는 키워드 선택:").pack(pady=5)

# 🔽 변경 포인트: Entry → Combobox (보기에서 선택)
keyword_var = tk.StringVar()
keyword_box = ttk.Combobox(root, textvariable=keyword_var, state="readonly", width=38)
keyword_box["values"] = (
    "키워드를 선택하세요",
    "현지인 맛집",
    "진한 육수",
    "양 푸짐한",
    "혼밥하기 좋은",
)
keyword_box.current(0)
keyword_box.pack(pady=5)

# 기존 버튼/라벨 유지 (텍스트만 살짝 변경)
ttk.Button(root, text="추천", command=recommend).pack(pady=10)
result_label = ttk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()
