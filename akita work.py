import streamlit as st
import requests
import json
import uuid
import datetime  # 日付や時間を扱うための部品

# ==========================================
# ★ データベース設定（Firebase）
# ==========================================
FIREBASE_URL = "https://akita-work-default-rtdb.firebaseio.com/v2.json"

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

# --- アプリの基本設定 ---
st.set_page_config(page_title="あきたワーク Pro", page_icon="🌾", layout="centered", initial_sidebar_state="collapsed")

# データの初期化
db = load_data()
if "users" not in db or db["users"] is None: db["users"] = {}
if "jobs" not in db or db["jobs"] is None: db["jobs"] = {}

# 画面切り替えの仕組み
if "page" not in st.session_state: st.session_state.page = "login"
if "user" not in st.session_state: st.session_state.user = None
if "phone" not in st.session_state: st.session_state.phone = None
if "current_job_id" not in st.session_state: st.session_state.current_job_id = None

akita_cities = ["秋田市", "能代市", "横手市", "大館市", "男鹿市", "湯沢市", "鹿角市", "由利本荘市", "潟上市", "大仙市", "北秋田市", "にかほ市", "仙北市", "小坂町", "上小阿仁村", "藤里町", "三種町", "八峰町", "五城目町", "八郎潟町", "井川町", "大潟村", "美郷町", "羽後町", "東成瀬村"]

def change_page(page_name):
    st.session_state.page = page_name
    st.rerun()

# ==========================================
# 1. ログイン画面
# ==========================================
def show_login():
    st.title("🌾 あきたワーク Pro")
    st.write("スマホやPCから使えるクラウド版です！")
    
    tab1, tab2 = st.tabs(["👤 一般ユーザー", "🏢 管理者（企業）"])
    
    with tab1:
        phone = st.text_input("電話番号", key="log_phone")
        password = st.text_input("暗証番号 (4桁)", type="password", key="log_pass")
        if st.button("ログイン", type="primary", use_container_width=True):
            user = db["users"].get(phone)
            if user and user.get("pass") == password:
                st.session_state.user = user
                st.session_state.phone = phone
                change_page("job_list")
            else:
                st.error("番号かパスワードが違います。")
        
        st.divider()
        if st.button("初めての方（新規登録）", use_container_width=True):
            change_page("register")
            
    with tab2:
        admin_id = st.text_input("管理者ID", key="log_admin_id")
        admin_pass = st.text_input("パスワード", type="password", key="log_admin_pass")
        if st.button("管理者としてログイン", type="primary", use_container_width=True):
            if admin_id == "9999" and admin_pass == "9999":
                change_page("admin_dashboard")
            else:
                st.error("管理者情報が違います。")

def show_register():
    st.title("📝 新規登録")
    name = st.text_input("お名前")
    phone = st.text_input("電話番号")
    password = st.text_input("暗証番号 (4桁)", type="password")
    city = st.selectbox("お住まいの市町村", akita_cities)
    
    if st.button("登録する", type="primary", use_container_width=True):
        if name and phone and password:
            if phone in db["users"]:
                st.error("この電話番号はすでに登録されています。")
            else:
                db["users"][phone] = {
                    "name": name, "pass": password, "city": city, "history": []
                }
                save_data(db)
                st.success("登録完了！ログイン画面に戻ります。")
                change_page("login")
        else:
            st.warning("すべて入力してください。")
    
    if st.button("戻る", use_container_width=True):
        change_page("login")

# ==========================================
# 2. 仕事一覧画面
# ==========================================
def show_job_list():
    with st.sidebar:
        st.subheader(f"👤 {st.session_state.user.get('name', 'ゲスト')} さん")
        user_city = st.session_state.user.get('city', '未設定')
        st.write(f"📍 {user_city}")
        st.divider()
        if st.button("➕ お願いを投稿", use_container_width=True): change_page("post_job")
        if st.button("📋 応募履歴", use_container_width=True): change_page("history")
        st.divider()
        if st.button("ログアウト", use_container_width=True):
            st.session_state.user = None
            st.session_state.phone = None
            change_page("login")

    st.title("🟢 現在の募集一覧")
    
    user_history = st.session_state.user.get("history", [])
    
    # 自分がまだ応募していない仕事だけを絞り込む
    available_jobs = {
        jid: j for jid, j in db["jobs"].items() 
        if j.get("status") == "approved" and jid not in user_history
    }
    
    if not available_jobs:
        st.info("現在
