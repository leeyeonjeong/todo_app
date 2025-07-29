import streamlit as st

st.header("Chapter 2-1 파이썬 기초")

# 변수: 정보 담기
name = "김코딩"
age = 30
st.write(f"변수 예시: 이름: {name}, 나이: {age}")

# 리스트: 여러 정보 나열 (순서가 있는 데이터 묶음)
fruits = ["사과", "바나나", "오렌지"]
st.write(f"리스트 예시: 좋아하는 과일: {fruits}")
st.write(f"첫 번째 과일: {fruits[0]}")
st.write(f"두 번째 과일: {fruits[1]}")
st.write(f"세 번째 과일: {fruits[2]}")

# 조건문: 만약 ~라면 (특정 조건에 따라 다른 동작)
score = st.slider("점수를 입력하세요:", 0, 100, 75)
if score >= 60:
    st.success(f"점수 {score}점으로 합격입니다.")
else:
    st.error(f"점수 {score}점으로 불합격입니다.")

# 반복문: 여러 번 반복하기 (특정 작업을 반복 수행)
st.write("좋아하는 과일 목록:")
for fruit in fruits:
    st.write(f"- {fruit}")

st.write("카운트다운:")
count = 0
while count < 3:
    st.write(f"반복 {count}회")
    count += 1

st.header("Chapter 2-2 함수 예제")

def greet(name):
    st.write(f"안녕하세요, {name}님!")

greet("김코딩")

def double_number(num):
    result = num * 2
    return result

st.write(f"5 * 2 = {double_number(5)}")

user_name_for_greet = st.text_input("이름을 입력하시면 인사해 드려요: ")
if user_name_for_greet:
    greet(user_name_for_greet)

my_num = st.number_input("숫자를 입력하세요: ")
if st.button("두 배로 만들기", key="double_button"):
    doubled_result = double_number(my_num)
    st.write(f"{my_num} * 2 = {doubled_result}")

def create_custom_button(label, key_name, message):
    if st.button(label, key=key_name):
        st.info(f"{label} 버튼이 눌렸습니다! {message}")

create_custom_button("첫 번째 버튼", "first_custom_button", "이것은 첫 번째 메시지입니다.")
create_custom_button("두 번째 버튼", "seconde_custom_button", "이것은 두 번째 메시지입니다.")
create_custom_button("세 번째 버튼", "third_custom_button", "간단하게 재사용할 수 있죠?")

st.header("Chapter 2-3 Streamlit 핵심 부품들 심화")

user_name_comp = st.text_input("이름을 입력하세요: ", key="user_name_comp")
if user_name_comp:
    st.write(f"환영합니다, {user_name_comp}님!")

if st.button("인사하기", key="greet_button_comp"):
    st.write("반갑습니다!")

age = st.slider("나이를 선택하세요: ", 0, 100, 25, key="age_slider, comp")
st.write(f"선택한 나이: {age}")

if st.checkbox("이용 약관에 동의합니다", key="agree_checkbox_comp"):
    st.success("동의하셨군요! 서비스를 이용할 수 있습니다.")
else:
    st.warning("동의하지 않았습니다. 서비스를 이용할 수 없습니다.")

option = st.selectbox("가장 좋아하는 색깔은?", ("빨강", "파랑", "초록", "노랑"), key="color_selectbotx_comp")
st.write(f"선택한 색깔: {option}")

st.markdown("---")
st.subheader("st.session_state")

if 'click_count' not in st.session_state:
    st.session_state['click_count'] = 0

st.write(f"버튼이 눌린 횟수: {st.session_state['click_count']}")

if st.button("카운트 증가", key="increment_button"):
    st.session_state['click_count'] += 1
    st.write(f"카운트 증가! 현재 횟수: {st.session_state['click_count']}")