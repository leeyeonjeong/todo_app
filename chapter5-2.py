import streamlit as st
import json
import os

# --- 파일 경로 설정 ---
TASKS_FILE = 'data/tasks.json'
MEMOS_FILE = 'data/memos.json'

# --- 공통 유틸 함수 ---
def ensure_data_folder():
    os.makedirs("data", exist_ok=True)

# --- 할 일 데이터 처리 함수 ---
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    ensure_data_folder()
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

def add_task():
    new_task = st.session_state.get("new_task_input", "").strip()
    if new_task:
        st.session_state['tasks'].append({"text": new_task, "done": False})
        save_tasks(st.session_state['tasks'])
        st.success(f"'{new_task}'가 추가되었습니다!")
        st.session_state["new_task_input"] = ""

# --- 메모 데이터 처리 함수 ---
def load_memos():
    if os.path.exists(MEMOS_FILE):
        with open(MEMOS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_memos(memos):
    ensure_data_folder()
    with open(MEMOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(memos, f, ensure_ascii=False, indent=4)

def add_memo():
    memo_text = st.session_state.get("new_memo_input", "").strip()
    is_starred = st.session_state.get("star_checkbox", False)
    if memo_text:
        st.session_state['memos'].append({"text": memo_text, "star": is_starred})
        save_memos(st.session_state['memos'])
        st.success("메모가 저장되었습니다!")
        st.session_state["new_memo_input"] = ""
        st.session_state["star_checkbox"] = False
    else:
        st.warning("메모 내용을 입력해주세요.")

# --- 세션 상태 초기화 ---
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = load_tasks()

if 'memos' not in st.session_state:
    st.session_state['memos'] = load_memos()

# Add 5-2 Chapter
if st.session_state.get("go_to_memo"):
    st.session_state["go_to_memo"] = False
    st.session_state["app_mode_select"] = "🗒️ 메모 & 즐겨찾기"
    st.rerun()

# --- 앱 전역 설정 ---
st.set_page_config(
    page_title="나만의 통합 자동화 웹앱",
    page_icon="☘️",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("")

# Add 5-2 Chapter
# --- 사이드바 메뉴 ---
st.sidebar.title("📌 메뉴 선택")
app_mode = st.sidebar.radio("기능을 선택하세요", ["📝 할 일 리스트", "🗒️ 메모 & 즐겨찾기"], key="app_mode_select")

def todo_app_function():
    st.title("📝 나만의 할 일 리스트")
    st.text_input("새로운 할 일을 입력하세요:", key="new_task_input")
    st.button("할 일 추가", on_click=add_task)

    st.markdown("---")
    st.subheader("📋 현재 할 일 목록")
    remove_indices = []

    if st.session_state['tasks']:
        for i, task in enumerate(st.session_state['tasks']):
            col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
            with col1:
                checked = st.checkbox(f"{task['text']}", value=task['done'], key=f"check_task_{i}")
                if checked != task['done']:
                    st.session_state['tasks'][i]['done'] = checked
                    save_tasks(st.session_state['tasks'])
                    st.rerun()
            with col2:
                if st.button("삭제", key=f"delete_task_{i}"):
                    remove_indices.append(i)
            # Add 5-2 Chapter
            with col3:
                if st.button("메모하기", key=f"memo_this_task_{i}"):
                    st.session_state['prefill_memo_content'] = task['text']
                    st.session_state['go_to_memo'] = True
                    st.rerun()
                
        for idx in sorted(remove_indices, reverse=True):
            del st.session_state['tasks'][idx]
        if remove_indices:
            save_tasks(st.session_state['tasks'])
            st.rerun()

        done = sum(1 for t in st.session_state['tasks'] if t['done'])
        total = len(st.session_state['tasks'])
        st.info(f"완료된 할 일: {done} / {total}")
        if total > 0 and done == total:
            st.balloons()
            st.success("🎉 모든 할 일을 완료했습니다!")
    else:
        st.info("할 일이 없습니다. 추가해보세요!")

def memo_app_function():
    st.title("🗒️ 나만의 메모장")

    # Add 5-2 Chapter
    prefill_text = ""
    if 'prefill_memo_content' in st.session_state and st.session_state['prefill_memo_content']:
        prefill_text = f"할 일 관련 메모: {st.session_state['prefill_memo_content']}\n"
        st.session_state['prefill_memo_content'] = None
    
    st.text_area("새로운 메모를 입력하세요: ", value=prefill_text, key="new_memo_input")
    st.checkbox("⭐ 즐겨찾기", key="star_checkbox")
    st.button("메모 저장", on_click=add_memo)

    st.markdown("---")
    st.subheader("📚 전체 메모 보기")

    search_query = st.text_input("🔍 메모 검색 (내용 포함)", key="memo_search")
    filter_starred = st.selectbox("필터", ["전체 메모", "⭐ 즐겨찾기 메모"])

    filtered = []
    for memo in st.session_state['memos']:
        match_search = search_query.lower() in memo['text'].lower() if search_query else True
        match_star = (filter_starred == "전체 메모") or (filter_starred == "⭐ 즐겨찾기 메모" and memo['star'])
        if match_search and match_star:
            filtered.append(memo)

    if filtered:
        for memo in filtered:
            star = "⭐ " if memo['star'] else ""
            st.write(f"- {star}{memo['text']}")
    else:
        st.info("조건에 맞는 메모가 없습니다.")

# Add 5-2 Chapter
# --- 할 일 기능 화면 ---
if st.session_state["app_mode_select"] == "📝 할 일 리스트":
    todo_app_function()
# --- 메모 기능 화면 ---
elif st.session_state["app_mode_select"] == "🗒️ 메모 & 즐겨찾기":
    memo_app_function()