import streamlit as st
from instagrapi import Client
import pandas as pd
import time

st.title("📩 Instagram DM 자동 발송기")
st.markdown("인스타 계정으로 로그인해서 엑셀에 있는 계정에 DM을 보내보세요!")

# 1. 로그인 정보
username = st.text_input("📱 인스타그램 ID", "")
password = st.text_input("🔒 비밀번호", "", type="password")

# 2. 엑셀 업로드
uploaded_file = st.file_uploader("📁 인스타 ID가 담긴 엑셀 업로드", type=["xlsx"])

# 3. DM 메시지 작성
message = st.text_area("💌 보낼 DM 메시지", "안녕하세요! 협찬 제안 드리고 싶어 연락드렸습니다 :)")

# 4. 실행 버튼
if st.button("🚀 DM 보내기 시작"):
    if not username or not password:
        st.error("로그인 정보를 입력해주세요!")
    elif not uploaded_file:
        st.error("엑셀 파일을 업로드해주세요!")
    elif not message.strip():
        st.error("메시지를 입력해주세요!")
    else:
        try:
            st.info("⏳ 인스타그램 로그인 중...")
            cl = Client()
            cl.login(username, password)
            st.success("✅ 로그인 성공!")

            df = pd.read_excel(uploaded_file)
            if "ID" not in df.columns:
                st.error("❌ 'ID'라는 컬럼명이 필요합니다.")
            else:
                accounts = df["ID"].dropna().unique().tolist()
                st.info(f"총 {len(accounts)}명에게 DM을 보냅니다!")

                progress = st.progress(0)
                status_area = st.empty()

                for i, username in enumerate(accounts):
                    try:
                        user_id = cl.user_id_from_username(username)
                        cl.direct_send(message, [user_id])
                        status_area.success(f"✅ {username} 에게 보냄")
                    except Exception as e:
                        status_area.warning(f"❌ {username} 실패: {e}")
                    time.sleep(3)  # 너무 빠르게 보내지 않도록
                    progress.progress((i+1) / len(accounts))

                st.success("🎉 모든 DM 전송 완료!")

        except Exception as e:
            st.error(f"❌ 에러 발생: {e}")