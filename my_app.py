import streamlit as st
import json
import os

TASKS_FILE = "data/tasks.json"
MEMO_FILE = "data/memos.json"

# 할 일 데이터 처리 함수
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

def add_task():
    new_task = st.session_state.get("new_task_input", "").strip()
    if new_task:
        st.session_state['tasks'].append({"text": new_task, "done": False})
        save_tasks(st.session_state['tasks'])
        st.success(f"{new_task}가 추가되었습니다!")
        st.session_state["new_task_input"] = ""

# 메모 데이터 처리 함수
def load_memos():
    if os.path.exists(MEMO_FILE):
        with open(MEMO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_memos(memos):
    os.makedirs(os.path.dirname(MEMO_FILE), exist_ok=True)
    with open(MEMO_FILE, 'w', encoding='utf-8') as f:
        json.dump(memos, f, ensure_ascii=False, indent=4)

def add_memo():
    memo_text = st.session_state.get("new_memo_input", "").strip()
    is_starred = st.session_state.get("star_checkbox", False)
    if memo_text:
        st.session_state['memos'].append({"text": memo_text, "star": is_starred})
        save_memos(st.session_state['memos'])
        st.success(f"{memo_text}가 저장되었습니다!")
        st.session_state["new_memo_input"] = ""
        st.session_state["star_checkbox"] = False
    else:
        st.warning("메모 내용을 입력해주세요.")

if 'tasks' not in st.session_state:
    st.session_state['tasks'] = load_tasks()

if 'memos' not in st.session_state:
    st.session_state['memos'] = load_memos()

st.set_page_config(
    page_title="나만의 할 일 & 메모 앱",
    page_icon="🖇️",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.sidebar.title("📍 메뉴 선택")
app_mode = st.sidebar.radio("기능을 선택하세요", ["할 일 리스트", "메모장"])

def todo_app_function():
    st.title("나만의 할 일 리스트")
    st.text_input("새로운 할 일을 입력하세요:", key="new_task_input")
    st.button("할 일 추가", on_click=add_task)

    st.markdown("---")
    st.subheader("현재 할 일 목록")
    remove_indexs = []

    if st.session_state['tasks']:
        for i, task in enumerate(st.session_state['tasks']):
            col1, col2 = st.columns([0.7, 0.3])

            with col1:
                checked = st.checkbox(f"{task['text']}", value=task['done'], key=f"check_task_{i}")
                if checked != st.session_state['tasks'][i]['done']:
                    st.session_state['tasks'][i]['done'] = checked
                    save_tasks(st.session_state['tasks'])
                    st.rerun()
            with col2:
                if st.button("삭제", key=f"delete_task_{i}"):
                    remove_indexs.append(i)
            
        for idx in sorted(remove_indexs, reverse=True):
            del st.session_state['tasks'][idx]
            st.info(f"할 일이 삭제되었습니다.")

        if remove_indexs:
            save_tasks(st.session_state['tasks'])
            st.rerun()
        
        done_tasks_count = sum(1 for task in st.session_state['tasks'] if task['done'])
        total_tasks_count = len(st.session_state['tasks'])

        st.markdown("---")
        st.info(f"완료된 할 일: {done_tasks_count} / {total_tasks_count}")

        if total_tasks_count > 0 and done_tasks_count == total_tasks_count:
            st.balloons()
            st.success("🎉 모든 할 일을 완료했습니다! 축하합니다! ")

    else:
        st.info("아직 할 일이 없습니다. 새로운 할 일을 추가해보세요!")

def memo_app_function():
    st.header("나만의 메모장")
    st.text_area("새로운 메모를 입력하세요:", key="new_memo_input")
    st.checkbox("⭐️ 즐겨찾기로 등록", key="star_checkbox")
    st.button("메모 저장", on_click=add_memo)
    
    st.markdown("---")
    st.subheader("전체 메모 보기")

    search_query = st.text_input("메모 검색", key="search_memo_input")
    filter_option = st.selectbox("메모 필터", ("전체 메모", "⭐️ 즐겨찾기 메모"), key="filter_memo_select")

    filtered_memos = []
    for memo in st.session_state['memos']:
        search_match = search_query.lower() in memo['text'].lower() if search_query else True
        if filter_option == "⭐️ 즐겨찾기 메모":
            if memo['star'] and search_match:
                filtered_memos.append(memo)
        else:
            if search_match:
                filtered_memos.append(memo)
    
    if filtered_memos:
        for memo in filtered_memos:
            star_icon = "⭐️ " if memo['star'] else ""
            st.write(f"- {star_icon}{memo['text']}")
    else:
        st.info("조건에 맞는 메모가 없습니다.")

if app_mode == "할 일 리스트":
    todo_app_function()
elif app_mode == "메모장":
    memo_app_function()