import streamlit as st
import requests
import json

# ==========================================
# 設定：確認したFirebaseのURL（末尾に/.jsonを追加済み）
# ==========================================
FIREBASE_URL = "https://akita-work-default-rtdb.firebaseio.com/.json"

# --- データの読み書き関数 ---
def load_data():
    try:
        res = requests.get(FIREBASE_URL)
        data = res.json()
        return data if data else {}
    except:
        return {}

def save_data(data):
    requests.put(FIREBASE_URL, json.dumps(data))

# --- アプリ設定 ---
st.set_page_config(page_title="あきたワーク Web", page_icon="🌾")

# データの初期読み込み
db = load_data()
if "users" not in db: db["users"] = {}
if "jobs" not in db: db["jobs"] = []

if "user" not in st.session_state:
    st.session_state.user = None

# --- 画面表示 ---
if not st.session_state.user:
    st.title("🌾 あきたワーク")
    tab1, tab2 = st.tabs(["ログイン", "新規登録"])
    
    with tab1:
        phone = st.text_input("電話番号 (ログイン用)")
        pw = st.text_input("暗証番号", type="password", key="login_pw")
        if st.button("ログイン"):
            user = db["users"].get(phone)
            if user and user["pass"] == pw:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("番号かパスワードが違います")
                
    with tab2:
        new_name = st.text_input("お名前")
        new_phone = st.text_input("登録用電話番号")
        new_pw = st.text_input("暗証番号（4桁）", type="password", key="reg_pw")
        if st.button("登録する"):
            if new_name and new_phone and new_pw:
                db["users"][new_phone] = {"name": new_name, "pass": new_pw}
                save_data(db)
                st.success("登録完了！「ログイン」タブからログインしてください。")
            else:
                st.warning("全部入力してください")
else:
    st.sidebar.title(f"👤 {st.session_state.user['name']}さん")
    menu = st.sidebar.radio("メニュー", ["お仕事を探す", "お願いを投稿する", "ログアウト"])

    if menu == "お仕事を探す":
        st.header("📍 募集中の仕事")
        if not db["jobs"]:
            st.info("現在、募集中の仕事はありません。")
        else:
            for i, job in enumerate(db["jobs"]):
                with st.expander(f"【{job['loc']}】 {job['title']}"):
                    st.write(f"報酬: {job['pay']}")
                    if st.button("応募する", key=f"apply_{i}"):
                        st.balloons()
                        st.success("応募しました！")

    elif menu == "お願いを投稿する":
        st.header("➕ お願いを投稿")
        t = st.text_input("内容")
        p = st.text_input("報酬")
        l = st.selectbox("場所", ["秋田市", "能代市", "横手市", "大仙市"])
        if st.button("投稿する"):
            if t and p:
                new_job = {"title": t, "pay": p, "loc": l}
                db["jobs"].append(new_job)
                save_data(db)
                st.success("投稿されました！")
            else:
                st.warning("内容と報酬を入力してください")

    if st.sidebar.button("ログアウト"):
        st.session_state.user = None
        st.rerun()
