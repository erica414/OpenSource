import tkinter as tk
from tkinter import ttk

def recommend():
    user_input = entry.get()
    # 나중에 키워드 매칭 코드랑 연결
    result_label.config(text=f"'{user_input}'에 맞는 국밥집 추천 중...")

root = tk.Tk()
root.title("부산 국밥집 추천기")
ttk.Label(root, text="원하는 키워드 입력:").pack(pady=5)
entry = ttk.Entry(root, width=40)
entry.pack(pady=5)
ttk.Button(root, text="추천", command=recommend).pack(pady=10)
result_label = ttk.Label(root, text="")
result_label.pack(pady=10)
root.mainloop()
