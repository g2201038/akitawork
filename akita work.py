import streamlit as st
import json
import uuid
import datetime
import os
import urllib.parse

# ==========================================
# ★ データベース設定（ファイル保存方式）
# ==========================================
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"users": {}, "jobs": {}}

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"保存エラー: {e}")

# --- アプリの基本設定 ---
st.set_page_config(page_title="あきたワーク Pro", page_icon="🌾", layout="centered", initial_sidebar_state="collapsed")

# ==========================================
# ✨ 劇的美術・デザインCSSの注入！
# ==========================================
st.markdown("""
    <style>
    /* Google Fontsから美しい日本語フォントを読み込み */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap');
    
    /* 全体の背景とフォントの設定 */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Noto Sans JP', sans-serif !important;
        background-color: #f4f7f6 !important; /* 目に優しい高級感のある薄いグレー */
    }
    
    /* メインタイトルのビューティフル化 */
    .beauty-title {
        font-size: 2.6rem;
        font-weight: 700;
        background: linear-gradient(135deg, #11998e, #38ef7d); /* 爽やかなエメラルドグラデーション */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: -1rem;
        margin-bottom: 0.5rem;
        letter-spacing: 1px;
    }
    .beauty-subtitle {
        text-align: center;
        color: #666;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }
    
    /* 標準のH1, H2, H3の美化 */
    h1, h2, h3 {
        font-family: 'Noto Sans JP', sans-serif !important;
    }
    h1 { color: #1e3d2f !important; font-weight: 700 !important; }
    h2 { color: #2e6f40 !important; font-weight: 600 !important; border-left: 5px solid #38ef7d; padding-left: 10px; }
    h3 { color: #333333 !important; font-weight: 600 !important; }

    /* Streamlitのコンテナ（border=True）を美しい高級カード化 */
    div[data-testid="stVerticalBlockBorderedTest"] {
        background-color: #ffffff !important;
        border: 1px solid rgba(0,0,0,0.04) !important;
        border-radius: 16px !important; /* 滑らかな角丸 */
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.04) !important; /* 高級感のあるソフトな影 */
        padding: 1.8rem !important;
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    /* ボタンの超美化 */
    .stButton>button {
        border-radius: 10px !important;
        font-weight: 500 !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: 1px solid #e0e0e0 !important;
        background-color: #ffffff;
        color: #333;
    }
    /* プライマリ（主ボタン）のグラデーション化 */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #11998e, #27ae60) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(39, 174, 96, 0.25) !important;
    }
    /* ボタンにホバーした時のアニメーション */
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08) !important;
        border-color: #11998e !important;
    }
    .stButton>button[kind="primary"]:hover {
        box-shadow: 0 8px 25px rgba(39, 174, 96, 0.4) !important;
    }
    
    /* 入力フォームの美化 */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea, .stNumberInput>div>div>input {
        border-radius: 10px !important;
        border: 1px solid #dee2e6 !important;
        background-color: #fafafa !important;
        transition: all 0.2s ease !important;
    }
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>div:focus, .stTextArea>div>div>textarea:focus {
        border-color: #11998e !important;
        background-color: #ffffff !important;
        box-shadow: 0 0 0 3px rgba(17, 153, 142, 0.1) !important;
    }
    
    /* タブの美化 */
    button[data-testid="stMarkdownContainer"] p {
        font-weight: 500;
    }
    
    /* サイドバーの高級化 */
    section[data-testid="stSidebar"] {
        background-color: #1e2d24 !important;
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] h3, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] .stButton>button {
        background-color: rgba(255,255,255,0.08) !important;
        color: #fff !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }
    section[data-testid="stSidebar"] .stButton>button:hover {
        background-color: rgba(255,255,255,0.2) !important;
    }
    </style>
""", unsafe_allow_html=True)

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

def get_japan_now():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).replace(tzinfo=None)

# ==========================================
# 1. ログイン画面
# ==========================================
def show_login():
    st.markdown('<div class="beauty-title">🌾 あきたワーク Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="beauty-subtitle">秋田の「助けて」と「お手伝い」を美しくつなぐクラウドプラットフォーム</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["👤 一般ユーザーとして利用", "🏢 管理者・企業としてログイン"])
    
    with tab1:
        with st.container(border=True):
            phone = st.text_input("登録電話番号", key="log_phone", placeholder="例: 09012345678")
            password = st.text_input("暗証番号 (4桁)", type="password", key="log_pass", placeholder="••••")
            st.write("")
            if st.button("ログインする", type="primary", use_container_width=True):
                user = db["users"].get(phone)
                if user and user.get("pass") == password:
                    st.session_state.user = user
                    st.session_state.phone = phone
                    change_page("job_list")
                else:
                    st.error("お電話番号または暗証番号が正しくありません。")
        
        st.write("")
        if st.button("初めての方はこちら（新規登録）", use_container_width=True):
            change_page("register")
            
    with tab2:
        with st.container(border=True):
            admin_id = st.text_input("管理者ID", key="log_admin_id", placeholder="管理コード入力")
            admin_pass = st.text_input("パスワード", type="password", key="log_admin_pass", placeholder="••••••••")
            st.write("")
            if st.button("管理者専用ログイン", type="primary", use_container_width=True):
                if admin_id == "9999" and admin_pass == "9999":
                    change_page("admin_dashboard")
                else:
                    st.error("管理者認証情報が一致しません。")

def show_register():
    st.markdown('<div class="beauty-title">📝 新規アカウント作成</div>', unsafe_allow_html=True)
    st.markdown('<div class="beauty-subtitle">わずか1分で登録完了！すぐにお仕事を探せます</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        name = st.text_input("お名前（姓名）", placeholder="例: 秋田 太郎")
        phone = st.text_input("電話番号（ログインIDになります）", placeholder="例: 09012345678")
        password = st.text_input("暗証番号 (好きな4桁の数字)", type="password", max_chars=4, placeholder="例: 1234")
        city = st.selectbox("お住まいの市町村", akita_cities)
        st.write("")
        
        if st.button("この内容で登録する", type="primary", use_container_width=True):
            if name and phone and password:
                if phone in db["users"]:
                    st.error("この電話番号はすでに登録されています。別の番号をご使用ください。")
                else:
                    db["users"][phone] = {
                        "name": name, "pass": password, "city": city, "history": []
                    }
                    save_data(db)
                    st.success("🎉 アカウントの作成が成功しました！ログインしてください。")
                    change_page("login")
            else:
                st.warning("すべての必須項目を入力してください。")
    
    st.write("")
    if st.button("ログイン画面に戻る", use_container_width=True):
        change_page("login")

# ==========================================
# 2. 仕事一覧画面
# ==========================================
def show_job_list():
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user.get('name', 'ゲスト')} さん")
        user_city = st.session_state.user.get('city', '未設定')
        st.markdown(f"📍 拠点: **{user_city}**")
        st.divider()
        if st.button("➕ お願いを新規投稿", use_container_width=True): change_page("post_job")
        if st.button("📋 自分の応募履歴", use_container_width=True): change_page("history")
        st.divider()
        if st.button("ログアウト", use_container_width=True):
            st.session_state.user = None
            st.session_state.phone = None
            change_page("login")

    st.markdown('<div class="beauty-title">🌾 現在募集中の求人一覧</div>', unsafe_allow_html=True)
    
    user_history = st.session_state.user.get("history", [])
    now = get_japan_now()
    
    available_jobs = {}
    for jid, j in db["jobs"].items():
        if j.get("status") == "approved" and jid not in user_history:
            skip_job = False
            
            if "deadline_at" in j:
                try:
                    deadline_dt = datetime.datetime.strptime(j["deadline_at"], "%Y-%m-%d %H:%M:%S")
                    if now >= deadline_dt: skip_job = True
                except: pass
            
            if "expire_at" in j:
                try:
                    expire_dt = datetime.datetime.strptime(j["expire_at"], "%Y-%m-%d %H:%M:%S")
                    if now >= expire_dt: skip_job = True
                except: pass
            
            if skip_job: continue
                
            available_jobs[jid] = j
    
    if not available_jobs:
        st.info("現在募集中の求人はありません（すべて応募済み、もしくは期限切れです）。")
    else:
        for jid, job in reversed(list(available_jobs.items())):
            with st.container(border=True):
                # タイトルをオシャレに
                st.markdown(f"### 💼 {job['title']}")
                
                deadline_str = "未設定"
                if "deadline_at" in job:
                    try:
                        dt = datetime.datetime.strptime(job["deadline_at"], "%Y-%m-%d %H:%M:%S")
                        deadline_str = dt.strftime("%Y年%m月%d日 %H:%M")
                    except: pass
                
                # 情報のレイアウトをスッキリ綺麗に
                col_a, col_b = st.columns(2)
                col_a.markdown(f"💰 **謝礼・給与:** <span style='color:#e74c3c; font-weight:bold; font-size:1.1rem;'>{job['pay']}</span>", unsafe_allow_html=True)
                col_b.markdown(f"⏳ **応募締切:** <span style='color:#7f8c8d;'>{deadline_str}</span>", unsafe_allow_html=True)
                
                st.markdown(f"⏰ **稼働日時:** {job['time']}")
                loc_type_label = f"🍃 [{job.get('loc_type', 'その他')}] " if job.get('loc_type') else ""
                st.markdown(f"📍 **勤務場所:** {loc_type_label}{job['loc']}")
                
                st.write("")
                if st.button("詳細を見て応募する", key=f"det_{jid}", type="primary", use_container_width=True):
                    st.session_state.current_job_id = jid
                    change_page("job_detail")

# ==========================================
# 3. 仕事詳細画面
# ==========================================
def show_job_detail():
    jid = st.session_state.current_job_id
    job = db["jobs"].get(jid)
    
    if not job:
        st.error("このお仕事は終了したか、削除された可能性があります。")
        if st.button("一覧に戻る"): change_page("job_list")
        return

    st.markdown('<div class="beauty-title">📋 募集案件の詳細情報</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown(f"## 💼 {job['title']}")
        
        deadline_str = "未設定"
        if "deadline_at" in job:
            try:
                dt = datetime.datetime.strptime(job["deadline_at"], "%Y-%m-%d %H:%M:%S")
                deadline_str = dt.strftime("%Y年%m月%d日 %H:%M")
            except: pass
            
        st.error(f"⚠️ **応募締め切り時間:** {deadline_str}")
        
        st.write("")
        col_d1, col_d2 = st.columns(2)
        col_d1.markdown(f"💰 **給与・お礼:** \n### {job['pay']}")
        col_d2.markdown(f"⏰ **仕事日時:** \n{job['time']}")
        
        st.divider()
        st.markdown(f"🎒 **持ち物・必要なもの:** \n{job['items']}")
        if job.get('loc_type'):
            st.markdown(f"🏢 **場所のジャンル:** \n{job['loc_type']}")
        st.markdown(f"📍 **正確な勤務地:** \n{job['loc']}")
        
        map_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(job['loc'])}"
        st.markdown(f"🗺️ [➡️ Googleマップでルートを確認する（別タブ）]({map_url})")
    
    st.write("")
    st.markdown("## 📝 応募フォーム（個人情報の入力）")
    st.caption("採用管理者に開示される詳細な個人情報です。正確に入力してください。")
    
    with st.container(border=True):
        col_n1, col_n2 = st.columns(2)
        app_name_kana = col_n1.text_input("氏名（ふりがな）", placeholder="あきた たろう")
        app_address = col_n2.text_input("詳しい現住所（番地・建物名まで）", placeholder="秋田市山王1丁目1-1 〇〇ビル2F")
        
        col1, col2 = st.columns(2)
        app_age = col1.number_input("ご年齢", min_value=15, max_value=100, value=20, step=1)
        app_gender = col2.selectbox("性別", ["男性", "女性", "その他", "回答しない"])
        
        col3, col4 = st.columns(2)
        app_occupation = col3.selectbox("現在のご職業", ["会社員", "自営業", "学生", "主婦・主夫", "フリーター", "無職", "その他"])
        app_transport = col4.selectbox("現地までの移動手段", ["自家用車（要駐車場）", "公共交通機関", "徒歩・自転車", "送迎あり", "その他"])
        
        col5, col6 = st.columns(2)
        app_license = col5.checkbox("🚗 普通自動車免許を所持している")
        app_exp = col6.selectbox("🌾 農業・屋外作業の経験値", ["未経験", "少し経験あり（家庭菜園・手伝いなど）", "経験豊富（農家・現場業務経験あり）"])
        
        app_health = st.text_input("🏥 健康状態・アレルギー等（配慮事項があればご記入ください）", placeholder="例: 特になし / 腰痛ありのため重労働不可 / 蜂アレルギー等")
        app_message = st.text_area("💬 自己PR・管理者へのメッセージ（必須）", placeholder="例: 体力に自信があります！精一杯お手伝いさせていただきます。")
        st.write("")
        
        if st.button("✨ この内容で正式に応募する", type="primary", use_container_width=True):
            now = get_japan_now()
            
            is_too_late = False
            if "deadline_at" in job:
                try:
                    deadline_dt = datetime.datetime.strptime(job["deadline_at"], "%Y-%m-%d %H:%M:%S")
                    if now >= deadline_dt: is_too_late = True
                except: pass
                
            if is_too_late:
                st.error("大変申し訳ありません。タッチの差で応募締め切り時間を過ぎてしまいました。")
            elif not app_message:
                st.warning("「自己PR・管理者へのメッセージ」を記入してください。")
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
                    st.success("🎉 応募が完了しました！管理者からの連絡をお待ちください。")
                    change_page("job_list")
        
    if st.button("一覧に戻る", use_container_width=True):
        change_page("job_list")

# ==========================================
# 4. お願い投稿画面 
# ==========================================
def show_post_job():
    st.markdown('<div class="beauty-title">➕ お願い（お仕事）を投稿する</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        title = st.text_input("お仕事のタイトル・困りごと", placeholder="例: 枝豆の収穫・袋詰め作業の手伝い")
        
        st.markdown("### 📅 稼働日時")
        japan_today = get_japan_now().date()
        job_date = st.date_input("稼働日", value=japan_today)
        
        col1, col2 = st.columns(2)
        start_time = col1.time_input("開始時刻", value=datetime.time(9, 0))
        end_time = col2.time_input("終了時刻", value=datetime.time(12, 0))
        
        st.divider()
        st.markdown("### ⏳ 応募の締め切り")
        col3, col4 = st.columns(2)
        deadline_date = col3.date_input("締め切り日", value=japan_today)
        deadline_time = col4.time_input("締め切り時刻", value=datetime.time(8, 0))
        
        st.divider()
        st.markdown("### 💰 謝礼・給料金額")
        pay_options = [f"{i:,.0f}円" for i in range(500, 20500, 500)] + ["その他 (手入力)"]
        pay_sel = st.selectbox("金額を選択 (500円刻み)", pay_options, index=3)
        pay = st.text_input("手入力用の金額 (例: 日給20,000円)") if pay_sel == "その他 (手入力)" else pay_sel
        
        st.divider()
        st.markdown("### 📍 勤務地・集合場所")
        user_city = st.session_state.user.get('city', '')
        default_idx = akita_cities.index(user_city) if user_city in akita_cities else 0
        city = st.selectbox("対象の市町村", akita_cities, index=default_idx)
        
        loc_type_options = ["個人宅（庭や屋内など）", "農地・畑・果樹園・山林", "店舗・商業施設・飲食店", "オフィス・事務所・工場", "公共施設（駅・公園・役所など）", "その他"]
        loc_type = st.selectbox("場所の種類・ジャンル", loc_type_options)
        loc_detail = st.text_input("番地・建物名・農地名など詳しい場所", placeholder="山王1丁目1-1 〇〇農園のビニールハウス集合")
            
        st.divider()
        items = st.text_input("🎒 持ち物や服装の注意点", placeholder="例: 軍手、汚れてもいい長靴、帽子、水分補給用飲料")
        st.write("")
        
        if st.button("事務局へ確認申請を提出する", type="primary", use_container_width=True):
            if title and pay and loc_detail:
                start_datetime = datetime.datetime.combine(job_date, start_time)
                expire_datetime = datetime.datetime.combine(job_date, end_time)
                deadline_datetime = datetime.datetime.combine(deadline_date, deadline_time)
                
                if expire_datetime <= start_datetime:
                    st.error("⚠️ 「終了時刻」は「開始時刻」より後の時間に設定してください。")
                elif deadline_datetime >= start_datetime:
                    st.error("⚠️ 「応募の締め切り」は、実際の仕事が始まる日時より前に設定してください。")
                else:
                    full_loc = f"秋田県{city} {loc_detail}".strip()
                    date_str = job_date.strftime("%Y年%m月%d日")
                    datetime_str = f"{date_str} {start_time.strftime('%H:%M')}〜{end_time.strftime('%H:%M')}"
                    
                    new_jid = str(uuid.uuid4())
                    db["jobs"][new_jid] = {
                        "title": title, "time": datetime_str, "pay": pay, "loc": full_loc, "loc_type": loc_type,
                        "items": items, "status": "pending", "posted_by": st.session_state.user.get("name", "名無し"),
                        "expire_at": expire_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                        "deadline_at": deadline_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    save_data(db)
                    st.success("📨 事務局へ確認申請を送信しました！承認され次第、全体に掲載されます。")
                    change_page("job_list")
            else:
                st.warning("未入力の項目があります。")
        
    if st.button("投稿をやめて戻る", use_container_width=True):
        change_page("job_list")

# ==========================================
# 5. 応募履歴
# ==========================================
def show_history():
    st.markdown('<div class="beauty-title">📋 あなたの応募履歴</div>', unsafe_allow_html=True)
    history_jids = st.session_state.user.get("history", [])
    
    if not history_jids:
        st.info("まだお仕事への応募履歴がありません。")
    else:
        for jid in history_jids:
            job = db["jobs"].get(jid)
            with st.container(border=True):
                if job:
                    st.success(f"✅ 応募済み: **{job['title']}**")
                    st.caption(f"日時: {job['time']} ｜ 給与: {job['pay']}")
                else:
                    st.warning("このお仕事は掲載終了、または削除されました。")
            
    st.write("")
    if st.button("一覧に戻る", type="primary", use_container_width=True):
        change_page("job_list")

# ==========================================
# 6. 管理者画面
# ==========================================
def show_admin_dashboard():
    with st.sidebar:
        st.title("🏢 管理者コントロール")
        if st.button("👥 登録会員の管理", use_container_width=True): change_page("admin_users")
        st.divider()
        if st.button("ログアウト", use_container_width=True): change_page("login")

    st.markdown('<div class="beauty-title">⚙️ あきたワーク 総合統括画面</div>', unsafe_allow_html=True)
    
    pending_jobs = {jid: j for jid, j in db["jobs"].items() if j.get("status") == "pending"}
    approved_jobs = {jid: j for jid, j in db["jobs"].items() if j.get("status") == "approved"}
    
    st.markdown(f"## 📥 新着・承認待ち案件 ({len(pending_jobs)}件)")
    for jid, job in pending_jobs.items():
        with st.container(border=True):
            st.markdown(f"### 💼 {job['title']}")
            st.write(f"投稿者: {job.get('posted_by')} さん")
            st.write(f"日時: {job['time']} ｜ 場所: {job['loc']}")
            col1, col2 = st.columns(2)
            if col1.button("✅ 掲載を許可する", key=f"app_admin_{jid}", type="primary", use_container_width=True):
                db["jobs"][jid]["status"] = "approved"
                save_data(db)
                st.rerun()
            if col2.button("🗑 却下・削除", key=f"del_admin_{jid}", use_container_width=True):
                del db["jobs"][jid]
                save_data(db)
                st.rerun()

    st.markdown(f"## 🟢 現在掲載中の求人一覧 ({len(approved_jobs)}件)")
    now = get_japan_now()
    
    for jid, job in approved_jobs.items():
        with st.container(border=True):
            is_expired = False
            is_deadline_passed = False
            if "expire_at" in job:
                try:
                    if now >= datetime.datetime.strptime(job["expire_at"], "%Y-%m-%d %H:%M:%S"): is_expired = True
                except: pass
            if "deadline_at" in job:
                try:
                    if now >= datetime.datetime.strptime(job["deadline_at"], "%Y-%m-%d %H:%M:%S"): is_deadline_passed = True
                except: pass
            
            if is_expired: st.error("⏰ 【稼働時間終了のため自動で非表示中】")
            elif is_deadline_passed: st.warning("⏳ 【応募締め切りを過ぎたため自動で非表示中】")
            
            st.markdown(f"### 💼 {job['title']}")
            st.write(f"日時: {job['time']} ｜ 場所: {job['loc']}")
            
            applicants = job.get("applicants", {})
            if applicants:
                st.markdown("#### 👥 この案件への応募者（詳細プロフィール）:")
                for phone, app in applicants.items():
                    with st.container(border=True):
                        name_kana = app.get('name_kana', '')
                        kana_display = f"（{name_kana}）" if name_kana else ""
                        st.markdown(f"👤 **{app['name']}** さん{kana_display} ｜ {app['gender']} / {app['age']}歳 / {app.get('occupation')}")
                        st.write(f"🏠 住所: {app.get('address')} ｜ 📞 連絡先: {phone}")
                        license_mark = "✅ あり" if app.get('has_license') else "❌ なし"
                        st.write(f"🚗 移動手段: {app.get('transport')} ｜ 普通免許: {license_mark}")
                        st.write(f"🌾 作業経験: {app.get('experience')} ｜ 🏥 配慮事項: {app.get('health')}")
                        st.info(f"💬 メッセージ:\n{app['message']}")
            else:
                st.caption("⚪ まだ応募者はいません")
                
            st.write("")
            if st.button("🗑️ この掲載を終了して削除", key=f"del_pub_{jid}", use_container_width=True):
                del db["jobs"][jid]
                save_data(db)
                st.rerun()

def show_admin_users():
    with st.sidebar:
        if st.button("ダッシュボードに戻る", use_container_width=True): change_page("admin_dashboard")
        
    st.markdown('<div class="beauty-title">👥 全登録ユーザーの管理</div>', unsafe_allow_html=True)
    
    for phone, u in db["users"].items():
        with st.container(border=True):
            st.markdown(f"### 👤 {u.get('name', '名無し')} さん")
            st.write(f"📞 電話番号: {phone} ｜ 📍 登録エリア: {u.get('city', '未設定')}")
            if st.button("🗑️ このアカウントを削除", key=f"del_user_{phone}", type="primary"):
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
