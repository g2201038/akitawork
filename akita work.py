import streamlit as st
import requests
import json
import uuid

# ==========================================
# ★ データベース設定（Firebase / 新しい部屋に変更してリセット）
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
    
    approved_jobs = {jid: j for jid, j in db["jobs"].items() if j.get("status") == "approved"}
    
    if not approved_jobs:
        st.info("現在募集中の求人はありません。左上の「＞」メニューから募集を投稿できます！")
    else:
        for jid, job in reversed(list(approved_jobs.items())):
            with st.container(border=True):
                st.subheader(job["title"])
                st.write(f"💰 **謝礼:** {job['pay']} ⏰ **日時:** {job['time']}")
                st.write(f"📍 **場所:** {job['loc']}")
                
                user_history = st.session_state.user.get("history", [])
                if jid in user_history:
                    st.button("✅ 応募済み", disabled=True, key=f"app_{jid}")
                else:
                    if st.button("詳しく見て応募する", key=f"det_{jid}", type="primary"):
                        st.session_state.current_job_id = jid
                        change_page("job_detail")

# ==========================================
# 3. 仕事詳細画面
# ==========================================
def show_job_detail():
    jid = st.session_state.current_job_id
    job = db["jobs"].get(jid)
    
    if not job:
        st.error("このお仕事は削除されたか、見つかりません。")
        if st.button("一覧に戻る"): change_page("job_list")
        return

    st.title("📋 お仕事の詳細")
    
    with st.container(border=True):
        st.subheader(job["title"])
        st.write(f"**⏰ 日時:** {job['time']}")
        st.write(f"**💰 給与:** {job['pay']}")
        st.write(f"**🎒 持ち物:** {job['items']}")
        st.write(f"**📍 勤務地:** {job['loc']}")
        
        map_url = f"https://www.google.com/maps/search/?api=1&query={job['loc']}"
        st.markdown(f"[🗺 Googleマップで場所を確認する]({map_url})")
    
    if st.button("✨ この仕事に応募する", type="primary", use_container_width=True):
        user_history = st.session_state.user.get("history", [])
        if jid not in user_history:
            user_history.append(jid)
            st.session_state.user["history"] = user_history
            db["users"][st.session_state.phone]["history"] = user_history
            save_data(db)
            st.success("応募しました！")
            change_page("job_list")
        
    if st.button("一覧に戻る", use_container_width=True):
        change_page("job_list")

# ==========================================
# 4. お願い投稿画面
# ==========================================
def show_post_job():
    st.title("➕ お願いを投稿")
    title = st.text_input("困りごと・内容 (例: 庭の草むしり)")
    
    col1, col2 = st.columns(2)
    month = col1.selectbox("月", list(range(1, 13)))
    day = col2.selectbox("日", list(range(1, 32)))
    time_str = st.text_input("希望時間 (例: 09:00〜12:00)")
    
    pay = st.text_input("お礼・給与 (例: 2,000円)")
    
    user_city = st.session_state.user.get('city', '')
    default_idx = akita_cities.index(user_city) if user_city in akita_cities else 0
    city = st.selectbox("集まる場所（市町村）", akita_cities, index=default_idx)
    
    loc_detail = st.text_input("詳しい場所・町名")
    items = st.text_input("持ち物や注意点")
    
    if st.button("確認申請を送る", type="primary", use_container_width=True):
        if title and pay:
            full_loc = f"{city} {loc_detail}".strip()
            datetime_str = f"{month}月{day}日 {time_str}"
            
            new_jid = str(uuid.uuid4())
            
            db["jobs"][new_jid] = {
                "title": title, "time": datetime_str, "pay": pay, "loc": full_loc,
                "items": items, "status": "pending", "posted_by": st.session_state.user.get("name", "名無し")
            }
            save_data(db)
            
            st.success("管理者に申請しました！許可されると一覧に表示されます。")
            change_page("job_list")
        else:
            st.warning("「内容」と「給与」は最低限入力してください。")
        
    if st.button("やめる（戻る）", use_container_width=True):
        change_page("job_list")

# ==========================================
# 5. 応募履歴
# ==========================================
def show_history():
    st.title("📋 応募履歴")
    history_jids = st.session_state.user.get("history", [])
    
    if not history_jids:
        st.info("まだ応募履歴がありません。")
    else:
        for jid in history_jids:
            job = db["jobs"].get(jid)
            if job:
                st.success(f"✅ {job['title']} ({job['time']})")
            else:
                st.warning("終了または削除されたお仕事です")
            
    if st.button("一覧に戻る"):
        change_page("job_list")

# ==========================================
# 6. 管理者画面
# ==========================================
def show_admin_dashboard():
    with st.sidebar:
        st.title("🏢 管理者メニュー")
        if st.button("👥 ユーザー管理"): change_page("admin_users")
        st.divider()
        if st.button("ログアウト"): change_page("login")

    st.title("⚙️ 管理ダッシュボード")
    
    pending_jobs = {jid: j for jid, j in db["jobs"].items() if j.get("status") == "pending"}
    approved_jobs = {jid: j for jid, j in db["jobs"].items() if j.get("status") == "approved"}
    
    st.subheader(f"📥 承認待ち ({len(pending_jobs)}件)")
    for jid, job in pending_jobs.items():
        with st.container(border=True):
            st.write(f"**{job['title']}** (投稿者: {job.get('posted_by', '不明')}さん)")
            col1, col2 = st.columns(2)
            if col1.button("✅ 許可", key=f"app_admin_{jid}", type="primary", use_container_width=True):
                db["jobs"][jid]["status"] = "approved"
                save_data(db)
                st.rerun()
            if col2.button("🗑 削除", key=f"del_admin_{jid}", use_container_width=True):
                del db["jobs"][jid]
                save_data(db)
                st.rerun()

    st.subheader(f"🟢 掲載中 ({len(approved_jobs)}件)")
    for jid, job in approved_jobs.items():
        with st.container(border=True):
            st.write(f"**{job['title']}** ({job['loc']})")
            if st.button("🗑 削除する", key=f"del_pub_{jid}"):
                del db["jobs"][jid]
                save_data(db)
                st.rerun()

def show_admin_users():
    with st.sidebar:
        if st.button("戻る"): change_page("admin_dashboard")
        
    st.title("👥 登録ユーザー一覧")
    
    for phone, u in db["users"].items():
        with st.container(border=True):
            st.write(f"**{u.get('name', '名無し')}** さん (📞 {phone}) - {u.get('city', '未設定')}")
            if st.button("🗑 アカウント削除", key=f"del_user_{phone}", type="primary"):
                del db["users"][phone]
                save_data(db)
                st.rerun()

# ==========================================
# ★ 画面の振り分け（ルーティング）
# ==========================================
if st.session_state.page == "login": show_login()
elif st.session_state.page == "register": show_register()
elif st.session_state.page == "job_list": show_job_list()
elif st.session_state.page == "job_detail": show_job_detail()
elif st.session_state.page == "post_job": show_post_job()
elif st.session_state.page == "history": show_history()
elif st.session_state.page == "admin_dashboard": show_admin_dashboard()
elif st.session_state.page == "admin_users": show_admin_users()
