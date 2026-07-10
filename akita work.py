import streamlit as st
import json
import uuid
import datetime
import os

# ==========================================
# ★ データベース設定（ファイル保存方式に変更！）
# Firebaseを使わず、システム内に「data.json」を作って保存します
# ==========================================
DATA_FILE = "data.json"

def load_data():
    # ファイルがあれば読み込み、なければ空のデータを作る
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"users": {}, "jobs": {}}

def save_data(data):
    # データをファイルに書き込んで保存する
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"保存エラー: {e}")

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

# --- ★日本時間を確実に取得する関数 ---
def get_japan_now():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).replace(tzinfo=None)

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
                # 少しだけ待たせずにすぐ切り替える
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
    now = get_japan_now()
    
    available_jobs = {}
    for jid, j in db["jobs"].items():
        if j.get("status") == "approved" and jid not in user_history:
            skip_job = False
            
            if "deadline_at" in j:
                try:
                    deadline_dt = datetime.datetime.strptime(j["deadline_at"], "%Y-%m-%d %H:%M:%S")
                    if now >= deadline_dt:
                        skip_job = True
                except: pass
            
            if "expire_at" in j:
                try:
                    expire_dt = datetime.datetime.strptime(j["expire_at"], "%Y-%m-%d %H:%M:%S")
                    if now >= expire_dt:
                        skip_job = True
                except: pass
            
            if skip_job:
                continue
                
            available_jobs[jid] = j
    
    if not available_jobs:
        st.info("現在募集中の求人はありません（すべて応募済み、期限切れ、または募集がありません）。")
    else:
        for jid, job in reversed(list(available_jobs.items())):
            with st.container(border=True):
                st.subheader(job["title"])
                
                deadline_str = "未設定"
                if "deadline_at" in job:
                    try:
                        dt = datetime.datetime.strptime(job["deadline_at"], "%Y-%m-%d %H:%M:%S")
                        deadline_str = dt.strftime("%Y年%m月%d日 %H:%M")
                    except: pass
                
                st.write(f"💰 **謝礼:** {job['pay']} ⏳ **締切:** {deadline_str}")
                st.write(f"⏰ **仕事日時:** {job['time']}")
                loc_type_label = f"[{job.get('loc_type', 'その他')}] " if job.get('loc_type') else ""
                st.write(f"📍 **場所:** {loc_type_label}{job['loc']}")
                
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
        
        deadline_str = "未設定"
        if "deadline_at" in job:
            try:
                dt = datetime.datetime.strptime(job["deadline_at"], "%Y-%m-%d %H:%M:%S")
                deadline_str = dt.strftime("%Y年%m月%d日 %H:%M")
            except: pass
            
        st.error(f"**⏳ 応募締切:** {deadline_str}")
        st.write(f"**⏰ 仕事日時:** {job['time']}")
        st.write(f"**💰 給与:** {job['pay']}")
        st.write(f"**🎒 持ち物:** {job['items']}")
        if job.get('loc_type'):
            st.write(f"**🏢 場所の種類:** {job['loc_type']}")
        st.write(f"**📍 詳しい勤務地:** {job['loc']}")
        
        import urllib.parse
        map_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(job['loc'])}"
        st.markdown(f"🗺️ [Googleマップで詳しい場所を開く（別タブ）]({map_url})")
    
    st.write("---")
    st.subheader("📝 応募フォーム（個人情報の入力）")
    st.write("このお仕事に応募するため、以下の項目を入力してください。")
    
    col_n1, col_n2 = st.columns(2)
    app_name_kana = col_n1.text_input("氏名（ふりがな）", placeholder="例: あきた たろう")
    app_address = col_n2.text_input("詳しい住所（番地・建物名）", placeholder="例: 山王1丁目1-1 〇〇ハイツ101")
    
    col1, col2 = st.columns(2)
    app_age = col1.number_input("年齢", min_value=15, max_value=100, value=20, step=1)
    app_gender = col2.selectbox("性別", ["男性", "女性", "その他", "回答しない"])
    
    col3, col4 = st.columns(2)
    app_occupation = col3.selectbox("現在のご職業", ["会社員", "自営業", "学生", "主婦・主夫", "フリーター", "無職", "その他"])
    app_transport = col4.selectbox("現地までの交通手段", ["自家用車（駐車場希望）", "公共交通機関（バス・電車）", "徒歩・自転車", "家族等の送迎", "その他"])
    
    col5, col6 = st.columns(2)
    app_license = col5.checkbox("🚗 普通自動車免許あり")
    app_exp = col6.selectbox("🌾 農業・屋外作業の経験", ["未経験", "少しある（家庭菜園・手伝い等）", "経験豊富（農家・業務経験あり）"])
    
    app_health = st.text_input("🏥 健康状態・アレルギー等（配慮が必要な場合）", placeholder="例: 特になし / 腰痛持ちのため重労働は厳しいです / 蜂アレルギーあり")
    app_message = st.text_area("💬 自己PR・管理者へのメッセージ", placeholder="例: 体力には自信があります！/ 土日いつでも動けます。よろしくお願いいたします。")
    
    if st.button("✨ この仕事に応募する", type="primary", use_container_width=True):
        now = get_japan_now()
        
        is_too_late = False
        if "deadline_at" in job:
            try:
                deadline_dt = datetime.datetime.strptime(job["deadline_at"], "%Y-%m-%d %H:%M:%S")
                if now >= deadline_dt:
                    is_too_late = True
            except: pass
            
        if is_too_late:
            st.error("申し訳ありません、このお仕事は応募締め切り時間を過ぎてしまいました。")
        elif not app_message:
            st.warning("「自己PR・管理者へのメッセージ」を入力してください。")
        else:
            user_history = st.session_state.user.get("history", [])
            if jid not in user_history:
                user_history.append(jid)
                st.session_state.user["history"] = user_history
                db["users"][st.session_state.phone]["history"] = user_history
                
                if "applicants" not in job or job["applicants"] is None:
                    job["applicants"] = {}
                
                now_str = now.strftime("%Y年%m月%d日 %H:%M")
                
                job["applicants"][st.session_state.phone] = {
                    "name": st.session_state.user.get("name", "名無し"),
                    "name_kana": app_name_kana,
                    "address": app_address,
                    "age": app_age,
                    "gender": app_gender,
                    "occupation": app_occupation,
                    "transport": app_transport,
                    "has_license": app_license,
                    "experience": app_exp,
                    "health": app_health,
                    "message": app_message,
                    "applied_at": now_str
                }
                db["jobs"][jid] = job
                
                save_data(db)
                st.success("応募が完了しました！")
                change_page("job_list")
        
    if st.button("一覧に戻る", use_container_width=True):
        change_page("job_list")

# ==========================================
# 4. お願い投稿画面 
# ==========================================
def show_post_job():
    st.title("➕ お願いを投稿")
    title = st.text_input("困りごと・内容 (例: 庭の草むしり)")
    
    st.write("**📅 仕事の日と時間**")
    japan_today = get_japan_now().date()
    job_date = st.date_input("仕事の日", value=japan_today)
    
    col1, col2 = st.columns(2)
    start_time = col1.time_input("始まりの時間", value=datetime.time(9, 0))
    end_time = col2.time_input("終わりの時間", value=datetime.time(12, 0))
    
    st.write("---")
    st.write("**⏳ 応募の締め切り**")
    col3, col4 = st.columns(2)
    deadline_date = col3.date_input("締め切りの日", value=japan_today)
    deadline_time = col4.time_input("締め切りの時間", value=datetime.time(8, 0))
    st.write("---")
    
    st.write("**💰 お礼・給与**")
    pay_options = [f"{i:,.0f}円" for i in range(500, 20500, 500)] + ["その他 (手入力)"]
    pay_sel = st.selectbox("金額を選ぶ (500円刻み)", pay_options, index=3)
    
    if pay_sel == "その他 (手入力)":
        pay = st.text_input("金額を入力 (例: 25,000円)")
    else:
        pay = pay_sel
    
    st.write("**📍 勤務地・集まる場所**")
    user_city = st.session_state.user.get('city', '')
    default_idx = akita_cities.index(user_city) if user_city in akita_cities else 0
    city = st.selectbox("市町村", akita_cities, index=default_idx)
    
    loc_type_options = ["個人宅（庭や屋内など）", "農地・畑・果樹園・山林", "店舗・商業施設・飲食店", "オフィス・事務所・工場", "公共施設（駅・公園・役所など）", "その他"]
    loc_type = st.selectbox("場所の種類・ジャンル", loc_type_options)
    
    loc_detail = st.text_input("詳しい住所・町名・建物名", placeholder="例: 山王1丁目1-1 など")
        
    items = st.text_input("🎒 持ち物や注意点 (例: 軍手、長靴)")
    
    if st.button("確認申請を送る", type="primary", use_container_width=True):
        if title and pay and loc_detail:
            
            start_datetime = datetime.datetime.combine(job_date, start_time)
            expire_datetime = datetime.datetime.combine(job_date, end_time)
            deadline_datetime = datetime.datetime.combine(deadline_date, deadline_time)
            
            if expire_datetime <= start_datetime:
                st.error("⚠️ エラー：「終わりの時間」は「始まりの時間」よりも【後】に設定してください。")
            elif deadline_datetime >= start_datetime:
                st.error("⚠️ エラー：「応募の締め切り」は、仕事が始まる時間よりも【前】に設定してください。")
            else:
                full_loc = f"秋田県{city} {loc_detail}".strip()
                
                date_str = job_date.strftime("%Y年%m月%d日")
                s_time_str = start_time.strftime("%H:%M")
                e_time_str = end_time.strftime("%H:%M")
                datetime_str = f"{date_str} {s_time_str}〜{e_time_str}"
                
                expire_str = expire_datetime.strftime("%Y-%m-%d %H:%M:%S")
                deadline_str = deadline_datetime.strftime("%Y-%m-%d %H:%M:%S")
                
                new_jid = str(uuid.uuid4())
                
                db["jobs"][new_jid] = {
                    "title": title, 
                    "time": datetime_str, 
                    "pay": pay, 
                    "loc": full_loc, 
                    "loc_type": loc_type,
                    "items": items, 
                    "status": "pending", 
                    "posted_by": st.session_state.user.get("name", "名無し"),
                    "expire_at": expire_str,
                    "deadline_at": deadline_str
                }
                save_data(db)
                
                st.success("管理者に申請しました！許可されると一覧に表示されます。")
                change_page("job_list")
        else:
            st.warning("未入力の項目があります。")
        
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
    now = get_japan_now()
    
    for jid, job in approved_jobs.items():
        with st.container(border=True):
            is_expired = False
            is_deadline_passed = False
            
            if "expire_at" in job:
                try:
                    expire_dt = datetime.datetime.strptime(job["expire_at"], "%Y-%m-%d %H:%M:%S")
                    if now >= expire_dt:
                        is_expired = True
                except: pass
                
            if "deadline_at" in job:
                try:
                    deadline_dt = datetime.datetime.strptime(job["deadline_at"], "%Y-%m-%d %H:%M:%S")
                    if now >= deadline_dt:
                        is_deadline_passed = True
                except: pass
            
            if is_expired:
                st.error("⏰ 【仕事終了・自動非表示中】")
            elif is_deadline_passed:
                st.warning("⏳ 【応募締め切り終了・自動非表示中】")
            
            st.markdown(f"### 💼 {job['title']}")
            
            deadline_str = "未設定"
            if "deadline_at" in job:
                try:
                    dt = datetime.datetime.strptime(job["deadline_at"], "%Y-%m-%d %H:%M:%S")
                    deadline_str = dt.strftime("%Y年%m月%d日 %H:%M")
                except: pass
                
            st.write(f"⏳ **締切:** {deadline_str} / ⏰ **日時:** {job['time']}")
            st.write(f"📍 **場所:** {job['loc']}")
            
            applicants = job.get("applicants", {})
            if applicants:
                st.write("👥 **この案件への応募者情報:**")
                for phone, app in applicants.items():
                    with st.container(border=True):
                        name_kana = app.get('name_kana', '')
                        kana_display = f"（{name_kana}）" if name_kana else ""
                        st.write(f"👤 **{app['name']}** さん {kana_display} ｜ {app['gender']} / {app['age']}歳 / {app.get('occupation', '不明')}")
                        st.write(f"🏠 **住所:** {app.get('address', '未記入')} ｜ 📞 **電話番号:** {phone}")
                        
                        license_mark = "✅ あり" if app.get('has_license') else "❌ なし"
                        st.write(f"🚗 **交通手段:** {app.get('transport', '不明')} ｜ 💳 **免許:** {license_mark}")
                        
                        st.write(f"🌾 **作業経験:** {app.get('experience', '不明')} ｜ 🏥 **健康状態・配慮:** {app.get('health', '特になし')}")
                        
                        st.write(f"💬 **自己PR・メッセージ:** {app['message']}")
            else:
                st.write("⚪ *まだ応募者はいません*")
                
            st.write("")
            if st.button("🗑 掲載を終了・削除", key=f"del_pub_{jid}", type="primary"):
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
