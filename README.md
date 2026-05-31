# **우리집 냉장고를 부탁해!**

**파이썬 식재료 관리 프로그램**

## **1. 프로그램 개요**

**개발 목적:** 자취생 및 1인 가구의 식재료 낭비를 방지하기 위한 직관적인 냉장고 재고 관리 및 소비기한 추적 시스템 제공.

**주요 특징:** 파이썬 프로그래밍에 익숙하지 않은 타 전공 학생 및 일반인도 즉시 실행할 수 있도록 설계했다. 외부 패키지 의존성을 배제하고 파이썬 표준 라이브러리만을 활용하여 사용자 접근성을 극대화했다.

## **2. 실행 환경 및 시스템 요구사항**

- **필요 환경:** Python 3.x 이상 (Windows / macOS 호환)
- **외부 라이브러리:** 불필요 (pip install 등 추가 모듈 설치 과정 없음)
- **실행 절차:**

1. **사전 준비:** PC 환경에 기본 Python 설치 진행. ( 설치 과정 중 'Add Python to PATH' 옵션 반드시 체크 요망)

2. **파일 다운로드:** 제공된 파이썬 소스코드 파일(예: refrigerator.py)을 로컬 PC의 원하는 디렉토리에 저장.

**프로그램 구동:** 복잡한 터미널 명령어 입력 없이, 저장된 .py 파일을 더블 클릭하여 즉시 실행. (또는 파이썬 IDLE 우클릭 후 'Edit with IDLE' 환경에서 F5 키 입력으로 실행 가능)

3. **시스템 구조 및 핵심 로직**

본 프로그램은 비전공자도 코드의 흐름을 쉽게 이해할 수 있도록 4가지 핵심 모듈로 구성했다.

- **상태 데이터 관리 :** 내부 메모리에 리스트(items) 및 딕셔너리(DEFAULT_SHELF_LIFE) 구조를 선언하여 현재 식재료 목록과 품목별 권장 보관 일수(예: 사과 14일, 우유 7일 등)를 데이터화하여 관리한다.
- **데이터 영속성 및 파일 입출력 :** 가벼운 구동을 위해 별도의 데이터베이스(DB) 시스템 대신 os 모듈을 활용했다. 프로그램 구동 시 같은 폴더에 food_list.txt라는 텍스트 파일을 자동 생성하고 항목이 추가되거나 변경될 때마다 해당 파일에 내역을 읽고(load) 씀(save). 이를 통해 프로그램 종료 후에도 기록이 안전하게 보존됨.
- **소비기한 자동 예측 알고리즘 :** 사용자가 날짜를 기입하지 않고 식재료 이름만 입력할 경우 작동하는 편의 기능. datetime 모듈을 활용하여 사전 정의된 보관 데이터를 바탕으로 '오늘 날짜 + 권장 보관 일수'를 연산하여 예상 소비기한을 텍스트 폼에 자동 기입함.

**직관적 UI 시각화 :** 파이썬 표준 그래픽 도구인 tkinter 내장 모듈을 사용하여 사용자 인터페이스(UI)를 구성한다. 데이터 표출 시 남은 소비기한 일수에 따라 4단계 색상 코딩(7일 이상: 🟢초록, 3~6일: 🟡노랑, 1~2일: 🟠주황, 기한 당일/경과: 🔴빨강)을 적용한 간트 차트막대그래프를 화면에 렌더링하여 직관적인 재고 관리를 지원한다.

4. **기대효과**

**경제적/환경적 측면 (식재료 폐기율 감소 및 식비 절감)**

자취생 및 1인 가구는 식재료의 소비 속도가 느려 유통기한을 넘겨 폐기하는 빈도가 높다. 이 프로그램은 소비기한이 임박한 식재료를 시각적으로 한 눈에 알아볼 수 있게 색깔별로 알려주어 우선 소비를 유도한다.

이를 통해 불필요한 식재료 폐기를 줄여 환경 보호에 기여하고 중복 구매를 방지하여 자취생의 생활비(식비) 절감에 직접적인 도움을 줄 수 있다.

## **3.코드 상세 분석**

**전역 상태 및 데이터 구조 관리**

```python
FILENAME = "food_list.txt"
today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
items = []

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
```

- **설명:** 프로그램 전반에서 공유할 상태 변수를 최상단에 정의했다.
- `items` 리스트는 현재 냉장고에 있는 식재료 딕셔너리들을 메모리에 올려두는 역할을 한다.
- `DEFAULT_SHELF_LIFE`는 식재료별 권장 보관 일수를 아예 정해두는 하드코딩 딕셔너리로 사용자가 소비기한을 모를 때 자동 예측을 수행하기 위한 기준이 된다.

**`load_data()` 함수: 초기 데이터 로드 및 초기화**

```python
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
```

- **기능 설명:** 프로그램 구동 시 최초로 실행되어 보조 기억 장치에 저장된 식재료 데이터를 메인 메모리(`items` 리스트)로 적재한다.
- **구현 상세:**
    - `os.path.exists()`를 통해 `food_list.txt` 파일의 존재 여부를 가장 먼저 확인한다. 만약 파일이 없다면 쓰기 모드(`"w"`)로 빈 파일을 즉시 생성하고 함수를 종료하여, 최초 실행 시 발생할 수 있는 '파일 찾을 수 없음' 에러를 방지한다.
    - 파일이 존재할 경우 읽기 모드(`"r"`)로 열어 한 줄씩 순회한다.
    - 각 줄의 공백을 제거(`strip()`)하고, 역슬래시(`\`)를 구분자로 사용하여 문자열을 분리(`split('\\')`)한다.
    - 분리된 데이터가 정확히 4개(이름, 용량, 소비기한, 보관방법)일 경우에만 딕셔너리 형태로 구성하여 `items` 전역 리스트에 추가한다.
    - `try-except` 블록을 구성하여 파일 읽기 과정에서 예기치 못한 오류가 발생하더라도 프로그램 전체가 종료되지 않도록 예외 처리한다.

**`save_data()` 함수: 데이터 파일 갱신**

```python
def save_data():
    try:
        with open(FILENAME, "w", encoding="utf-8") as f:
            for item in items:
                f.write(f"{item['name']}\\{item['qty']}\\{item['exp']}\\{item['storage']}\n")
    except Exception as e:
        messagebox.showerror("저장 오류", f"오류 발생: {e}")
```

- **기능 설명:** 사용자의 추가, 수정, 삭제 작업으로 인해 메모리 상의 `items` 리스트가 변경될 때마다 이를 `food_list.txt` 파일에 덮어써서 동기화한다.
- **구현 상세:**
    - 파일을 쓰기 모드(`"w"`)로 열어 기존 내용을 모두 지우고 현재 리스트의 내용으로 새롭게 갱신한다.
    - `for` 문을 통해 `items` 리스트를 순회하며, 각 딕셔너리의 값들을 역슬래시(`\`)로 연결한 단일 문자열로 포맷팅하여 기록한다.
    - 파일 입출력 중 권한 문제나 디스크 용량 부족 등의 오류가 발생할 경우 콘솔 출력이 아닌 `messagebox`를 통해 사용자에게 직접 오류를 안내하도록 구성하여 GUI 프로그램의 특성을 살렸다.

**`predict_expiry(name, storage)` 함수: 소비기한 자동 산출 알고리즘**

```python
def predict_expiry(name, storage):
    """재료명 키워드를 기반으로 소비기한을 자동 예측."""
    for keyword, days in DEFAULT_SHELF_LIFE.items():
        if keyword in name:
            # 냉동 보관 시 2배로 연장
            multiplier = 2 if storage == "냉동" else 1
            return (today + timedelta(days=days * multiplier)).strftime("%Y.%m.%d")
    return ""
```

- **기능 설명:** 사용자가 식재료 추가 시 소비기한을 미입력한 경우 식재료 이름을 분석하여 적정 소비기한을 자동 예측한다.
- **구현 상세:**
    - 미리 정의된 전역 딕셔너리인 `DEFAULT_SHELF_LIFE`의 모든 항목을 순회하며 키워드 매칭을 시도한다. (예: 입력값이 "서울우유"일 경우 키워드 "우유"와 매칭됨)
    - 키워드가 매칭되면 해당 식재료의 기본 보관 일수(`days`)를 획득한다.
    - 사용자가 선택한 보관 방법(`storage`)이 '냉동'인지 확인하고 냉동일 경우 보관 기한을 2배(`multiplier = 2`)로 연장하는 예외 로직을 적용한다.
    - `datetime` 모듈의 `timedelta`를 활용하여 오늘 기준일(`today`)에 최종 계산된 보관 일수를 더한 후, "YYYY.MM.DD" 형식의 문자열로 변환하여 반환한다. 예측할 수 없는 경우 빈 문자열을 반환한다.

**`classify_color(remaining)` 함수: 데이터 시각화를 위한 상태 분류**

```python
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
```

- **기능 설명:** 식재료의 남은 소비기한 일수(`remaining`)를 기반으로, UI 렌더링 시 적용할 색상 코드를 결정한다.
- **구현 상세:**
    - `if-elif-else` 제어문을 사용하여 남은 일수를 4개의 구간으로 분할한다.
    - 7일 이상은 안전한 상태로 판단하여 초록색(여유), 3일 이상은 노란색(주의), 1일 이상은 주황색(임박) 코드를 반환한다.
    - 남은 일수가 0이거나 음수인 경우 당일 소비 혹은 기한 경과를 의미하므로 사용자에게 강한 느낌의 빨간색 코드를 반환하도록 하여 직관적인 UX를 제공한다.

**`render_timeline()` 함수: 간트 차트(막대그래프) 시각화 구현**

```python
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
```

- **기능 설명:** `tkinter.Canvas` 위젯을 제어하여 식재료별 유통기한 현황을 가로 막대 그래프(간트 차트) 형태로 동적 렌더링한다.
- **구현 상세:**
    - 화면을 초기화(`delete("all")`)한 후 최대 14일치(`days_to_show`)를 표현할 수 있도록 배경 눈금선과 기준일("Today") 라벨을 좌표 기반으로 직접 만든다.
    - `items` 리스트를 순회하며 남은 기한(`delta`)을 픽셀 길이(`end_x`)로 환산하여 사각형(`create_rectangle`) 객체를 그린다.
    - 이때 `classify_color()`를 호출하여 막대의 배경색(`fill`)을 결정하며 특히 기한이 지난 항목(`delta < 0`)은 최소 길이로 붉은색 막대를 고정하고 테두리를 진하게 처리하여 시각적 경고 효과를 극대화한다.

**`confirm_add()` 함수: 신규 데이터 검증 및 등록**

```python
def confirm_add():
    global adding_item
    # ... (입력값 정제 생략) ...

    # 입력값 필수 확인
    if not new_data["name"]:
        messagebox.showwarning("입력 오류", "식재료 이름은 필수입니다.")
        return

    # 소비기한 빈칸 시 자동 예측 연계
    if not new_data["exp"]:
        predicted = predict_expiry(new_data["name"], new_data["storage"])
        if predicted:
            new_data["exp"] = predicted
            messagebox.showinfo("소비기한 자동 예측", f"'{new_data['name']}'의 소비기한을\n{predicted} 으로 자동 설정했습니다.")
        else:
            messagebox.showwarning("소비기한 없음", "소비기한을 자동으로 예측할 수 없습니다.\n직접 입력해 주세요.")
            return

    # 정상 데이터 리스트 추가 및 UI 갱신
    items.append(new_data)
    adding_item = None
    refresh_ui()
```

- **기능 설명:** 사용자가 신규 식재료 폼을 작성하고 저장 버튼(✔)을 눌렀을 때 데이터를 검증하고 리스트에 반영하는 제어 함수이다.
- **구현 상세:**
    - 사용자 입력값 중 가장 중요한 "식재료 이름"의 누락 여부를 1차적으로 검증한다.
    - 사용자가 날짜를 기입하지 않았을 경우(`not new_data["exp"]`), `predict_expiry()` 함수를 호출하여 기한 예측을 시도한다.
    - 예측에 성공하면 획득한 날짜를 빈칸에 채우고 사용자에게 팝업으로 안내하며 예측이 불가능한 미확인 식재료일 경우 진행을 차단하고 수동 입력을 요청한다.
    - 모든 검증을 통과한 유효한 데이터만 `items` 리스트에 최종적으로 `append` 한 뒤 상태 변수를 초기화하고 화면을 갱신(`refresh_ui()`)한다.

## **입력 편의성 및 UI 이벤트 제어 함수**

`_clear_hint(event, entry, hint)` 및 `_restore_hint(event, entry, hint)` 함수

```python
def _clear_hint(event, entry, hint):
    if entry.get() == hint:
        entry.delete(0, tk.END)
        entry.config(fg="black")

def _restore_hint(event, entry, hint):
    if not entry.get():
        entry.insert(0, hint)
        entry.config(fg="#aaaaaa")
```

- **기능 설명:** 사용자 입력창 내부의 안내 문구를 동적으로 제어하여 화면의 직관성을 높인다.
- **구현 상세:**
    - 사용자가 식재료를 추가하기 위해 텍스트 입력창을 마우스로 클릭하여 포커스가 이동하면 `_clear_hint`가 실행된다.
    - 입력창의 현재 텍스트가 기본 힌트 문구와 동일한지 확인하고 일치하면 텍스트를 모두 지운 뒤 글자 색상을 검은색으로 변경하여 실제 입력을 받을 준비를 마친다.
    - 사용자가 아무것도 입력하지 않고 다른 곳을 클릭해 포커스가 벗어나면 `_restore_hint`가 실행되어 다시 회색 글씨로 힌트 문구를 채워 넣는다.

`update_button_states()` 함수

```python
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
```

- **기능 설명:** 프로그램의 현재 조작 상태(수정, 삭제, 추가)에 따라 화면 하단 버튼들의 디자인과 활성화 여부를 동적으로 갱신한다.
- **구현 상세:**
    - 특정 작업이 진행 중일 때는 다른 작업 버튼을 비활성화(`tk.DISABLED`)하여 논리적 충돌이나 중복 입력을 사전에 방지한다.
    - 수정 및 삭제 모드가 켜지면 해당 버튼의 배경색과 글자색 그리고 버튼 텍스트를 강렬한 색상으로 즉각 변경하여 사용자가 현재 어떤 상태인지 시각적으로 명확하게 인지하도록 돕는다.

`toggle_edit()` 함수

```python
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
```

- **기능 설명:** 식재료 목록의 수정 모드를 켜거나 끄며 완료 시 변경된 데이터를 검증하고 저장한다.
- **구현 상세:**
    - 수정 모드가 켜진 상태에서 사용자가 수정 완료를 누르면 화면에 입력된 모든 날짜 데이터의 유효성을 우선적으로 검사한다.
    - 잘못된 날짜 형식이 하나라도 발견되면 즉시 경고창을 띄우고 데이터 덮어쓰기 과정을 중단하여 오류를 차단한다.
    - 모든 데이터가 정상이면 딕셔너리의 이름, 용량, 소비기한, 보관방법 데이터를 갱신한 뒤 UI를 새로고침하여 변경 사항을 반영한다.

`toggle_delete()` 및 `remove_item(idx)` 함수

```python
def toggle_delete():
    global delete_mode
    delete_mode = not delete_mode
    refresh_ui()

def remove_item(idx):
    name = items[idx]['name']
    if messagebox.askyesno("삭제 확인", f"'{name}'을(를) 삭제할까요?"):
        del items[idx]
        refresh_ui()
```

- **기능 설명:** 데이터 삭제 모드를 활성화하고 사용자가 특정 항목을 선택했을 때 메모리에서 안전하게 삭제한다.
- **구현 상세:**
    - `toggle_delete`가 실행되면 전역 상태 변수를 반전시키고 표의 맨 앞 열에 삭제를 위한 빨간색 조작 버튼을 생성한다.
    - 사용자가 개별 항목의 삭제 버튼을 클릭하면 `remove_item`이 실행되어 실수로 지우는 것을 방지하기 위해 팝업창으로 최종 확인을 받는다.
    - 사용자가 동의 버튼을 누르면 리스트에서 해당 인덱스의 항목을 완전히 제거하고 화면을 새롭게 그린다.

`start_add_item()` 및 `cancel_add()` 함수

```python
def start_add_item():
    global adding_item
    adding_item = {"name": "", "qty": "", "exp": "", "storage": "냉장"}
    refresh_ui()

def cancel_add():
    global adding_item
    adding_item = None
    refresh_ui()
```

- **기능 설명:** 새로운 식재료를 추가하기 위한 신규 입력 폼을 표 하단에 생성하거나 취소한다.
- **구현 상세:**
    - 하단의 추가 버튼을 누르면 `adding_item` 변수에 빈 문자열과 기본 보관방법이 담긴 딕셔너리를 할당하고 화면을 갱신하여 빈 입력칸을 띄운다.
    - 사용자가 입력을 포기하고 취소(✘) 버튼을 누르면 해당 변수를 다시 초기화하고 UI를 갱신하여 화면에서 입력 폼을 깔끔하게 제거한다.

`render_legend(parent)` 함수

```python
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
```

- **기능 설명:** 간트 차트의 막대그래프 색상이 어떤 의미를 가지는지 설명하는 범례(Legend)를 타임라인 상단에 시각적으로 그린다.
- **구현 상세:**
    - 여유, 주의, 임박, 경고를 의미하는 4가지 색상 코드와 설명 텍스트를 리스트 형태의 쌍으로 묶어 순차적으로 레이아웃에 배치한다.
    - 이를 통해 별도의 외부 설명서 없이도 사용자가 색상의 의미를 직관적으로 파악하고 자신의 식재료 상태를 손쉽게 점검하도록 지원한다.

`setup_ui()` 함수 및 프로그램 진입점

```python
def setup_ui():
    global root, canvas, table_frame, btn_edit, btn_delete, btn_add, list_canvas, status_bar

    # 메인 윈도우 생성 및 기본 설정
    root = tk.Tk()
    root.title("🥦 냉장고 관리자")
    root.geometry("660x780")
    root.configure(bg="#f5f5f5")
    root.resizable(True, True)

    # 1. 타임라인 영역 (상단 간트 차트)
    timeline_container = tk.Frame(root, bg="white", relief="groove", borderwidth=1)
    timeline_container.pack(fill='x', padx=16, pady=(16, 6))
    # ... (캔버스 및 스크롤바 배치 코드 중략) ...
    canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    # 2. 컨트롤 영역 (수정, 삭제 버튼)
    control_frame = tk.Frame(root, bg="#f5f5f5")
    control_frame.pack(fill='x', padx=16, pady=4)
    # ... (버튼 배치 코드 중략) ...

    # 3. 리스트 영역 (하단 데이터 표)
    list_container = tk.Frame(root, bg="#f5f5f5")
    list_container.pack(fill='both', expand=True, padx=16)
    # ... (표 프레임 및 마우스 휠 이벤트 연동 코드 중략) ...

    # 4. 하단 버튼 및 상태바
    bottom_frame = tk.Frame(root, bg="#f5f5f5")
    bottom_frame.pack(fill='x', padx=16, pady=(6, 4))
    # ... (추가 버튼 및 상태 텍스트 배치 코드 중략) ...

    # 초기 데이터 로드 및 이벤트 루프 실행
    load_data()
    refresh_ui()
    root.mainloop()

if __name__ == "__main__":
    setup_ui()
```

- **기능 설명:** 프로그램의 뼈대가 되는 메인 창을 생성하고 타임라인, 컨트롤 버튼, 데이터 표, 상태바 등 4가지 주요 영역을 화면에 배치한 뒤 프로그램을 본격적으로 실행한다.
- **구현 상세:**
    - `tkinter` 라이브러리의 `Tk()` 객체를 호출하여 기본 바탕이 되는 윈도우 창을 만들고 프로그램의 제목과 기본 해상도를 지정한다.
    - 화면을 위에서부터 아래로 총 4개의 구역(타임라인 영역, 컨트롤 영역, 리스트 영역, 하단 영역)으로 나누어 논리적이고 깔끔하게 위젯들을 조립하듯 배치한다.
    - 마우스 휠을 굴렸을 때 화면이 자연스럽게 위아래로 움직이도록 상단 캔버스와 하단 리스트 영역에 마우스 휠 스크롤 이벤트를 각각 연결하여 사용자의 조작 편의성을 높인다.
    - 화면 구성 요소의 배치가 모두 끝나면 `load_data()`와 `refresh_ui()`를 차례로 호출하여 텍스트 파일에 저장된 기존 식재료 데이터를 메모리로 불러오고 화면에 최초로 그린다.
    - 마지막으로 `root.mainloop()`를 실행하여 프로그램이 바로 종료되지 않고 사용자의 마우스 클릭이나 키보드 입력을 계속 기다리도록 무한 대기 상태로 진입시킨다.
    - 파일 최하단에 `if __name__ == "__main__":` 조건문을 추가하여 이 파이썬 파일이 메인으로 실행될 때만 화면을 띄우도록 프로그래밍 표준 관례를 지켜 안정성을 확보한다.

냉장고with절차적프로그래밍.py

- 코드
    
    ```python
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
    
    ```
