import streamlit as st
import os
import uuid
import json
from bs4 import BeautifulSoup

st.set_page_config(page_title="사양 추출기 + 이력 저장", layout="wide")

DATA_DIR = "saved_specs"
os.makedirs(DATA_DIR, exist_ok=True)

def extract_specs(html: str, mode: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    result = ""

    if mode == "pc":
        wraps = soup.select(".item_wrap")
        for wrap in wraps:
            title = wrap.select_one(".item_tit")
            category = title.get_text(strip=True) if title else ""
            if category:
                result += f"\n[카테고리] {category}\n"

            for a in wrap.select("a"):
                id_ = a.get("data-modal-id")
                name = a.get_text(strip=True)
                if id_ and name:
                    result += f"- {id_} {name}\n"
            result += "\n"

    elif mode == "mo":
        items = soup.select(".accordion__list > li")
        for li in items:
            title = li.select_one("button")
            category = title.get_text(strip=True) if title else ""
            if category:
                result += f"\n[카테고리] {category}\n"

            for item in li.select("li"):
                a = item.select_one("a")
                if a:
                    id_ = a.get("data-modal-id")
                    name = a.get_text(strip=True)
                    if id_ and name:
                        result += f"- {id_} {name}\n"
            result += "\n"

    return result.strip()

st.title("📄 기아 가격표 HTML 사양 추출기 + 이력 저장")

tab1, tab2 = st.tabs(["📤 새 작업", "📚 저장된 이력"])

with tab1:
    uploaded_file = st.file_uploader("HTML 파일 업로드", type=["html"])
    mode = st.radio("버전 선택", ["pc", "mo"], horizontal=True)
    description = st.text_input("이 작업에 대한 설명을 입력하세요 (예: 2025 카니발 가격표)")

    if uploaded_file:
        html = uploaded_file.read().decode("utf-8")
        result = extract_specs(html, mode)
        st.text_area("📌 추출 결과", result, height=400)

        if st.button("💾 이 작업 저장하기"):
            uid = str(uuid.uuid4())
            save_data = {
                "id": uid,
                "description": description,
                "filename": uploaded_file.name,
                "mode": mode,
                "result": result
            }
            with open(f"{DATA_DIR}/{uid}.json", "w", encoding="utf-8") as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            st.success("✅ 저장 완료! '저장된 이력' 탭에서 확인하세요.")

with tab2:
    files = sorted(os.listdir(DATA_DIR), reverse=True)
    for fname in files:
        with open(f"{DATA_DIR}/{fname}", encoding="utf-8") as f:
            data = json.load(f)
        with st.expander(f"🗂 {data['description']} ({data['filename']})"):
            st.code(data["result"], language="text")
