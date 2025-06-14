import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="가격표(PC-모바일 비교) Tool", layout="wide")

st.markdown("""
# 가격표(PC-모바일 비교) Tool

자동차 가격표 HTML을 업로드하고 PC/모바일 결과를 빠르게 비교하세요.
""")

with open("index.html", "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=1050, scrolling=True)
