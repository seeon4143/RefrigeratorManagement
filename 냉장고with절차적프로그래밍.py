import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import os

# ==========================================
# 전역 상태 (Global State) 변수 초기화
# ==========================================
FILENAME = "food_list.txt"
today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
items = []

edit_mode = False
delete_mode = False
adding_item = None
entries = []
new_row_vars = {}

# UI 위젯을 담을 전역 변수 (setup_ui에서 할당됨)
root = None
canvas = None
table_frame = None
btn_edit = None
btn_delete = None
btn_add = None
list_canvas = None
status_bar = None

# ==========================================
# 소비기한 예측용 기본 보관 기간 딕셔너리
# ==========================================
DEFAULT_SHELF_LIFE = {
    # 육류
    "닭": 3, "돼지": 4, "소": 5, "삼겹": 4, "갈비": 4, "불고기": 4,
    "햄": 7, "소시지": 7, "베이컨": 7,
    # 해산물
    "생선": 2, "고등어": 2, "연어": 2, "참치": 2, "오징어": 2, "새우": 2,
    # 유제품·달걀
    "우유": 7, "계란": 14, "달걀": 14, "치즈": 14, "버터": 30, "요거트": 10,
    # 두부·콩류
    "두부": 5, "콩": 30,
    # 채소
    "시금치": 4, "상추": 4, "양상추": 5, "배추": 14, "무": 14,
    "당근": 21, "감자": 30, "양파": 30, "마늘": 30,
    # 과일
    "딸기": 4, "바나나": 5, "사과": 14, "배": 14, "귤": 14, "오렌지": 14,
    # 가공식품
    "김치": 30, "된장": 180, "고추장": 180, "간장": 365,
    "아이스크림": 180, "냉동만두": 90, "냉동밥": 30,
}

STORAGE_OPTIONS = ["냉장", "냉동", "실온"]

# ==========================================
# 데이터 처리 함수
# ==========================================
def load_data():
    global items
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w", encoding="utf-8") as f:
            pass
        return
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('\\')
                if len(parts) == 4:
                    items.append({
                        "name": parts[0], "qty": parts[1],
                        "exp": parts[2], "storage": parts[3]
                    })
    except Exception as e:
        print(f"파일 로드 오류: {e}")

def save_data():
    try:
        with open(FILENAME, "w", encoding="utf-8") as f:
            for item in items:
                f.write(f"{item['name']}\\{item['qty']}\\{item['exp']}\\{item['storage']}\n")
    except Exception as e:
        messagebox.showerror("저장 오류", f"오류 발생: {e}")

def parse_date(date_str):
    for fmt in ("%Y.%m.%d", "%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return datetime.max

def sort_data():
    items.sort(key=lambda x: parse_date(x['exp']))

# ==========================================
# 소비기한 예측 함수
# ==========================================
def predict_expiry(name, storage):
    """재료명 키워드를 기반으로 소비기한을 자동 예측."""
    for keyword, days in DEFAULT_SHELF_LIFE.items():
        if keyword in name:
            # 냉동 보관 시 2배로 연장
            multiplier = 2 if storage == "냉동" else 1
            return (today + timedelta(days=days * multiplier)).strftime("%Y.%m.%d")
    return ""

# ==========================================
# 색상 분류 함수 (보고서 설계 기준)
# ==========================================
def classify_color(remaining):
    """남은 일수를 기준으로 색상 반환."""
    if remaining >= 7:
        return "#a5d6a7"   # 초록 — 여유
    elif remaining >= 3:
        return "#fff176"   # 노랑 — 주의
    elif remaining >= 1:
        return "#ffcc80"   # 주황 — 임박
    else:
        return "#ef9a9a"   # 빨강 — 경고 (당일 또는 경과)

def classify_text_color(remaining):
    """막대 위 텍스트 색상 (가독성용)."""
    if remaining < 3:
        return "#b71c1c"
    return "#1b5e20"

def get_status_label(remaining):
    if remaining > 7:
        return "여유"
    elif remaining >= 3:
        return "주의"
    elif remaining >= 1:
        return "임박"
    elif remaining == 0:
        return "오늘까지"
    else:
        return f"{abs(remaining)}일 경과"

# ==========================================
# 날짜 유효성 검사
# ==========================================
def validate_date(date_str):
    """날짜 형식 유효성 검사. 통과 시 True, 실패 시 에러 메시지 반환."""
    if not date_str.strip():
        return True, ""   # 비어있으면 예측으로 채워주므로 허용
    if parse_date(date_str) == datetime.max:
        return False, "날짜 형식이 올바르지 않습니다.\nYYYY.MM.DD 형식으로 입력해주세요.\n예) 2026.12.31"
    return True, ""

# ==========================================
# UI 렌더링 및 제어 함수
# ==========================================
def refresh_ui():
    sort_data()
    save_data()
    render_timeline()
    render_table()
    update_button_states()
    update_status_bar()

def update_status_bar():
    """하단 상태바: 전체 개수, 임박/경과 개수 표시."""
    total = len(items)
    expired = sum(1 for it in items if parse_date(it['exp']) != datetime.max
                  and (parse_date(it['exp']) - today).days < 0)
    urgent = sum(1 for it in items if parse_date(it['exp']) != datetime.max
                 and 0 <= (parse_date(it['exp']) - today).days < 3)
    msg = f"총 {total}개 식재료"
    if expired:
        msg += f"  |  ⚠ 기한 경과 {expired}개"
    if urgent:
        msg += f"  |  🔔 임박 {urgent}개"
    status_bar.config(text=msg)

def render_timeline():
    canvas.delete("all")
    canvas_width = 520
    row_height = 28
    days_to_show = 14
    day_width = canvas_width / days_to_show
    label_y = 10
    bar_top_offset = 25

    total_height = bar_top_offset + len(items) * row_height + 10

    # 배경 줄 (홀짝 구분)
    for i, item in enumerate(items):
        y = bar_top_offset + i * row_height
        bg = "#f9f9f9" if i % 2 == 0 else "#ffffff"
        canvas.create_rectangle(0, y, canvas_width, y + row_height, fill=bg, outline="")

    # 세로 눈금선 및 날짜 라벨
    for i in range(days_to_show + 1):
        x = i * day_width
        canvas.create_line(x, label_y + 12, x, total_height, fill="#e0e0e0")
        if i == 0:
            canvas.create_text(x + 4, label_y, text="Today", fill="#e53935",
                               anchor="w", font=('Arial', 8, 'bold'))
        elif i % 2 == 0:
            canvas.create_text(x, label_y, text=f"+{i}일", fill="#9e9e9e",
                               anchor="n", font=('Arial', 7))

    # Today 기준선 (빨간 세로선)
    canvas.create_line(0, label_y + 12, 0, total_height, fill="#e53935", width=2)

    # 각 식재료 막대 렌더링
    for i, item in enumerate(items):
        exp_date = parse_date(item['exp'])
        y = bar_top_offset + i * row_height
        bar_h_top = y + 4
        bar_h_bot = y + row_height - 4

        if exp_date == datetime.max:
            # 날짜 없음: 회색 점선 표시
            canvas.create_rectangle(0, bar_h_top, canvas_width, bar_h_bot,
                                    fill="#eeeeee", outline="#bdbdbd", dash=(4, 4))
            canvas.create_text(6, y + row_height // 2,
                                text=f"{item['name']} (날짜 없음)",
                                anchor="w", font=('Arial', 9), fill="#9e9e9e")
            continue

        delta = (exp_date - today).days
        color = classify_color(delta)

        if delta < 0:
            # 기한 경과: 빗금 패턴 효과 (진한 빨강 테두리)
            canvas.create_rectangle(0, bar_h_top, 18, bar_h_bot,
                                    fill="#ef9a9a", outline="#c62828")
            canvas.create_text(22, y + row_height // 2,
                                text=f"⚠ {item['name']} ({abs(delta)}일 경과)",
                                anchor="w", font=('Arial', 9, 'bold'), fill="#c62828")
        else:
            end_x = min(delta, days_to_show) * day_width
            end_x = max(end_x, 2)   # 최소 2px는 그리기
            canvas.create_rectangle(0, bar_h_top, end_x, bar_h_bot,
                                    fill=color, outline=color)
            label = get_status_label(delta)
            canvas.create_text(6, y + row_height // 2,
                                text=f"{item['name']}  [{label}]",
                                anchor="w", font=('Arial', 9),
                                fill=classify_text_color(delta))

    canvas.config(scrollregion=(0, 0, canvas_width, max(total_height, 150)))

def render_table():
    global new_row_vars
    for widget in table_frame.winfo_children():
        widget.destroy()

    entries.clear()
    headers = ["식재료명", "용량", "소비기한", "보관"]
    col_offset = 1 if delete_mode or adding_item else 0

    # 헤더
    header_bg = "#1565c0"
    for j, h in enumerate(headers):
        tk.Label(table_frame, text=h, font=('Arial', 10, 'bold'),
                 bg=header_bg, fg="white",
                 borderwidth=1, relief="flat", width=13,
                 padx=4, pady=4).grid(row=0, column=j + col_offset, sticky='nsew', padx=1, pady=1)

    # 데이터 행
    for i, item in enumerate(items):
        row_idx = i + 1
        exp_date = parse_date(item['exp'])
        delta = (exp_date - today).days if exp_date != datetime.max else 999
        row_bg = classify_color(delta) if exp_date != datetime.max else "#f5f5f5"
        # 짝수/홀수 행 미세 구분
        if exp_date == datetime.max:
            row_bg = "#f5f5f5"

        if delete_mode:
            tk.Button(table_frame, text="✕", fg="white", bg="#e53935",
                      relief="flat", font=('Arial', 9, 'bold'),
                      command=lambda idx=i: remove_item(idx)).grid(row=row_idx, column=0, padx=2, pady=1)

        if edit_mode:
            row_vars = {}
            for j, key in enumerate(["name", "qty", "exp", "storage"]):
                var = tk.StringVar(value=item[key])
                if key == "storage":
                    # 보관 방식은 드롭다운
                    opt = tk.OptionMenu(table_frame, var, *STORAGE_OPTIONS)
                    opt.config(width=9, bg="white", relief="groove")
                    opt.grid(row=row_idx, column=j + col_offset, padx=1, pady=1)
                else:
                    tk.Entry(table_frame, textvariable=var, width=13,
                             justify='center', relief="groove").grid(
                        row=row_idx, column=j + col_offset, padx=1, pady=1)
                row_vars[key] = var
            entries.append(row_vars)
        else:
            for j, key in enumerate(["name", "qty", "exp", "storage"]):
                text = item[key]
                # 소비기한 컬럼에 D-day 표시 추가
                if key == "exp" and exp_date != datetime.max:
                    if delta < 0:
                        text = f"{item[key]} (D+{abs(delta)})"
                    elif delta == 0:
                        text = f"{item[key]} (D-Day)"
                    else:
                        text = f"{item[key]} (D-{delta})"
                tk.Label(table_frame, text=text, bg=row_bg,
                         borderwidth=1, relief="groove", width=13,
                         padx=4, pady=4).grid(
                    row=row_idx, column=j + col_offset, sticky='nsew', padx=1, pady=1)

    # 추가 입력 행
    if adding_item is not None:
        new_row_idx = len(items) + 1

        btn_frame = tk.Frame(table_frame, bg="#e8f5e9")
        btn_frame.grid(row=new_row_idx, column=0, padx=2, pady=2)
        tk.Button(btn_frame, text="✔", fg="white", bg="#43a047",
                  relief="flat", font=('Arial', 9, 'bold'),
                  command=confirm_add, width=2).pack(side='left', padx=1)
        tk.Button(btn_frame, text="✘", fg="white", bg="#e53935",
                  relief="flat", font=('Arial', 9, 'bold'),
                  command=cancel_add, width=2).pack(side='left', padx=1)

        new_row_vars = {}
        for j, key in enumerate(["name", "qty", "exp", "storage"]):
            var = tk.StringVar()
            if key == "storage":
                var.set("냉장")
                opt = tk.OptionMenu(table_frame, var, *STORAGE_OPTIONS)
                opt.config(width=9, bg="#fffde7", relief="groove")
                opt.grid(row=new_row_idx, column=j + 1, padx=1, pady=2)
            else:
                ph = {"name": "재료명*", "qty": "용량", "exp": "YYYY.MM.DD (비우면 자동)"}
                entry = tk.Entry(table_frame, textvariable=var, width=13,
                                 justify='center', bg="#fffde7", relief="groove")
                entry.grid(row=new_row_idx, column=j + 1, padx=1, pady=2)
                # placeholder 힌트 텍스트
                hint = ph.get(key, "")
                if hint:
                    entry.insert(0, hint)
                    entry.config(fg="#aaaaaa")
                    entry.bind("<FocusIn>", lambda e, en=entry, h=hint: _clear_hint(e, en, h))
                    entry.bind("<FocusOut>", lambda e, en=entry, h=hint: _restore_hint(e, en, h))
            new_row_vars[key] = var

    table_frame.update_idletasks()
    list_canvas.config(scrollregion=list_canvas.bbox("all"))

def _clear_hint(event, entry, hint):
    if entry.get() == hint:
        entry.delete(0, tk.END)
        entry.config(fg="black")

def _restore_hint(event, entry, hint):
    if not entry.get():
        entry.insert(0, hint)
        entry.config(fg="#aaaaaa")

def update_button_states():
    idle = not (edit_mode or delete_mode or adding_item)
    btn_edit.config(
        state=tk.NORMAL,
        text="수정 완료" if edit_mode else "✏ 수정",
        bg="#1565c0" if edit_mode else "#e3f2fd",
        fg="white" if edit_mode else "#1565c0"
    )
    btn_delete.config(
        state=tk.NORMAL,
        text="삭제 완료" if delete_mode else "🗑 삭제",
        bg="#c62828" if delete_mode else "#ffebee",
        fg="white" if delete_mode else "#c62828"
    )
    btn_add.config(state=tk.NORMAL if idle else tk.DISABLED)

# ==========================================
# 이벤트 핸들러 (버튼 동작)
# ==========================================
def toggle_edit():
    global edit_mode
    if edit_mode:
        # 수정 완료 — 날짜 유효성 검사 후 저장
        for i, row_vars in enumerate(entries):
            exp_val = row_vars["exp"].get()
            ok, msg = validate_date(exp_val)
            if not ok:
                messagebox.showwarning("날짜 오류", f"[{items[i]['name']}]\n{msg}")
                return
            for key in ["name", "qty", "exp", "storage"]:
                items[i][key] = row_vars[key].get()
    edit_mode = not edit_mode
    refresh_ui()

def toggle_delete():
    global delete_mode
    delete_mode = not delete_mode
    refresh_ui()

def start_add_item():
    global adding_item
    adding_item = {"name": "", "qty": "", "exp": "", "storage": "냉장"}
    refresh_ui()

def confirm_add():
    global adding_item

    hint_texts = {"name": "재료명*", "exp": "YYYY.MM.DD (비우면 자동)"}
    new_data = {}
    for k, v in new_row_vars.items():
        val = v.get()
        # placeholder 텍스트 제거
        if val == hint_texts.get(k, ""):
            val = ""
        new_data[k] = val.strip()

    # 이름 필수 체크
    if not new_data["name"]:
        messagebox.showwarning("입력 오류", "식재료 이름은 필수입니다.")
        return

    # 날짜 유효성 검사
    ok, msg = validate_date(new_data["exp"])
    if not ok:
        messagebox.showwarning("날짜 오류", msg)
        return

    # 소비기한 비어있으면 자동 예측
    if not new_data["exp"]:
        predicted = predict_expiry(new_data["name"], new_data["storage"])
        if predicted:
            new_data["exp"] = predicted
            messagebox.showinfo(
                "소비기한 자동 예측",
                f"'{new_data['name']}'의 소비기한을\n{predicted} 으로 자동 설정했습니다.\n"
                "(보관 방식·실제 상태에 따라 다를 수 있습니다)"
            )
        else:
            # 예측 불가 시 사용자에게 직접 입력 요청
            messagebox.showwarning("소비기한 없음",
                                   "소비기한을 자동으로 예측할 수 없습니다.\n"
                                   "직접 입력해 주세요. (YYYY.MM.DD)")
            return

    items.append(new_data)
    adding_item = None
    refresh_ui()

def cancel_add():
    global adding_item
    adding_item = None
    refresh_ui()

def remove_item(idx):
    name = items[idx]['name']
    if messagebox.askyesno("삭제 확인", f"'{name}'을(를) 삭제할까요?"):
        del items[idx]
        refresh_ui()

# ==========================================
# 범례 렌더링
# ==========================================
def render_legend(parent):
    legend_frame = tk.Frame(parent, bg="white")
    legend_frame.pack(anchor='w', padx=4, pady=(2, 0))
    legend_data = [
        ("#a5d6a7", "7일 이상 (여유)"),
        ("#fff176", "3~6일 (주의)"),
        ("#ffcc80", "1~2일 (임박)"),
        ("#ef9a9a", "당일/경과 (경고)"),
    ]
    for color, label in legend_data:
        box = tk.Label(legend_frame, bg=color, width=2, relief="groove")
        box.pack(side='left', padx=(4, 1))
        tk.Label(legend_frame, text=label, font=('Arial', 8), bg="white",
                 fg="#555555").pack(side='left', padx=(0, 8))

# ==========================================
# 메인 UI 설정 및 프로그램 진입점
# ==========================================
def setup_ui():
    global root, canvas, table_frame, btn_edit, btn_delete, btn_add, list_canvas, status_bar

    root = tk.Tk()
    root.title("🥦 냉장고 관리자")
    root.geometry("660x780")
    root.configure(bg="#f5f5f5")
    root.resizable(True, True)

    # ── 1. 타임라인 영역 ──────────────────────────
    timeline_container = tk.Frame(root, bg="white", relief="groove", borderwidth=1)
    timeline_container.pack(fill='x', padx=16, pady=(16, 6))

    header_frame = tk.Frame(timeline_container, bg="white")
    header_frame.pack(fill='x', padx=8, pady=(6, 2))
    tk.Label(header_frame, text="📅  소비기한 현황", font=('Arial', 11, 'bold'),
             bg="white", fg="#1565c0").pack(side='left')

    render_legend(timeline_container)

    canvas_frame = tk.Frame(timeline_container, bg="white")
    canvas_frame.pack(fill='both', expand=True, padx=4, pady=(2, 6))

    canvas = tk.Canvas(canvas_frame, bg="white", height=160, highlightthickness=0)
    tl_scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=tl_scrollbar.set)
    tl_scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # 마우스 휠 스크롤 (타임라인)
    canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    # ── 구분선 ─────────────────────────────────────
    tk.Frame(root, height=1, bg="#bdbdbd").pack(fill='x', padx=16, pady=4)

    # ── 2. 컨트롤 영역 ────────────────────────────
    control_frame = tk.Frame(root, bg="#f5f5f5")
    control_frame.pack(fill='x', padx=16, pady=4)

    tk.Label(control_frame, text="< List >", font=('Arial', 13, 'bold'),
             bg="#f5f5f5").pack(side='left', padx=(0, 10))

    btn_edit = tk.Button(control_frame, text="✏ 수정",
                         bg="#e3f2fd", fg="#1565c0", relief="flat",
                         font=('Arial', 9, 'bold'), padx=8, pady=3,
                         cursor="hand2", command=toggle_edit)
    btn_edit.pack(side='left', padx=3)

    btn_delete = tk.Button(control_frame, text="🗑 삭제",
                           bg="#ffebee", fg="#c62828", relief="flat",
                           font=('Arial', 9, 'bold'), padx=8, pady=3,
                           cursor="hand2", command=toggle_delete)
    btn_delete.pack(side='left', padx=3)

    # ── 3. 리스트 영역 ────────────────────────────
    list_container = tk.Frame(root, bg="#f5f5f5")
    list_container.pack(fill='both', expand=True, padx=16)

    list_canvas = tk.Canvas(list_container, highlightthickness=0, bg="#f5f5f5")
    list_scrollbar = tk.Scrollbar(list_container, orient="vertical", command=list_canvas.yview)

    table_frame = tk.Frame(list_canvas, bg="#f5f5f5")
    canvas_window = list_canvas.create_window((0, 0), window=table_frame, anchor="nw")

    list_canvas.configure(yscrollcommand=list_scrollbar.set)
    list_scrollbar.pack(side="right", fill="y")
    list_canvas.pack(side="left", fill="both", expand=True)

    list_canvas.bind('<Configure>',
                     lambda e: list_canvas.itemconfig(canvas_window, width=e.width))
    list_canvas.bind("<MouseWheel>",
                     lambda e: list_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    # ── 4. 하단 버튼 + 상태바 ─────────────────────
    bottom_frame = tk.Frame(root, bg="#f5f5f5")
    bottom_frame.pack(fill='x', padx=16, pady=(6, 4))

    btn_add = tk.Button(bottom_frame, text="  ⊕  식재료 추가  ",
                        bg="#43a047", fg="white", relief="flat",
                        font=('Arial', 10, 'bold'), padx=10, pady=5,
                        cursor="hand2", command=start_add_item)
    btn_add.pack(side='left')

    status_bar = tk.Label(root, text="", font=('Arial', 9),
                          bg="#eeeeee", fg="#555555", anchor='w', padx=10, pady=3)
    status_bar.pack(fill='x', side='bottom')

    # ── 초기화 ────────────────────────────────────
    load_data()
    refresh_ui()
    root.mainloop()

if __name__ == "__main__":
    setup_ui()
