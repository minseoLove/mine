import streamlit as st
import base64

# 배경 이미지 인코딩
file_path = "/mnt/data/D794A7A7-795A-4D48-8374-9FD9B82D665D.jpeg"
with open(file_path, "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

# 페이지 설정
st.set_page_config(layout="wide")

# CSS로 전체 배경 설정 + 타이틀 스타일링
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        font-family: 'Georgia', serif;
    }}

    .title-text {{
        color: white;
        text-shadow: 2px 2px 6px #000000AA;
        font-size: 60px;
        text-align: center;
        margin-top: 20vh;
    }}

    .start-button {{
        display: flex;
        justify-content: center;
        margin-top: 40px;
    }}

    .stButton>button {{
        background-color: rgba(255, 255, 255, 0.8);
        color: #333;
        font-size: 20px;
        padding: 0.5em 2em;
        border: none;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }}

    .stButton>button:hover {{
        background-color: #eee;
    }}
    </style>
""", unsafe_allow_html=True)

# 게임 타이틀
st.markdown("<div class='title-text'>장미의 계약: 왕관 아래 피어난 맹세</div>", unsafe_allow_html=True)

# 시작 버튼
st.markdown("<div class='start-button'>", unsafe_allow_html=True)
start = st.button("게임 시작하기")
st.markdown("</div>", unsafe_allow_html=True)

# 클릭 시 반응
if start:
    st.success("✨ 새로운 이야기가 시작됩니다...")
