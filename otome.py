import streamlit as st
import json
import time
from datetime import datetim

# CSS 스타일 (금색의 코르다 스타일)
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background-image: url('data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAGQAZADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD5/ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooimport streamlit as st
import json
import time
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="이중속성의 소녀",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일 (금색의 코르다 스타일)
st.markdown(r"""
<style>
    /* 전체 배경 - 책상과 꽃들을 연상시키는 배경 */
    .stApp {
        background: linear-gradient(135deg, 
            rgba(240, 248, 255, 0.95) 0%,
            rgba(230, 245, 255, 0.95) 30%,
            rgba(220, 240, 255, 0.95) 60%,
            rgba(200, 230, 255, 0.95) 100%),
            radial-gradient(circle at 20% 50%, rgba(135, 206, 250, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(176, 224, 230, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(240, 248, 255, 0.4) 0%, transparent 50%);
        background-size: cover;
        background-attachment: fixed;
        color: #2c3e50;
        min-height: 100vh;
    }
    
    /* 페이지 패턴 추가 */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(255,255,255,0.8) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.8) 1px, transparent 1px);
        background-size: 20px 20px;
        z-index: -1;
        opacity: 0.3;
    }
    
    /* 메인 컨테이너 - 책과 종이 느낌 */
    .main-container {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem auto;
        max-width: 800px;
        border: 2px solid rgba(135, 206, 250, 0.3);
        box-shadow: 
            0 8px 32px rgba(0, 100, 200, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
        position: relative;
    }
    
    /* 종이 질감 추가 */
    .main-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 25px,
            rgba(135, 206, 250, 0.1) 25px,
            rgba(135, 206, 250, 0.1) 26px
        );
        border-radius: 20px;
        pointer-events: none;
    }
    
    /* 제목 스타일 */
    .game-title {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(45deg, #4682b4, #87ceeb, #4682b4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .game-subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #5a6c7d;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        width: 100%;
        height: 60px;
        background: linear-gradient(45deg, #87ceeb 0%, #4682b4 100%);
        color: white;
        border: none;
        border-radius: 15px;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(70, 130, 180, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(70, 130, 180, 0.4);
        background: linear-gradient(45deg, #4682b4 0%, #87ceeb 100%);
    }
    
    /* 텍스트 입력 스타일 */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.8);
        border: 2px solid rgba(135, 206, 235, 0.5);
        border-radius: 10px;
        color: #2c3e50;
        font-size: 1.1rem;
        padding: 10px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4682b4;
        box-shadow: 0 0 10px rgba(70, 130, 180, 0.3);
    }
    
    /* 스토리 텍스트 박스 */
    .story-box {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #4682b4;
        line-height: 1.8;
        font-size: 1.3rem;
        color: #2c3e50;
        box-shadow: 0 2px 10px rgba(70, 130, 180, 0.1);
    }
    
    /* 선택지 버튼 */
    .choice-button {
        background: rgba(255, 255, 255, 0.8);
        border: 2px solid rgba(135, 206, 235, 0.5);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        color: #2c3e50;
    }
    
    .choice-button:hover {
        background: rgba(135, 206, 235, 0.2);
        border-color: #4682b4;
    }
    
    /* 캐릭터 이름 */
    .character-name {
        color: #4682b4;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    /* 나레이션 */
    .narration {
        font-style: italic;
        color: #5a6c7d;
        margin: 1rem 0;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
        font-size: 1.2rem;
        line-height: 1.8;
        border-left: 3px solid #87ceeb;
    }
    
    /* 작은 버튼 스타일 */
    .small-button {
        width: 120px !important;
        height: 35px !important;
        font-size: 0.9rem !important;
        margin: 0.2rem !important;
    }
    
    /* 자동 진행 표시 */
    .auto-progress {
        text-align: center;
        color: #5a6c7d;
        font-size: 0.9rem;
        margin: 1rem 0;
        background: rgba(255, 255, 255, 0.6);
        padding: 0.5rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# 게임 데이터 초기화
def init_game_data():
    if 'game_state' not in st.session_state:
        st.session_state.game_state = {
            'current_scene': 'main_menu',
            'player_name': '',
            'current_chapter': 'prologue',
            'current_episode': 1,
            'affection': {
                'yoonho': 0, 'doyoon': 0, 'minjun': 0,
                'joowon': 0, 'yoojun': 0, 'eunho': 0
            },
            'player_stats': {
                'light_control': 0, 'dark_control': 0,
                'balance': 0, 'confidence': 0
            },
            'story_flags': {},
            'choices_made': [],
            'save_data': []
        }

# 세이브 시스템
def save_game():
    save_data = st.session_state.game_state.copy()
    save_data['save_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.game_state['save_data'] = save_data
    st.success("게임이 저장되었습니다!")
    time.sleep(1)

def load_game():
    if st.session_state.game_state.get('save_data'):
        st.session_state.game_state.update(st.session_state.game_state['save_data'])
        st.success("게임을 불러왔습니다!")
        time.sleep(1)
        return True
    else:
        st.error("저장된 게임이 없습니다.")
        return False

# 메인 메뉴
def show_main_menu():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # 게임 제목
    st.markdown('<h1 class="game-title">🌙 이중속성의 소녀 ✨</h1>', unsafe_allow_html=True)
    st.markdown('<p class="game-subtitle">~ 빛과 어둠 사이에서 피어나는 사랑 ~</p>', unsafe_allow_html=True)
    
    # 분위기 있는 인트로 텍스트
    st.markdown("""
    <div class="narration">
    천 년에 한 번 태어나는 이중속성자...<br>
    빛과 어둠을 동시에 품은 소녀의 운명은 과연..?<br><br>
    마법학원에서 펼쳐지는 여섯 남주와의 감동적인 로맨스 판타지
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # 이름 입력
        st.markdown("### 👑 주인공 이름 설정")
        player_name = st.text_input("이름을 입력해주세요", 
                                  value=st.session_state.game_state.get('player_name', ''),
                                  placeholder="예: 이하늘")
        
        if player_name:
            st.session_state.game_state['player_name'] = player_name
        
        st.markdown("---")
        
        # 메뉴 버튼들
        if st.button("🌟 새로 시작하기"):
            if player_name:
                st.session_state.game_state['current_scene'] = 'prologue'
                st.session_state.game_state['current_episode'] = 1
                st.rerun()
            else:
                st.error("이름을 입력해주세요!")
        
        if st.button("📚 이어서 하기"):
            if load_game():
                st.rerun()
        
        if st.button("💾 게임 저장하기"):
            save_game()
        
        if st.button("⚙️ 설정"):
            st.info("설정 기능은 개발 중입니다!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# 프롤로그 데이터 생성 함수
def get_prologue_episodes():
    player_name = st.session_state.game_state.get('player_name', '공주')
    
    return {
        1: {
            'title': '운명적 탄생',
            'scenes': [
                {
                    'type': 'narration',
                    'text': '17년 전, 어느 작은 마을...\n\n달이 가장 높이 뜬 자정, 한 아이가 태어났다.'
                },
                {
                    'type': 'narration', 
                    'text': '그 순간, 마을 전체가 빛과 어둠으로 뒤덮였다.\n정오인데도 별이 보이고, 한밤중인데도 태양빛이 스며들었다.'
                },
                {
                    'type': 'dialogue',
                    'character': '마을 사람',
                    'text': '저, 저주받은 아이다...! 이상한 일이 일어나고 있어!'
                },
                {
                    'type': 'narration',
                    'text': '부모조차 갓난아기를 제대로 안아보지 못했다.\n작은 생명이 세상에 가져온 것은 축복이 아닌, 두려움이었다.'
                }
            ]
        },
        2: {
            'title': '어린 시절의 따뜻한 기억들',
            'scenes': [
                {
                    'type': 'narration',
                    'text': '1-4살까지의 희미한 기억들...\n\n비록 짧았지만, 가족과 함께한 따뜻한 시간들이 있었다.'
                },
                {
                    'type': 'dialogue',
                    'character': '어머니',
                    'text': f'우리 {player_name}가 제일 예뻐... ♪'
                },
                {
                    'type': 'narration',
                    'text': '어머니가 불러주던 자장가...\n아버지가 높이 들어올려 주던 따뜻한 손길...'
                },
                {
                    'type': 'narration',
                    'text': '남동생과 함께 그림 그리며 놀던 시간들...\n가족만의 작은 정원에서 꽃을 기르던 평온한 오후들...'
                },
                {
                    'type': 'dialogue',
                    'character': '아버지',
                    'text': f'우리 {player_name}가 제일 예뻐!'
                },
                {
                    'type': 'narration',
                    'text': '그때는 몰랐다.\n이 작은 행복이 곧 끝날 것이라는 걸...'
                }
            ]
        },
        3: {
            'title': '운명의 날',
            'scenes': [
                {
                    'type': 'narration',
                    'text': '5살 생일날...\n\n가족들이 준비해준 작은 생일 케이크를 받았다.'
                },
                {
                    'type': 'dialogue',
                    'character': f'어린 {player_name}',
                    'text': '와아! 케이크다! 고마워요!'
                },
                {
                    'type': 'narration',
                    'text': '너무 기뻐서 감정이 폭발했다.\n\n순간적으로 온 집이 빛으로 가득 차더니 급속히 어둠에 휩싸였다.'
                },
                {
                    'type': 'narration',
                    'text': '빛과 어둠이 충돌하며 집 전체가 무너지기 시작했다.\n\n모든 것이 혼돈에 빠졌다.'
                },
                {
                    'type': 'dialogue',
                    'character': '어머니',
                    'text': f'{player_name}... 괜찮아, 엄마가 지켜줄게...'
                },
                {
                    'type': 'narration',
                    'text': '정신을 잃기 전 마지막으로 본 것은...\n자신을 감싸 안은 어머니의 모습이었다.'
                },
                {
                    'type': 'narration',
                    'text': '...\n\n...\n\n깨어났을 때는 폐허 속에 혼자였다.\n가족은 모두 사라져 있었고, 그 이후 모든 기억이 사라졌다.'
                },
                {
                    'type': 'choice',
                    'text': '17년이 지난 지금...',
                    'options': [
                        {
                            'text': '아직도 그날의 악몽에 시달린다',
                            'effects': {'confidence': -2, 'dark_control': +1}
                        },
                        {
                            'text': '기억은 없지만 마음 한켠이 아프다', 
                            'effects': {'confidence': -1, 'balance': +1}
                        },
                        {
                            'text': '이제는 과거에 얽매이지 않겠다',
                            'effects': {'confidence': +1, 'light_control': +1}
                        }
                    ]
                }
            ]
        }
    }

# 프롤로그 표시
def show_prologue():
    current_ep = st.session_state.game_state.get('current_episode', 1)
    
    # 프롤로그 데이터 동적 생성
    PROLOGUE_EPISODES = get_prologue_episodes()
    
    if current_ep > len(PROLOGUE_EPISODES):
        st.session_state.game_state['current_scene'] = 'chapter_1'
        st.session_state.game_state['current_episode'] = 1
        st.rerun()
        return
    
    episode = PROLOGUE_EPISODES[current_ep]
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # 에피소드 제목
    st.markdown(f'<h2 style="text-align: center; color: #ffd700;">📖 프롤로그 {current_ep} - {episode["title"]}</h2>', unsafe_allow_html=True)
    
    # 장면별 표시
    scene_index = st.session_state.game_state.get('current_scene_index', 0)
    
    if scene_index < len(episode['scenes']):
        scene = episode['scenes'][scene_index]
        
        # 자동 진행을 위한 타이머 설정
        auto_advance_time = 4  # 4초 후 자동 진행
        if 'scene_start_time' not in st.session_state:
            st.session_state.scene_start_time = time.time()
        
        if scene['type'] == 'narration':
            st.markdown(f'<div class="narration">{scene["text"]}</div>', unsafe_allow_html=True)
            
        elif scene['type'] == 'dialogue':
            st.markdown(f'<div class="character-name">{scene["character"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="story-box">"{scene["text"]}"</div>', unsafe_allow_html=True)
            
        elif scene['type'] == 'choice':
            st.markdown(f'<div class="narration">{scene["text"]}</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                for i, option in enumerate(scene['options']):
                    if st.button(option['text'], key=f"choice_{current_ep}_{i}"):
                        # 선택지 효과 적용
                        for stat, value in option['effects'].items():
                            st.session_state.game_state['player_stats'][stat] += value
                        
                        # 다음 장면으로
                        st.session_state.game_state['current_scene_index'] = scene_index + 1
                        if 'scene_start_time' in st.session_state:
                            del st.session_state.scene_start_time
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        # 자동 진행 로직 (선택지가 아닌 경우에만)
        elapsed_time = time.time() - st.session_state.scene_start_time
        remaining_time = max(0, auto_advance_time - elapsed_time)
        
        # 자동 진행 표시
        if remaining_time > 0:
            st.markdown(f'<div class="auto-progress">⏰ {remaining_time:.1f}초 후 자동 진행 (다음 버튼으로 빠르게 진행 가능)</div>', unsafe_allow_html=True)
            
            # 자동 진행 타이머
            progress_bar = st.progress(1 - (remaining_time / auto_advance_time))
            
            # 짧은 지연 후 페이지 새로고침
            time.sleep(0.1)
            if remaining_time <= 0.1:
                if scene_index + 1 < len(episode['scenes']):
                    st.session_state.game_state['current_scene_index'] = scene_index + 1
                else:
                    # 다음 에피소드로
                    st.session_state.game_state['current_episode'] = current_ep + 1
                    st.session_state.game_state['current_scene_index'] = 0
                if 'scene_start_time' in st.session_state:
                    del st.session_state.scene_start_time
                st.rerun()
            else:
                # 자동 새로고침
                st.rerun()
        
        # 수동 다음 버튼 (작게)
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("▶ 다음", key=f"next_{scene_index}", help="빠르게 넘어가기"):
                if scene_index + 1 < len(episode['scenes']):
                    st.session_state.game_state['current_scene_index'] = scene_index + 1
                else:
                    # 다음 에피소드로
                    st.session_state.game_state['current_episode'] = current_ep + 1
                    st.session_state.game_state['current_scene_index'] = 0
                if 'scene_start_time' in st.session_state:
                    del st.session_state.scene_start_time
                st.rerun()
    
    # 진행 상황 표시
    progress = min(max((scene_index + 1) / len(episode['scenes']), 0.0), 1.0)
    st.progress(progress)
    st.markdown(f'<p style="text-align: center; color: #888;">에피소드 {current_ep}/3 - 진행률: {int(progress * 100)}%</p>', unsafe_allow_html=True)
    
    # 메뉴 버튼 (작게)
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col2:
        if st.button("🏠 메뉴", help="메인 메뉴로"):
            st.session_state.game_state['current_scene'] = 'main_menu'
            if 'scene_start_time' in st.session_state:
                del st.session_state.scene_start_time
            st.rerun()
    with col4:
        if st.button("💾 저장", help="현재 진행 저장"):
            save_game()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 메인 실행 함수
def main():
    init_game_data()
    
    current_scene = st.session_state.game_state.get('current_scene', 'main_menu')
    
    if current_scene == 'main_menu':
        show_main_menu()
    elif current_scene == 'prologue':
        show_prologue()
    elif current_scene == 'chapter_1':
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; color: #ffd700;">🏫 Chapter 1 - 절망의 학원 생활</h2>', unsafe_allow_html=True)
        st.markdown('<div class="story-box">Chapter 1은 개발 중입니다! 곧 업데이트 예정이에요 ✨</div>', unsafe_allow_html=True)
        
        if st.button("🏠 메인 메뉴로 돌아가기"):
            st.session_state.game_state['current_scene'] = 'main_menu'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
