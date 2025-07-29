import streamlit as st
import json
import os

TASKS_FILE = "data/tasks.json"

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

if 'tasks' not in st.session_state:
    st.session_state['tasks'] = load_tasks()

st.set_page_config(
    page_title="나만의 할 일 리스트",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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