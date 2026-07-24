import streamlit as st
import json
import uuid
import datetime
import os
import urllib.parse
import urllib.request
import base64

# ==========================================
# ★ データベース設定
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

# ==========================================
# ★ 画像をBase64にエンコードする関数
# ==========================================
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# ロゴ画像のパス（Streamlitを実行するディレクトリからの相対パス）
LOGO_FILE = "image_26.png"
if os.path.exists(LOGO_FILE):
    base64_logo = get_base64_of_bin_file(LOGO_FILE)
    logo_html_raw = f'data:image/png;base64,{base64_logo}'
else:
    logo_html_raw = ""
    base64_logo = ""

# ==========================================
# ★ アプリ設定（Faviconとタイトル）
# ==========================================
st.set_page_config(
    page_title="老-MEE Pro (老ミー プロ)",
    page_icon=base64_logo if base64_logo else "🌾",
    layout="wide", # 画面を広く使う
    initial_sidebar_state="collapsed"
)

# ==========================================
# ✨ デザインCSS（新しい分割レイアウトとロゴ適用）
# ==========================================
# 画像のデザインを再現するためのカスタムCSS。
# 画面全体をティールグリーンにし、左側にクリーム色のパネルを配置。
css_str = f"""
    <style>
    /* 全体設定 */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', 'メイリオ', Meiryo, sans-serif !important;
        background-color: #1D5E5A !important; /* 深いティールグリーン */
        color: #FFFFFF !important;
        margin: 0;
        padding: 0;
    }}
    
    /* 画面分割設定 */
    .st-emotion-cache-z5fcl4 {{
        width: 100%;
        padding: 0;
    }}
    [data-testid="stAppViewContainer"] > section > div {{
        padding: 0;
    }}

    p, li, .stMarkdown {{
        font-size: 1.05rem !important;
        line-height: 1.8 !important;
        letter-spacing: 0.03em !important;
    }}

    /* ロゴ・タイトル用CSS */
    .app-logo-img {{
        content: url('{logo_html_raw}');
        height: auto;
        width: 100%;
        max-width: 250px;
        display: block;
        margin: 0 auto 10px;
    }}
    .app-logo-img-small {{
        content: url('{logo_html_raw}');
        height: 60px;
        width: auto;
        display: block;
        margin: 0 auto 10px;
    }}
    
    .beauty-title {{
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin: 0 0 10px;
        color: #FFFFFF !important;
    }}
    
    .beauty-subtitle {{
        text-align: center;
        color: #FFFFFF;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 600;
    }}

    /* 左パネル（紹介エリア） */
    .intro-panel-wrapper {{
        background-color: #FDF9F1 !important; /* クリーム色 */
        color: #1D5E5A !important; /* ティールグリーン */
        width: 50vw;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 40px;
        float: left;
    }}
    
    /* 紹介パネル内ロゴ用CSS */
    .intro-panel-wrapper .app-logo-img {{
        max-width: 350px;
    }}
    .intro-panel-wrapper .beauty-title {{
        color: #1D5E5A !important;
        font-size: 4rem;
    }}
    .intro-panel-wrapper .beauty-subtitle {{
        color: #1D5E5A !important;
        font-size: 1.5rem;
    }}
    
    /* ブラウザタブ風CSS */
    .browser-tab {{
        background-color: #FFFFFF;
        color: #222222;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 10px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: auto;
        margin-bottom: 40px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    
    .browser-tab span {{
        font-size: 1rem;
        font-weight: 600;
    }}
    
    .browser-tab img {{
        height: 30px;
        width: auto;
        margin-right: 15px;
    }}
    
    .browser-tab .close-btn {{
        background: none;
        border: none;
        color: #757575;
        font-weight: bold;
        cursor: pointer;
    }}

    /* 右パネル（ログインエリア） */
    .login-panel-wrapper {{
        width: 50vw;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 40px;
        float: right;
    }}
    
    /* ログインフォームパネルCSS */
    [data-testid="stVerticalBlockBorderedTest"] {{
        background-color: #ffffff !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
        padding: 1.8rem !important; 
        margin-bottom: 1.2rem;
    }}
    
    [data-testid="stVerticalBlockBorderedTest"] input,
    [data-testid="stVerticalBlockBorderedTest"] textarea {{
        color: #222222 !important;
    }}
    
    /* ログインボタン・グラデーション適用 */
    .stButton>button[kind="primary"] {{
        border-radius: 30px !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        padding: 0.6rem 2rem !important;
        /* ゴールドからシルバーへのグラデーション */
        background: linear-gradient(135deg, #FFD700, #C0C0C0) !important;
        border: none !important;
        color: #3E2723 !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
    }}
    
    .stButton>button[kind="primary"] p {{ color: #3E2723 !important; }}
    
    /* 入力フィールドのカスタマイズ */
    .stTextInput>div>div>input {{
        border-radius: 8px !important;
        border: 2px solid #FFE0B2 !important;
        background-color: #FFFDF9 !important;
    }}
    
    [data-testid="stVerticalBlockBorderedTest"] label {{
        color: #3E2723 !important;
        font-weight: 600;
    }}

    @media (max-width: 768px) {{
        .intro-panel-wrapper, .login-panel-wrapper {{
            width: 100vw;
            height: auto;
            float: none;
            padding: 20px;
        }}
    }}
    </style>
"""
st.markdown(css_str, unsafe_allow_html=True)

# データの初期化
db = load_data()
if "users" not in db or db["users"] is None: db["users"] = {}
if "jobs" not in db or db["jobs"] is None: db["jobs"] = {}

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
    # ------------------------------------------
    # ★ 新しいログイン・紹介画面
    # ------------------------------------------
    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        # ------------------------------------------
        # 左パネル：紹介エリア
        # ------------------------------------------
        st.markdown('<div class="intro-panel-wrapper">', unsafe_allow_html=True)
        # ブラウザタブ風デザイン
        if logo_html_raw:
            st.markdown(f'<div class="browser-tab"><img src="{logo_html_raw}" alt="老-MEEアイコン"><span>老-MEE | 仕事と暮らし、あなたのまちで。</span><button class="close-btn">X</button></div>', unsafe_allow_html=True)
        # 大きなロゴ
        st.markdown('<div class="app-logo-img"></div>', unsafe_allow_html=True)
        # タイトルとSubtitle
        st.markdown('<div class="beauty-title">老-MEE</div>', unsafe_allow_html=True)
        st.markdown('<div class="beauty-subtitle">仕事と暮らし、あなたのまちで。</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        # ------------------------------------------
        # 右パネル：ログインエリア
        # ------------------------------------------
        st.markdown('<div class="login-panel-wrapper">', unsafe_allow_html=True)
        # 小さなロゴとタイトル
        st.markdown('<div class="app-logo-img-small"></div>', unsafe_allow_html=True)
        st.markdown('<div class="beauty-title">老-MEE Pro</div>', unsafe_allow_html=True)
        st.markdown('<div class="beauty-subtitle">地域で助け合う、新しいお仕事マッチング</div>', unsafe_allow_html=True)
        
        with st.container(border=True):
            tab1, tab2 = st.tabs(["ログイン", "新規登録"])
            
            with tab1:
                phone = st.text_input("電話", key="log_phone", placeholder="例: 09012345678")
                password = st.text_input("パスワード", type="password", key="log_pass", placeholder="••••")
                st.write("")
                # primary Kind を使用してグラデーションを適用
                if st.button("プリマりログイン", type="primary", use_container_width=True):
                    user = db["users"].get(phone)
                    if user and user.get("pass") == password:
                        st.session_state.user = user
                        st.session_state.phone = phone
                        change_page("job_list")
                    else:
                        st.error("電話番号または暗証番号が違います。")
                st.markdown('<div style="text-align:center;"><a href="#" style="color:#757575; font-size:0.9rem;">パスワードを忘れた場合</a></div>', unsafe_allow_html=True)
            
            with tab2:
                name = st.text_input("お名前（姓名）", placeholder="例: 秋田 太郎")
                phone_reg = st.text_input("電話番号（ログインIDになります）", placeholder="例: 09012345678")
                password_reg = st.text_input("暗証番号 (好きな4桁の数字)", type="password", max_chars=4, placeholder="例: 1234")
                city = st.selectbox("お住まいの市町村", akita_cities)
                st.write("")
                
                if st.button("この内容で登録する", type="primary", use_container_width=True):
                    if name and phone_reg and password_reg:
                        if phone_reg in db["users"]:
                            st.error("この電話番号はすでに登録されています。")
                        else:
                            db["users"][phone_reg] = {"name": name, "pass": password_reg, "city": city, "history": []}
                            save_data(db)
                            st.success("🎉 登録完了しました！ログインしてください。")
                            # ログインタブに戻るようにしたいが、初心者向けにはここまでとする。
                            change_page("login")
                    else:
                        st.warning("すべての項目を入力してください。")
        st.markdown('</div>', unsafe_allow_html=True)

def show_register():
    # 登録画面はshow_login内で完結させる。
    pass

# ==========================================
# 2. 仕事一覧画面
# ==========================================
def show_job_list():
    with st.sidebar:
        # サイドバーにも小さなロゴ
        st.markdown(f'<div style="text-align:center; margin-bottom:10px;"><img src="{logo_html_raw}" height="60px"></div>', unsafe_allow_html=True)
        st.markdown(f"### 👤 {st.session_state.user.get('name', 'ゲスト')} さん")
        st.markdown(f"📍 拠点: **{st.session_state.user.get('city', '未設定')}**")
        st.divider()
        if st.button("➕ お願いを新規投稿", use_container_width=True): change_page("post_job")
        if st.button("📢 自分の募集・応募者を見る", use_container_width=True): change_page("my_posts")
        if st.button("📋 自分の応募履歴とチャット", use_container_width=True): change_page("history")
        st.divider()
        if st.button("ログアウト", use_container_width=True):
            st.session_state.user = None
            st.session_state.phone = None
            change_page("login")

    # タイトル部分
    st.markdown('<div class="beauty-title"><div class="app-logo-img-small"></div>募集中の求人一覧</div>', unsafe_allow_html=True)
    
    user_history = st.session_state.user.get("history", [])
    now = get_japan_now()
    available_jobs = {}
    
    for jid, j in db["jobs"].items():
        if j.get("posted_by_phone") == st.session_state.phone:
            continue
            
        if j.get("status") == "approved" and jid not in user_history:
            skip_job = False
            if "deadline_at" in j:
                try:
                    if now >= datetime.datetime.strptime(j["deadline_at"], "%Y-%m-%d %H:%M:%S"): skip_job = True
                except: pass
            if "expire_at" in j:
                try:
                    if now >= datetime.datetime.strptime(j["expire_at"], "%Y-%m-%d %H:%M:%S"): skip_job = True
                except: pass
            if skip_job: continue
            available_jobs[jid] = j
    
    if not available_jobs:
        st.info("現在募集中の求人はありません（すべて応募済み、もしくは期限切れです）。")
    else:
        for jid, job in reversed(list(available_jobs.items())):
            with st.container(border=True):
                st.markdown(f"### 💼 {job['title']}")
                
                deadline_str = "未設定"
                if "deadline_at" in job:
                    try:
                        dt = datetime.datetime.strptime(job["deadline_at"], "%Y-%m-%d %H:%M:%S")
                        deadline_str = dt.strftime("%Y/%m/%d %H:%M")
                    except: pass
                
                col_a, col_b = st.columns(2)
                col_a.markdown(f"💰 **謝礼:** <span style='color:#D84315; font-weight:bold; font-size:1.2rem;'>{job['pay']}</span>", unsafe_allow_html=True)
                col_b.markdown(f"⏳ **締切:** {deadline_str}")
                
                st.markdown(f"⏰ **日時:** {job['time']}")
                st.markdown(f"📍 **場所:** {job['loc']}")
                
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
        st.error("このお仕事は終了しました。")
        if st.button("一覧に戻る"): change_page("job_list")
        return

    st.markdown('<div class="beauty-title"><div class="app-logo-img-small"></div>募集案件の詳細</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown(f"## 💼 {job['title']}")
        st.error(f"⚠️ **応募締め切り:** {job.get('deadline_at', '未設定')}")
        st.write("")
        col_d1, col_d2 = st.columns(2)
        col_d1.markdown(f"💰 **給与:** \n### {job['pay']}")
        col_d2.markdown(f"⏰ **仕事日時:** \n{job['time']}")
        st.divider()
        st.markdown(f"🎒 **持ち物:** \n{job['items']}")
        st.markdown(f"📍 **勤務地:** \n{job['loc']}")
        map_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(job['loc'])}"
        st.markdown(f"🗺️ [Googleマップで確認（別タブ）]({map_url})")
    
    st.write("")
    st.markdown("## 📝 応募フォーム")
    
    with st.container(border=True):
        st.markdown("#### 📍 現住所の検索（自動入力）")
        col_z1, col_z2 = st.columns([2, 1])
        app_zip = col_z1.text_input("郵便番号（ハイフンなし）", placeholder="例: 0100951", key="app_zip")
        if col_z2.button("🔍 住所を検索", key="app_zip_btn", use_container_width=True):
            if app_zip:
                url = f"https://zipcloud.ibsnet.co.jp/api/search?zipcode={app_zip}"
                try:
                    req = urllib.request.Request(url)
                    with urllib.request.urlopen(req) as response:
                        res_json = json.loads(response.read().decode("utf-8"))
                        if res_json["status"] == 200 and res_json["results"]:
                            data = res_json["results"][0]
                            st.session_state.app_address_input = f"{data['address1']}{data['address2']}{data['address3']}"
                            st.rerun()
                        else:
                            st.error("郵便番号が見つかりませんでした。")
                except Exception:
                    st.error("通信エラーが発生しました。")
        
        if "app_address_input" not in st.session_state:
            st.session_state.app_address_input = ""
            
        st.divider()

        col_n1, col_n2 = st.columns(2)
        app_name_kana = col_n1.text_input("氏名（ふりがな）")
        app_address = col_n2.text_input("詳しい現住所（番地・アパート名まで）", key="app_address_input")
        col1, col2 = st.columns(2)
        app_age = col1.number_input("ご年齢", min_value=15, max_value=100, value=20)
        app_gender = col2.selectbox("性別", ["男性", "女性", "その他"])
        col3, col4 = st.columns(2)
        app_occupation = col3.selectbox("現在のご職業", ["会社員", "自営業", "学生", "主婦・主夫", "フリーター", "無職", "その他"])
        app_transport = col4.selectbox("移動手段", ["自家用車", "公共交通機関", "徒歩・自転車", "送迎あり"])
        col5, col6 = st.columns(2)
        app_license = col5.checkbox("🚗 普通免許あり")
        app_exp = col6.selectbox("🌾 作業経験", ["未経験", "少し経験あり", "経験豊富"])
        
        app_health = st.text_input("🏥 健康状態・配慮事項")
        app_message = st.text_area("💬 自己PR・メッセージ（必須）")
        st.write("")
        
        if st.button("✨ この内容で応募する", type="primary", use_container_width=True):
            now = get_japan_now()
            is_too_late = False
            if "deadline_at" in job:
                try:
                    if now >= datetime.datetime.strptime(job["deadline_at"], "%Y-%m-%d %H:%M:%S"): is_too_late = True
                except: pass
                
            if is_too_late:
                st.error("応募締め切り時間を過ぎています。")
            elif not app_message:
                st.warning("メッセージを記入してください。")
            else:
                user_history = st.session_state.user.get("history", [])
                if jid not in user_history:
                    user_history.append(jid)
                    st.session_state.user["history"] = user_history
                    db["users"][st.session_state.phone]["history"] = user_history
                    
                    if "applicants" not in job or job["applicants"] is None: job["applicants"] = {}
                    job["applicants"][st.session_state.phone] = {
                        "name": st.session_state.user.get("name", "名無し"),
                        "name_kana": app_name_kana, "address": app_address, "age": app_age, "gender": app_gender,
                        "occupation": app_occupation, "transport": app_transport, "has_license": app_license,
                        "experience": app_exp, "health": app_health, "message": app_message,
                        "applied_at": now.strftime("%Y年%m月%d日 %H:%M"),
                        "chat": [] 
                    }
                    db["jobs"][jid] = job
                    save_data(db)
                    
                    st.success("🎉 応募が完了しました！履歴からチャットが使えます。")
                    change_page("job_list")
        
    if st.button("一覧に戻る", use_container_width=True): change_page("job_list")

# ==========================================
# 4. お願い投稿画面
# ==========================================
def show_post_job():
    st.markdown('<div class="beauty-title"><div class="app-logo-img-small"></div>お願いを投稿する</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        title = st.text_input("お仕事のタイトル・困りごと")
        japan_today = get_japan_now().date()
        job_date = st.date_input("稼働日", value=japan_today)
        col1, col2 = st.columns(2)
        start_time = col1.time_input("開始時刻", value=datetime.time(9, 0))
        end_time = col2.time_input("終了時刻", value=datetime.time(12, 0))
        
        st.divider()
        col3, col4 = st.columns(2)
        deadline_date = col3.date_input("締め切り日", value=japan_today)
        deadline_time = col4.time_input("締め切り時刻", value=datetime.time(8, 0))
        
        st.divider()
        col_p1, col_p2 = st.columns([1, 2])
        pay_type = col_p1.selectbox("給与の種類", ["日給", "時給", "1回あたり", "月給"])
        pay_amount = col_p2.number_input("謝礼・給料金額（100円区切り）", min_value=0, step=100, value=1000)
        
        st.divider()
        st.markdown("#### 📍 勤務地の指定")
        col_z1, col_z2 = st.columns([2, 1])
        zip_code = col_z1.text_input("郵便番号（ハイフンなし）", placeholder="例: 0100951")
        if col_z2.button("🔍 住所を検索", use_container_width=True):
            if zip_code:
                url = f"https://zipcloud.ibsnet.co.jp/api/search?zipcode={zip_code}"
                try:
                    req = urllib.request.Request(url)
                    with urllib.request.urlopen(req) as response:
                        res_json = json.loads(response.read().decode("utf-8"))
                        if res_json["status"] == 200 and res_json["results"]:
                            result_data = res_json["results"][0]
                            searched_city = result_data["address2"]
                            searched_town = result_data["address3"]
                            
                            if searched_city in akita_cities:
                                st.session_state.post_city = searched_city
                            st.session_state.post_detail = searched_town
                            st.rerun()
                        else:
                            st.error("郵便番号が見つかりませんでした。")
                except Exception:
                    st.error("住所の検索中に通信エラーが発生しました。")

        if "post_city" not in st.session_state:
            user_city = st.session_state.user.get('city', '')
            st.session_state.post_city = user_city if user_city in akita_cities else akita_cities[0]
        if "post_detail" not in st.session_state:
            st.session_state.post_detail = ""

        city = st.selectbox("対象の市町村", akita_cities, key="post_city")
        loc_type = st.selectbox("場所のジャンル", ["個人宅", "農地・畑", "店舗", "オフィス", "公共施設", "その他"])
        loc_detail = st.text_input("詳しい場所 (例: 山王1-1)", key="post_detail")
        items = st.text_input("🎒 持ち物")
        st.write("")
        
        if st.button("事務局へ確認申請を提出する", type="primary", use_container_width=True):
            if title and loc_detail:
                pay = f"{pay_type} {pay_amount:,}円"
                full_loc = f"秋田県{city} {loc_detail}".strip()
                new_jid = str(uuid.uuid4())
                
                db["jobs"][new_jid] = {
                    "title": title, 
                    "time": f"{job_date.strftime('%Y年%m月%d日')} {start_time.strftime('%H:%M')}〜{end_time.strftime('%H:%M')}", 
                    "pay": pay, "loc": full_loc, "loc_type": loc_type, "items": items, 
                    "status": "pending", 
                    "posted_by": st.session_state.user.get("name", "名無し"),
                    "posted_by_phone": st.session_state.phone,
                    "expire_at": datetime.datetime.combine(job_date, end_time).strftime("%Y-%m-%d %H:%M:%S"),
                    "deadline_at": datetime.datetime.combine(deadline_date, deadline_time).strftime("%Y-%m-%d %H:%M:%S")
                }
                save_data(db)
                
                st.success("📨 事務局へ申請しました！")
                change_page("job_list")
            else:
                st.warning("未入力の項目があります。")
        
    if st.button("戻る", use_container_width=True): change_page("job_list")

# ==========================================
# 5. 自分の募集と応募者を見る
# ==========================================
def show_my_posts():
    st.markdown('<div class="beauty-title"><div class="app-logo-img-small"></div>あなたが募集したお仕事</div>', unsafe_allow_html=True)
    
    my_jobs = {jid: j for jid, j in db["jobs"].items() if j.get("posted_by_phone") == st.session_state.phone}
    
    if not my_jobs:
        st.info("まだ募集したお仕事はありません。")
    else:
        for jid, job in reversed(list(my_jobs.items())):
            with st.container(border=True):
                col_t, col_d = st.columns([4, 1])
                col_t.markdown(f"## 💼 {job['title']}")
                if col_d.button("🗑️ 削除", key=f"del_my_{jid}"):
                    del db["jobs"][jid]
                    save_data(db)
                    st.rerun()

                status_text = "✅ 掲載中・承認済み" if job.get("status") == "approved" else "⏳ 事務局の承認待ち"
                st.write(f"ステータス: **{status_text}**")
                
                # 募集内容を後から確認できるボタン
                with st.expander("📌 募集内容の詳細を確認する"):
                    st.markdown(f"⏰ **日時:** {job['time']}")
                    st.markdown(f"💰 **給与:** {job.get('pay', '未設定')}")
                    st.markdown(f"🎒 **持ち物:** {job.get('items', '特になし')}")
                    st.markdown(f"📍 **勤務地:** {job.get('loc', '未設定')}")
                
                st.divider()
                st.markdown("### 👥 応募してきた方の一覧")
                
                applicants = job.get("applicants", {})
                if not applicants:
                    st.write("⚪ まだ応募者はいません。")
                else:
                    for app_phone, app in applicants.items():
                        with st.container(border=True):
                            st.markdown(f"#### 👤 {app['name']} さん （{app.get('age')}歳 / {app.get('gender')}）")
                            st.write(f"📞 **連絡先:** {app_phone}")
                            st.write(f"🏠 **住所:** {app.get('address')}")
                            st.write(f"🌾 **経験:** {app.get('experience')} ｜ 🚗 **移動:** {app.get('transport')}")
                            st.info(f"💬 **メッセージ:**\n{app['message']}")
                            
                            st.markdown("---")
                            st.markdown(f"💬 **{app['name']} さんとの相談チャット**")
                            
                            chat_history = app.get("chat", [])
                            if not chat_history:
                                st.caption("まだチャットのやり取りはありません。")
                            else:
                                for msg in chat_history:
                                    if msg["sender_phone"] == st.session_state.phone:
                                        st.markdown(f'<div class="chat-bubble-me"><b>あなた</b><br>{msg["text"]}<span class="chat-time">{msg["time"]}</span></div>', unsafe_allow_html=True)
                                    else:
                                        st.markdown(f'<div class="chat-bubble-other"><b>{msg["sender_name"]}さん</b><br>{msg["text"]}<span class="chat-time">{msg["time"]}</span></div>', unsafe_allow_html=True)
                            
                            with st.form(key=f"form_chat_{jid}_{app_phone}", clear_on_submit=True):
                                text = st.text_input("メッセージを入力", placeholder="例：ご応募ありがとうございます！一度お電話可能ですか？")
                                if st.form_submit_button("✉️ メッセージを送信", type="primary"):
                                    if text.strip():
                                        if "chat" not in db["jobs"][jid]["applicants"][app_phone]:
                                            db["jobs"][jid]["applicants"][app_phone]["chat"] = []
                                        
                                        db["jobs"][jid]["applicants"][app_phone]["chat"].append({
                                            "sender_phone": st.session_state.phone,
                                            "sender_name": st.session_state.user.get("name", "募集主"),
                                            "text": text.strip(),
                                            "time": get_japan_now().strftime("%m/%d %H:%M")
                                        })
                                        save_data(db)
                                        st.rerun()
    
    st.write("")
    if st.button("一覧に戻る", type="primary", use_container_width=True):
        change_page("job_list")

# ==========================================
# 6. 応募履歴
# ==========================================
def show_history():
    st.markdown('<div class="beauty-title"><div class="app-logo-img-small"></div>あなたの応募履歴</div>', unsafe_allow_html=True)
    history_jids = st.session_state.user.get("history", [])
    
    if not history_jids:
        st.info("まだお仕事への応募履歴がありません。")
    else:
        for jid in history_jids:
            job = db["jobs"].get(jid)
            with st.container(border=True):
                if job:
                    st.success(f"✅ 応募済み: **{job['title']}**")
                    st.caption(f"投稿者: {job.get('posted_by')} さん")
                    
                    with st.expander("📌 仕事の詳細・場所を確認する"):
                        st.markdown(f"⏰ **日時:** {job['time']}")
                        st.markdown(f"💰 **給与:** {job.get('pay', '未設定')}")
                        st.markdown(f"🎒 **持ち物:** {job.get('items', '特になし')}")
                        st.markdown(f"📍 **勤務地:** {job.get('loc', '未設定')}")
                        if 'loc' in job:
                            map_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(job['loc'])}"
                            st.markdown(f"🗺️ [Googleマップで場所を開く]({map_url})")

                    st.markdown("---")
                    st.markdown("💬 **仕事の依頼主との相談チャット**")
                    
                    app_data = job.get("applicants", {}).get(st.session_state.phone, {})
                    chat_history = app_data.get("chat", [])
                    
                    if not chat_history:
                        st.caption("まだチャットのやり取りはありません。相手からの返信をお待ちください。")
                    else:
                        for msg in chat_history:
                            if msg["sender_phone"] == st.session_state.phone:
                                st.markdown(f'<div class="chat-bubble-me"><b>あなた</b><br>{msg["text"]}<span class="chat-time">{msg["time"]}</span></div>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<div class="chat-bubble-other"><b>{msg["sender_name"]}さん（依頼主）</b><br>{msg["text"]}<span class="chat-time">{msg["time"]}</span></div>', unsafe_allow_html=True)
                    
                    with st.form(key=f"form_app_chat_{jid}", clear_on_submit=True):
                        text = st.text_input("メッセージを入力", placeholder="例：当日の集合場所についてお伺いしたいです。")
                        if st.form_submit_button("✉️ メッセージを送信", type="primary"):
                            if text.strip():
                                if "chat" not in db["jobs"][jid]["applicants"][st.session_state.phone]:
                                    db["jobs"][jid]["applicants"][st.session_state.phone]["chat"] = []
                                
                                db["jobs"][jid]["applicants"][st.session_state.phone]["chat"].append({
                                    "sender_phone": st.session_state.phone,
                                    "sender_name": st.session_state.user.get("name", "応募者"),
                                    "text": text.strip(),
                                    "time": get_japan_now().strftime("%m/%d %H:%M")
                                })
                                db["jobs"][jid]["applicants"][st.session_state.phone] = db["jobs"][jid]["applicants"][st.session_state.phone]
                                save_data(db)
                                st.rerun()
                else:
                    st.warning("このお仕事は終了しました。")
            
    st.write("")
    if st.button("一覧に戻る", type="primary", use_container_width=True): change_page("job_list")

# ==========================================
# 7. 管理者画面
# ==========================================
def show_admin_dashboard():
    with st.sidebar:
        # 管理者画面サイドバーにもロゴを追加
        st.markdown(f'<div style="text-align:center; margin-bottom:10px;"><img src="{logo_html_raw}" height="60px"></div>', unsafe_allow_html=True)
        if st.button("👥 登録会員の管理", use_container_width=True): change_page("admin_users")
        if st.button("ログアウト", use_container_width=True): change_page("login")

    st.markdown('<div class="beauty-title"><div class="app-logo-img-small"></div>⚙️ 統括画面</div>', unsafe_allow_html=True)
    
    pending_jobs = {jid: j for jid, j in db["jobs"].items() if j.get("status") == "pending"}
    approved_jobs = {jid: j for jid, j in db["jobs"].items() if j.get("status") == "approved"}
    
    st.markdown(f"## 📥 承認待ち ({len(pending_jobs)}件)")
    for jid, job in pending_jobs.items():
        with st.container(border=True):
            st.write(f"**{job['title']}はい、もちろん可能です。

ご提示いただいた最新のPythonコード（クマのロゴ画像が反映されたもの）をベースに、さらに少しの変更（CSSの追加とルーティングの調整）を加えるだけで、お望みのデザイン（温かみのあるクリーム色 $\times$ 深いティールグリーンの2分割画面）を実現できます。

### 🌟 なぜこの方法で作れるの？（初心者向け解説）

アプリ開発において、**「プログラムの頭脳（Firebaseへの接続など）」**と**「画面の見た目（デザイン）」**は別の仕組みになっています。

ご提示いただいたコードは「頭脳」の部分がしっかりしています。ここに、**「CSS」という「見た目の着せ替え用の命令」**を少し追加するだけで、データベースの仕組みはそのままに、デザインだけをガラリと変えることができるのです。

---

### 🔥 実際のコード修正例

以下は、ご提示いただいたコードをベースに、`st.columns` を使って画面を2分割し、新しいCSSを追加してデザインを適用した修正コードです。

**変更点:**
1.  **CSSの追加**: 画面を2分割し、左側をクリーム色、右側をティールグリーンにする命令を追加しました。
2.  **`st.columns` の利用**: ログイン画面を、左側の「紹介エリア」と右側の「ログインフォーム」に分割しました。
3.  **ルーティングの変更**: `show_register` を削除し、新規登録フォームもログイン画面のタブの中に統合しました。

---

```python
import streamlit as st
import json
import uuid
import datetime
import os
import urllib.parse
import urllib.request
import base64

# ==========================================
# ★ データベース設定
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

# ==========================================
# ★ 画像をBase64にエンコードする関数
# ==========================================
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# ロゴ画像のパス（Streamlitを実行するディレクトリからの相対パス）
LOGO_FILE = "image_26.png"
if os.path.exists(LOGO_FILE):
    base64_logo = get_base64_of_bin_file(LOGO_FILE)
    logo_html_raw = f'data:image/png;base64,{base64_logo}'
else:
    logo_html_raw = ""
    base64_logo = ""

# ==========================================
# ★ アプリ設定（Faviconとタイトル）
# ==========================================
st.set_page_config(
    page_title="老-MEE Pro (老ミー プロ)",
    page_icon=base64_logo if base64_logo else "🌾",
    layout="wide", # 画面を広く使う
    initial_sidebar_state="collapsed"
)

# ==========================================
# ✨ デザインCSS（新しい配色と分割レイアウト）
# ==========================================
# 画像のデザインを再現するためのカスタムCSS。
# 画面全体を深いティールグリーンにし、左側にクリーム色のパネルを配置する。
# また、ログインボタンにグラデーションを適用する。
css_str = f"""
    <style>
    /* 全体設定 */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', 'メイリオ', Meiryo, sans-serif !important;
        background-color: #1D5E5A !important; /* 深いティールグリーン */
        color: #FFFFFF !important;
        margin: 0;
        padding: 0;
    }}
    
    /* 画面分割設定 */
    .st-emotion-cache-z5fcl4 {{
        width: 100%;
        padding: 0;
    }}
    [data-testid="stAppViewContainer"] > section > div {{
        padding: 0;
    }}

    p, li, .stMarkdown {{
        font-size: 1.05rem !important;
        line-height: 1.8 !important;
        letter-spacing: 0.03em !important;
    }}

    /* ロゴ・タイトル用CSS */
    .app-logo-img {{
        content: url('{logo_html_raw}');
        height: auto;
        width: 100%;
        max-width: 250px;
        display: block;
        margin: 0 auto 10px;
    }}
    .app-logo-img-small {{
        content: url('{logo_html_raw}');
        height: 60px;
        width: auto;
        display: block;
        margin: 0 auto 10px;
    }}
    
    .beauty-title {{
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin: 0 0 10px;
        color: #FFFFFF !important;
    }}
    
    .beauty-subtitle {{
        text-align: center;
        color: #FFFFFF;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 600;
    }}

    /* 左パネル（紹介エリア） */
    .intro-panel-wrapper {{
        background-color: #FDF9F1 !important; /* 温かみのあるクリーム色 */
        color: #1D5E5A !important; /* ティールグリーン */
        width: 50vw;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 40px;
        float: left;
    }}
    
    /* 紹介パネル内ロゴ用CSS */
    .intro-panel-wrapper .app-logo-img {{
        max-width: 350px;
    }}
    .intro-panel-wrapper .beauty-title {{
        color: #1D5E5A !important;
        font-size: 4rem;
    }}
    .intro-panel-wrapper .beauty-subtitle {{
        color: #1D5E5A !important;
        font-size: 1.5rem;
    }}
    
    /* ブラウザタブ風CSS */
    .browser-tab {{
        background-color: #FFFFFF;
        color: #222222;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 10px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: auto;
        margin-bottom: 40px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }}
    
    .browser-tab span {{
        font-size: 1rem;
        font-weight: 600;
    }}
    
    .browser-tab img {{
        height: 30px;
        width: auto;
        margin-right: 15px;
    }}
    
    .browser-tab .close-btn {{
        background: none;
        border: none;
        color: #757575;
        font-weight: bold;
        cursor: pointer;
    }}

    /* 右パネル（ログインエリア） */
    .login-panel-wrapper {{
        width: 50vw;
        height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 40px;
        float: right;
    }}
    
    /* ログインフォームパネルCSS */
    [data-testid="stVerticalBlockBorderedTest"] {{
        background-color: #ffffff !important;
        border: 1px solid #E0E0E0 !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
        padding: 1.8rem !important; 
        margin-bottom: 1.2rem;
    }}
    
    [data-testid="stVerticalBlockBorderedTest"] input,
    [data-testid="stVerticalBlockBorderedTest"] textarea {{
        color: #222222 !important;
    }}
    
    /* ログインボタン・グラデーション適用 */
    .stButton>button[kind="primary"] {{
        border-radius: 30px !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        padding: 0.6rem 2rem !important;
        /* ゴールドからシルバーへのグラデーション */
        background: linear-gradient(135deg, #FFD700, #C0C0C0) !important;
        border: none !important;
        color: #3E2723 !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
    }}
    
    .stButton>button[kind="primary"] p {{ color: #3E2723 !important; }}
    
    /* 入力フィールドのカスタマイズ */
    .stTextInput>div>div>input {{
        border-radius: 8px !important;
        border: 2px solid #FFE0B2 !important;
        background-color: #FFFDF9 !important;
    }}
    
    [data-testid="stVerticalBlockBorderedTest"] label {{
        color: #3E2723 !important;
        font-weight: 600;
    }}

    @media (max-width: 768px) {{
        .intro-panel-wrapper, .login-panel-wrapper {{
            width: 100vw;
            height: auto;
            float: none;
            padding: 20px;
        }}
    }}
    </style>
"""
st.markdown(css_str, unsafe_allow_html=True)

# データの初期化
db = load_data()
if "users" not in db or db["users"] is None: db["users"] = {}
if "jobs" not in db or db["jobs"] is None: db["jobs"] = {}

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
    # ------------------------------------------
    # ★ 新しいログイン・紹介画面
    # ------------------------------------------
    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        # ------------------------------------------
        # 左パネル：紹介エリア
        # ------------------------------------------
        st.markdown('<div class="intro-panel-wrapper">', unsafe_allow_html=True)
        # ブラウザタブ風デザイン
        if logo_html_raw:
            st.markdown(f'<div class="browser-tab"><img src="{logo_html_raw}" alt="老-MEEアイコン"><span>老-MEE | 仕事と暮らし、あなたのまちで。</span><button class="close-btn">X</button></div>', unsafe_allow_html=True)
        # 大きなロゴ
        st.markdown('<div class="app-logo-img"></div>', unsafe_allow_html=True)
        # タイトルとSubtitle
        st.markdown('<div class="beauty-title">老-MEE</div>', unsafe_allow_html=True)
        st.markdown('<div class="beauty-subtitle">仕事と暮らし、あなたのまちで。</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        # ------------------------------------------
        # 右パネル：ログインエリア
        # ------------------------------------------
        st.markdown('<div class="login-panel-wrapper">', unsafe_allow_html=True)
        # 小さなロゴとタイトル
        st.markdown('<div class="app-logo-img-small"></div>', unsafe_allow_html=True)
        st.markdown('<div class="beauty-title">老-MEE Pro</div>', unsafe_allow_html=True)
        st.markdown('<div class="beauty-subtitle">地域で助け合う、新しいお仕事マッチング</div>', unsafe_allow_html=True)
        
        with st.container(border=True):
            tab1, tab2 = st.tabs(["ログイン", "新規登録"])
            
            with tab1:
                phone = st.text_input("電話", key="log_phone", placeholder="例: 09012345678")
                password = st.text_input("パスワード", type="password", key="log_pass", placeholder="••••")
                st.write("")
                # primary Kind を使用してグラデーションを適用
                if st.button("プリマりログイン", type="primary", use_container_width=True):
                    user = db["users"].get(phone)
                    if user and user.get("pass") == password:
                        st.session_state.user = user
                        st.session_state.phone = phone
                        change_page("job_list")
                    else:
                        st.error("電話番号または暗証番号が違います。")
                st.markdown('<div style="text-align:center;"><a href="#" style="color:#757575; font-size:0.9rem;">パスワードを忘れた場合</a></div>', unsafe_allow_html=True)
            
            with tab2:
                name = st.text_input("お名前（姓名）", placeholder="例: 秋田 太郎")
                phone_reg = st.text_input("電話番号（ログインIDになります）", placeholder="例: 09012345678")
                password_reg = st.text_input("暗証番号 (好きな4桁の数字)", type="password", max_chars=4, placeholder="例: 1234")
                city = st.selectbox("お住まいの市町村", akita_cities)
                st.write("")
                
                if st.button("この内容で登録する", type="primary", use_container_width=True):
                    if name and phone_reg and password_reg:
                        if phone_reg in db["users"]:
                            st.error("この電話番号はすでに登録されています。")
                        else:
                            db["users"][phone_reg] = {"name": name, "pass": password_reg, "city": city, "history": []}
                            save_data(db)
                            st.success("🎉 登録完了しました！ログインしてください。")
                            # ログインタブに戻るようにしたいが、初心者向けにはここまでとする。
                            change_page("login")
                    else:
                        st.warning("すべての項目を入力してください。")
        st.markdown('</div>', unsafe_allow_html=True)

def show_register():
    # 登録画面はshow_login内で完結させる。
    pass

# ==========================================
# 2. 仕事一覧画面
# ==========================================
def show_job_list():
    with st.sidebar:
        # サイドバーにも小さなロゴ
        st.markdown(f'<div style="text-align:center; margin-bottom:10px;"><img src="{logo_html_raw}" height="60px"></div>', unsafe_allow_html=True)
        st.markdown(f"### 👤 {st.session_state.user.get('name', 'ゲスト')} さん")
        st.markdown(f"📍 拠点: **{st.session_state.user.get('city', '未設定')}**")
        st.divider()
        if st.button("➕ お願いを新規投稿", use_container_width=True): change_page("post_job")
        if st.button("📢 自分の募集・応募者を見る", use_container_width=True): change_page("my_posts")
        if st.button("📋 自分の応募履歴とチャット", use_container_width=True): change_page("history")
        st.divider()
        if st.button("ログアウト", use_container_width=True):
            st.session_state.user = None
            st.session_state.phone = None
            change_page("login")

    # タイトル部分
    st.markdown('<div class="beauty-title"><div class="app-logo-img-small"></div>募集中の求人一覧</div>', unsafe_allow_html=True)
    
    user_history = st.session_state.user.get("history", [])
    now = get_japan_now()
    available_jobs = {}
    
    for jid, j in db["jobs"].items():
        if j.get("posted_by_phone") == st.session_state.phone:
            continue
            
        if j.get("status") == "approved" and jid not in user_history:
            skip_job = False
            if "deadline_at" in j:
                try:
                    if now >= datetime.datetime.strptime(j["deadline_at"], "%Y-%m-%d %H:%M:%S"): skip_job = True
                except: pass
            if "expire_at" in j:
                try:
                    if now >= datetime.datetime.strptime(j["expire_at"], "%Y-%m-%d %H:%M:%S"): skip_job = True
                except: pass
            if skip_job: continue
            available_jobs[jid] = j
    
    if not available_jobs:
        st.info("現在募集中の求人はありません（すべて応募済み、もしくは期限切れです）。")
    else:
        for jid, job in reversed(list(available_jobs.items())):
            with st.container(border=True):
                st.markdown(f"### 💼 {job['title']}")
                
                deadline_str = "未設定"
                if "deadline_at" in job:
                    try:
                        dt = datetime.datetime.strptime(job["deadline_at"], "%Y-%m-%d %H:%M:%S")
                        deadline_str = dt.strftime("%Y/%m/%d %H:%M")
                    except: pass
                
                col_a, col_b = st.columns(2)
                col_a.markdown(f"💰 **謝礼:** <span style='color:#D84315; font-weight:bold; font-size:1.2rem;'>{job['pay']}</span>", unsafe_allow_html=True)
                col_b.markdown(f"⏳ **締切:** {deadline_str}")
                
                st.markdown(f"⏰ **日時:** {job['time']}")
                st.markdown(f"📍 **場所:** {job['loc']}")
                
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
        st.error("このお仕事は終了しました。")
        if st.button("一覧に戻る"): change_page("job_list")
        return

    st.markdown('<div class="beauty-title"><div class="app-logo-img-small"></div>募集案件の詳細</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown(f"## 💼 {job['title']}")
        st.error(f"⚠️ **応募締め切り:** {job.get('deadline_at', '未設定')}")
        st.write("")
        col_d1, col_d2 = st.columns(2)
        col_d1.markdown(f"💰 **給与:** \n### {job['pay']}")
        col_d2.markdown(f"⏰ **仕事日時:** \n{job['time']}")
        st.divider()
        st.markdown(f"🎒 **持ち物:** \n{job['items']}")
        st.markdown(f"📍 **勤務地:** \n{job['loc']}")
        map_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(job['loc'])}"
        st.markdown(f"🗺️ [Googleマップで確認（別タブ）]({map_url})")
    
    st.write("")
    st.markdown("## 📝 応募フォーム")
    
    with st.container(border=True):
        st.markdown("#### 📍 現住所の検索（自動入力）")
        col_z1, col_z2 = st.columns([2, 1])
        app_zip = col_z1.text_input("郵便番号（ハイフンなし）", placeholder="例: 0100951", key="app_zip")
        if col_z2.button("🔍 住所を検索", key="app_zip_btn", use_container_width=True):
            if app_zip:
                url = f"[https://zipcloud.ibsnet.co.jp/api/search?zipcode=](https://zipcloud.ibsnet.co.jp/api/search?zipcode=){app_zip}"
                try:
                    req = urllib.request.Request(url)
                    with urllib.request.urlopen(req) as response:
                        res_json = json.loads(response.read().decode("utf-8"))
                        if res_json["status"] == 200 and res_json["results"]:
                            data = res_json["results"][0]
                            st.session_state.app_address_input = f"{data['address1']}{data['address2']}{data['address3']}"
                            st.rerun()
                        else:
                            st.error("郵便番号が見つかりませんでした。")
                except Exception:
                    st.error("通信エラーが発生しました。")
        
        if "app_address_input" not in st.session_state:
            st.session_state.app_address_input = ""
            
        st.divider()

        col_n1, col_n2 = st.columns(2)
        app_name_kana = col_n1.text_input("氏名（ふりがな）")
        app_address = col_n2.text_input("詳しい現住所（番地・アパート名まで）", key="app_address_input")
        col1, col2 = st.columns(2)
        app_age = col1.number_input("ご年齢", min_value=15, max_value=100, value=20)
        app_gender = col2.selectbox("性別", ["男性", "女性", "その他"])
        col3, col4 = st.columns(2)
        app_occupation = col3.selectbox("現在のご職業", ["会社員", "自営業", "学生", "主婦・主夫", "フリーター", "無職", "その他"])
        app_transport = col4.selectbox("移動手段", ["自家用車", "公共交通機関", "徒歩・自転車", "送迎あり"])
        col5, col6 = st.columns(2)
        app_license = col5.checkbox("🚗 普通免許あり")
        app_exp = col6.selectbox("🌾 作業経験", ["未経験", "少し経験あり", "経験豊富"])
        
        app_health = st.text_input("🏥 健康状態・配慮事項")
        app_message = st.text_area("💬 自己PR・メッセージ（必須）")
        st.write("")
        
        if st.button("✨ この内容で応募する", type="primary", use_container_width=True):
            now = get_japan_now()
            is_too_late = False
            if "deadline_at" in job:
                try:
                    if now >= datetime.datetime.strptime(job["deadline_at"], "%Y-%m-%d %H:%M:%S"): is_too_late = True
                except: pass
                
            if is_too_late:
                st.error("応募締め切り時間を過ぎています。")
            elif not app_message:
                st.warning("メッセージを記入してください。")
            else:
                user_history = st.session_state.user.get("history", [])
                if jid not in user_history:
                    user_history.append(jid)
                    st.session_state.user["history"] = user_history
                    db["users"][st.session_state.phone]["history"] = user_history
                    
                    if "applicants" not in job or job["applicants"] is None: job["applicants"] = {}
                    job["applicants"][st.session_state.phone] = {
                        "name": st.session_state.user.get("name", "名無し"),
                        "name_kana": app_name_kana, "address": app_address, "age": app_age, "gender": app_gender,
                        "occupation": app_occupation, "transport": app_transport, "has_license": app_license,
                        "experience": app_exp, "health": app_health, "message": app_message,
                        "applied_at": now.strftime("%Y年%m月%d日 %H:%M"),
                        "chat": [] 
                    }
                    db["jobs"][jid] = job
                    save_data(db)
                    
                    st.success("🎉 応募が完了しました！履歴からチャットが使えます。")
                    change_page("job_list")
        
    if st.button("一覧に戻る", use_container_width=True): change_page("job_list")

# ==========================================
# 4. お願い投稿画面
# ==========================================
def show_post_job():
    st.markdown('<div class="beauty-title"><div class="app-logo-img-small"></div>お願いを投稿する</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        title = st.text_input("お仕事のタイトル・困りごと")
        japan_today = get_japan_now().date()
        job_date = st.date_input("稼働日", value=japan_today)
        col1, col2 = st.columns(2)
        start_time = col1.time_input("開始時刻", value=datetime.time(9, 0))
        end_time = col2.time_input("終了時刻", value=datetime.time(12, 0))
        
        st.divider()
        col3, col4 = st.columns(2)
        deadline_date = col3.date_input("締め切り日", value=japan_today)
        deadline_time = col4.time_input("締め切り時刻", value=datetime.time(8, 0))
        
        st.divider()
        col_p1, col_p2 = st.columns([1, 2])
        pay_type = col_p1.selectbox("給与の種類", ["日給", "時給", "1回あたり", "月給"])
        pay_amount = col_p2.number_input("謝礼・給料金額（100円区切り）", min_value=0, step=100, value=1000)
        
        st.divider()
        st.markdown("#### 📍 勤務地の指定")
        col_z1, col_z2 = st.columns([2, 1])
        zip_code = col_z1.text_input("郵便番号（ハイフンなし）", placeholder="例: 0100951")
        if col_z2.button("🔍 住所を検索", use_container_width=True):
            if zip_code:
                url = f"[https://zipcloud.ibsnet.co.jp/api/search?zipcode=](https://zipcloud.ibsnet.co.jp/api/search?zipcode=){zip_code}"
                try:
                    req = urllib.request.Request(url)
                    with urllib.request.urlopen(req) as response:
                        res_json = json.loads(response.read().decode("utf-8"))
                        if res_json["status"] == 200 and res_json["results"]:
                            result_data = res_json["results"][0]
                            searched_city = result_data["address2"]
                            searched_town = result_data["address3"]
                            
                            if searched_city in akita_cities:
                                st.session_state.post_city = searched_city
                            st.session_state.post_detail = searched_town
                            st.rerun()
                        else:
                            st.error("郵便番号が見つかりませんでした。")
                except Exception:
                    st.error("住所の検索中に通信エラーが発生しました。")

        if "post_city" not in st.session_state:
            user_city = st.session_state.user.get('city', '')
            st.session_state.post_city = user_city if user_city in akita_cities else akita_cities[0]
        if "post_detail" not in st.session_state:
            st.session_state.post_detail = ""

        city = st.selectbox("対象の市町村", akita_cities, key="post_city")
        loc_type = st.selectbox("場所のジャンル", ["個人宅", "農地・畑", "店舗", "オフィス", "公共施設", "その他"])
        loc_detail = st.text_input("詳しい場所 (例: 山王1-1)", key="post_detail")
        items = st.text_input("🎒 持ち物")
        st.write("")
        
        if st.button("事務局へ確認申請を提出する", type="primary", use_container_width=True):
            if title and loc_detail:
                pay = f"{pay_type} {pay_amount:,}円"
                full_loc = f"秋田県{city} {loc_detail}".strip()
                new_jid = str(uuid.uuid4())
                
                db["jobs"][new_jid] = {
                    "title": title, 
                    "time": f"{job_date.strftime('%Y年%m月%d日')} {start_time.strftime('%H:%M')}〜{end_time.strftime('%H:%M')}", 
                    "pay": pay, "loc": full_loc, "loc_type": loc_type, "items": items, 
                    "status": "pending", 
                    "posted_by": st.session_state.user.get("name", "名無し"),
                    "posted_by_phone": st.session_state.phone,
                    "expire_at": datetime.datetime.combine(job_date, end_time).strftime("%Y-%m-%d %H:%M:%S"),
                    "deadline_at": datetime.datetime.combine(deadline_date, deadline_time).strftime("%Y-%m-%d %H:%M:%S")
                }
                save_data(db)
                
                st.success("📨 事務局へ申請しました！")
                change_page("job_list")
            else:
                st.warning("未入力の項目があります。")
        
    if st.button("戻る", use_container_width=True): change_page("job_list")

# ==========================================
# 5. 自分の募集と応募者を見る
# ==========================================
def show_my_posts():
    st.markdown('<div class="beauty-title"><div class="app-logo-img-small"></div>あなたが募集したお仕事</div>', unsafe_allow_html=True)
    
    my_jobs = {jid: j for jid, j in db["jobs"].items() if j.get("posted_by_phone") == st.session_state.phone}
    
    if not my_jobs:
        st.info("まだ募集したお仕事はありません。")
    else:
        for jid, job in reversed(list(my_jobs.items())):
            with st.container(border=True):
                col_t, col_d = st.columns([4, 1])
                col_t.markdown(f"## 💼 {job['title']}")
                if col_d.button("🗑️ 削除", key=f"del_my_{jid}"):
                    del db["jobs"][jid]
                    save_data(db)
                    st.rerun()

                status_text = "✅ 掲載中・承認済み" if job.get("status") == "approved" else "⏳ 事務局の承認待ち"
                st.write(f"ステータス: **{status_text}**")
                
                with st.expander("📌 募集内容の詳細を確認する"):
                    st.markdown(f"⏰ **日時:** {job['time']}")
                    st.markdown(f"💰 **給与:** {job.get('pay', '未設定')}")
                    st.markdown(f"🎒 **持ち物:** {job.get('items', '特になし')}")
                    st.markdown(f"📍 **勤務地:** {job.get('loc', '未設定')}")
                
                st.divider()
                st.markdown("### 👥 応募してきた方の一覧")
                
                applicants = job.get("applicants", {})
                if not applicants:
                    st.write("⚪ まだ応募者はいません。")
                else:
                    for app_phone, app in applicants.items():
                        with st.container(border=True):
                            st.markdown(f"#### 👤 {app['name']} さん （{app.get('age')}歳 / {app.get('gender')}）")
                            st.write(f"📞 **連絡先:** {app_phone}")
                            st.write(f"🏠 **住所:** {app.get('address')}")
                            st.write(f"🌾 **経験:** {app.get('experience')} ｜ 🚗 **移動:** {app.get('transport')}")
                            st.info(f"💬 **メッセージ:**\n{app['message']}")
                            
                            st.markdown("---")
                            st.markdown(f"💬 **{app['name']} さんとの相談チャット**")
                            
                            chat_history = app.get("chat", [])
                            if not chat_history:
                                st.caption("まだチャットのやり取りはありません。")
                            else:
                                for msg in chat_history:
                                    if msg["sender_phone"] == st.session_state.phone:
                                        st.markdown(f'<div class="chat-bubble-me"><b>あなた</b><br>{msg["text"]}<span class="chat-time">{msg["time"]}</span></div>', unsafe_allow_html=True)
                                    else:
                                        st.markdown(f'<div class="chat-bubble-other"><b>{msg["sender_name"]}さん</b><br>{msg["text"]}<span class="chat-time">{msg["time"]}</span></div>', unsafe_allow_html=True)
                            
                            with st.form(key=f"form_chat_{jid}_{app_phone}", clear_on_submit=True):
                                text = st.text_input("メッセージを入力", placeholder="例：ご応募ありがとうございます！一度お電話可能ですか？")
                                if st.form_submit_button("✉️ メッセージを送信", type="primary"):
                                    if text.strip():
                                        if "chat" not in db["jobs"][jid]["applicants"][app_phone]:
                                            db["jobs"][jid]["applicants"][app_phone]["chat"] = []
                                        
                                        db["jobs"][jid]["applicants"][app_phone]["chat"].append({
                                            "sender_phone": st.session_state.phone,
                                            "sender_name": st.session_state.user.get("name", "募集主"),
                                            "text": text.strip(),
                                            "time": get_japan_now().strftime("%m/%d %H:%M")
                                        })
                                        save_data(db)
                                        st.rerun()
    
    st.write("")
    if st.button("一覧に戻る", type="primary", use_container_width=True):
        change_page("job_list")

# ==========================================
# 6. 応募履歴
# ==========================================
def show_history():
    st.markdown('<div class="beauty-title"><div class="app-logo-img-small"></div>あなたの応募履歴</div>', unsafe_allow_html=True)
    history_jids = st.session_state.user.get("history", [])
    
    if not history_jids:
        st.info("まだお仕事への応募履歴がありません。")
    else:
        for jid in history_jids:
            job = db["jobs"].get(jid)
            with st.container(border=True):
                if job:
                    st.success(f"✅ 応募済み: **{job['title']}**")
                    st.caption(f"投稿者: {job.get('posted_by')} さん")
                    
                    with st.expander("📌 仕事の詳細・場所を確認する"):
                        st.markdown(f"⏰ **日時:** {job['time']}")
                        st.markdown(f"💰 **給与:** {job.get('pay', '未設定')}")
                        st.markdown(f"🎒 **持ち物:** {job.get('items', '特になし')}")
                        st.markdown(f"📍 **勤務地:** {job.get('loc', '未設定')}")
                        if 'loc' in job:
                            map_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(job['loc'])}"
                            st.markdown(f"🗺️ [Googleマップで場所を開く]({map_url})")

                    st.markdown("---")
                    st.markdown("💬 **仕事の依頼主との相談チャット**")
                    
                    app_data = job.get("applicants", {}).get(st.session_state.phone, {})
                    chat_history = app_data.get("chat", [])
                    
                    if not chat_history:
                        st.caption("まだチャットのやり取りはありません。相手からの返信をお待ちください。")
                    else:
                        for msg in chat_history:
                            if msg["sender_phone"] == st.session_state.phone:
                                st.markdown(f'<div class="chat-bubble-me"><b>あなた</b><br>{msg["text"]}<span class="chat-time">{msg["time"]}</span></div>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<div class="chat-bubble-other"><b>{msg["sender_name"]}さん（依頼主）</b><br>{msg["text"]}<span class="chat-time">{msg["time"]}</span></div>', unsafe_allow_html=True)
                    
                    with st.form(key=f"form_app_chat_{jid}", clear_on_submit=True):
                        text = st.text_input("メッセージを入力", placeholder="例：当日の集合場所についてお伺いしたいです。")
                        if st.form_submit_button("✉️ メッセージを送信", type="primary"):
                            if text.strip():
                                if "chat" not in db["jobs"][jid]["applicants"][st.session_state.phone]:
                                    db["jobs"][jid]["applicants"][st.session_state.phone]["chat"] = []
                                
                                db["jobs"][jid]["applicants"][st.session_state.phone]["chat"].append({
                                    "sender_phone": st.session_state.phone,
                                    "sender_name": st.session_state.user.get("name", "応募者"),
                                    "text": text.strip(),
                                    "time": get_japan_now().strftime("%m/%d %H:%M")
                                })
                                db["jobs"][jid]["applicants"][st.session_state.phone] = db["jobs"][jid]["applicants"][st.session_state.phone]
                                save_data(db)
                                st.rerun()
                else:
                    st.warning("このお仕事は終了しました。")
            
    st.write("")
    if st.button("一覧に戻る", type="primary", use_container_width=True): change_page("job_list")

# ==========================================
# 7. 管理者画面
# ==========================================
def show_admin_dashboard():
    with st.sidebar:
        if logo_html_raw:
            st.markdown(f'<div style="text-align:center; margin-bottom:10px;"><img src="{logo_html_raw}" height="60px"></div>', unsafe_allow_html=True)
        if st.button("👥 登録会員の管理", use_container_width=True): change_page("admin_users")
        if st.button("ログアウト", use_container_width=True): change_page("login")

    st.markdown('<div class="beauty-title"><div class="app-logo-img-small"></div>⚙️ 統括画面</div>', unsafe_allow_html=True)
    
    pending_jobs = {jid: j for jid, j in db["jobs"].items() if j.get("status") == "pending"}
    approved_jobs = {jid: j for jid, j in db["jobs"].items() if j.get("status") == "approved"}
    
    st.markdown(f"## 📥 承認待ち ({len(pending_jobs)}件)")
    for jid, job in pending_jobs.items():
        with st.container(border=True):
            st.write(f"**{job['title']}** (投稿者: {job.get('posted_by')}さん)")
            col1, col2 = st.columns(2)
            if col1.button("✅ 許可", key=f"app_{jid}", type="primary", use_container_width=True):
                db["jobs"][jid]["status"] = "approved"
                save_data(db)
                st.rerun()
            if col2.button("🗑 却下", key=f"del_{jid}", use_container_width=True):
                del db["jobs"][jid]
                save_data(db)
                st.rerun()

    st.markdown(f"## 🟢 掲載中 ({len(approved_jobs)}件)")
    for jid, job in approved_jobs.items():
        with st.container(border=True):
            st.write(f"**{job['title']}**")
            
            applicants = job.get("applicants", {})
            if applicants:
                st.markdown("#### 👥 応募者")
                for app_phone, app in applicants.items():
                    st.write(f"👤 {app['name']} さん (📞 {app_phone})")
            
            st.write("")
            if st.button("🗑️ 掲載終了・削除", key=f"del_pub_{jid}"):
                del db["jobs"][jid]
                save_data(db)
                st.rerun()

def show_admin_users():
    if st.button("戻る"): change_page("admin_dashboard")
    st.markdown("## 👥 登録ユーザー")
    for phone, u in db["users"].items():
        with st.container(border=True):
            st.write(f"**{u.get('name')}** (📞 {phone})")
            if st.button("🗑️ 削除", key=f"del_user_{phone}"):
                del db["users"][phone]
                save_data(db)
                st.rerun()

# ==========================================
# ★ 画面の振り分け（ルーティング）
# ==========================================
if st.session_state.page == "login": show_login()
elif st.session_state.page == "job_list": show_job_list()
elif st.session_state.page == "job_detail": show_job_detail()
elif st.session_state.page == "post_job": show_post_job()
elif st.session_state.page == "my_posts": show_my_posts()
elif st.session_state.page == "history": show_history()
elif st.session_state.page == "admin_dashboard": show_admin_dashboard()
elif st.session_state.page == "admin_users": show_admin_users()
