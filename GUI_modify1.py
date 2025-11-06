import tkinter as tk
from tkinter import ttk

# 우리가 선택한 10개 국밥집 데이터
RESTAURANTS = [
    {"name": "본천돼지국밥", "area": "부산역"},
    {"name": "수변최고돼지국밥", "area": "민락본점"},
    {"name": "합천일류돼지국밥", "area": "사상"},
    {"name": "영진돼지국밥", "area": "신평"},
    {"name": "엄용백돼지국밥", "area": "해운대"},
    {"name": "합천국밥집", "area": "용호동"},
    {"name": "안목", "area": "남천동"},
    {"name": "60년전통 할매국밥", "area": "범일동"},
    {"name": "수라국밥", "area": "경성대점"},
    {"name": "쌍둥이국밥", "area": "본점"},
]

def show_recommend_frame():
    list_frame.pack_forget()
    recommend_frame.pack(fill="both", expand=True)

def show_list_frame():
    recommend_frame.pack_forget()
    list_frame.pack(fill="both", expand=True)

def recommend():
    selected_keyword = keyword_var.get()
    if not selected_keyword:
        result_label.config(text="키워드를 먼저 선택해주세요!")
    else:
        # 나중에 키워드 매칭 추천 로직이랑 연결하면 됨
        result_label.config(text=f"'{selected_keyword}'에 맞는 국밥집 추천 중...")

root = tk.Tk()
root.title("부산 국밥집 추천기")
root.geometry("480x320")

# 메뉴바
menubar = tk.Menu(root)

view_menu = tk.Menu(menubar, tearoff=0)
view_menu.add_command(label="키워드 추천 화면", command=show_recommend_frame)
view_menu.add_command(label="식당 리스트 보기", command=show_list_frame)

menubar.add_cascade(label="메뉴", menu=view_menu)
root.config(menu=menubar)

# 공통 스타일
style = ttk.Style()
style.configure("TLabel", font=("맑은 고딕", 11))
style.configure("TButton", font=("맑은 고딕", 10))
style.configure("Treeview.Heading", font=("맑은 고딕", 10, "bold"))

# 추천 화면 프레임
recommend_frame = ttk.Frame(root, padding=10)

ttk.Label(recommend_frame, text="다음 키워드 중 원하는 것을 선택하세요:").pack(pady=5)

keywords = ["가성비", "24시간", "역 근처", "혼밥", "전통", "맑은국물", "진한국물"]
keyword_var = tk.StringVar()

combo = ttk.Combobox(
    recommend_frame,
    textvariable=keyword_var,
    values=keywords,
    state="readonly",
    width=20
)
combo.pack(pady=5)

ttk.Button(recommend_frame, text="추천", command=recommend).pack(pady=10)

result_label = ttk.Label(recommend_frame, text="")
result_label.pack(pady=10)

# 식당 리스트 화면 프레임
list_frame = ttk.Frame(root, padding=10)

ttk.Label(list_frame, text="부산 국밥집 리스트 (팀이 선정한 10곳)").pack(pady=(0, 5))

columns = ("name", "area")
tree = ttk.Treeview(
    list_frame,
    columns=columns,
    show="headings",
    height=8
)

tree.heading("name", text="가게 이름")
tree.heading("area", text="지역")

tree.column("name", width=260)
tree.column("area", width=150, anchor="center")

for r in RESTAURANTS:
    tree.insert("", tk.END, values=(r["name"], r["area"]))

tree.pack(fill="both", expand=True, pady=5)

# 기본 화면은 추천 화면
recommend_frame.pack(fill="both", expand=True)

root.mainloop()