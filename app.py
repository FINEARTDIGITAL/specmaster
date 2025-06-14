import streamlit as st
import uuid
import os
import json

os.makedirs("results", exist_ok=True)
os.makedirs("uploads", exist_ok=True)

st.title("📄 파일 업로드 & 텍스트 저장 웹앱")

user_text = st.text_area("📝 텍스트 입력", height=200)
uploaded_file = st.file_uploader("📎 파일 업로드", type=None)

if st.button("✅ 저장하고 공유 링크 생성하기"):
    if not user_text and not uploaded_file:
        st.warning("텍스트나 파일 중 하나는 입력해야 합니다.")
    else:
        unique_id = str(uuid.uuid4())

        data = {"id": unique_id, "text": user_text}

        if uploaded_file is not None:
            file_path = f"uploads/{unique_id}_{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            data["filename"] = uploaded_file.name

        with open(f"results/{unique_id}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        share_url = f"?view_id={unique_id}"
        st.success("✅ 저장 완료!")
        st.markdown(f"🔗 [공유 링크 보기](/{share_url})")
        st.markdown(f"URL 복사: `{share_url}`")

view_id = st.query_params.get("view_id")
if view_id:
    result_path = f"results/{view_id}.json"
    if os.path.exists(result_path):
        with open(result_path, "r", encoding="utf-8") as f:
            result = json.load(f)
        st.header("📄 저장된 결과 보기")
        st.markdown(f"**입력 텍스트**: {result['text']}")
        if "filename" in result:
            file_path = f"uploads/{view_id}_{result['filename']}"
            st.markdown(f"**업로드 파일**: [다운로드]({file_path})")
    else:
        st.error("해당 ID의 결과가 존재하지 않습니다.")
