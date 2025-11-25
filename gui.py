import tkinter as tk
from tkinter import ttk

def recommend():
    selected_keyword = keyword_var.get()
    if not selected_keyword:
        result_label.config(text="키워드를 먼저 선택해주세요!")
    else:
        # 나중에 키워드 매칭 코드랑 연결
        result_label.config(text=f"'{selected_keyword}'에 맞는 국밥집 추천 중...")

root = tk.Tk()
root.title("부산 국밥집 추천기")

# 안내 문구
ttk.Label(root, text="다음 키워드 중 원하는 것을 선택하세요:").pack(pady=5)

# 선택 가능한 키워드 목록
keywords = ["가성비", "24시간", "역 근처", "혼밥", "전통", "맑은국물", "진한국물"]
keyword_var = tk.StringVar()

# 콤보박스 생성
combo = ttk.Combobox(root, textvariable=keyword_var, values=keywords, state="readonly", width=20)
combo.pack(pady=5)

# 추천 버튼
ttk.Button(root, text="추천", command=recommend).pack(pady=10)

# 결과 출력
result_label = ttk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()
