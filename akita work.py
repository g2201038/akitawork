import streamlit as st
import requests
import json

# ==========================================
# 設定：FirebaseのURLをここに貼り付けてください
# 例: "https://project-id-default-rtdb.firebaseio.com/"
# ==========================================
FIREBASE_URL = "https://YOUR-PROJECT-ID.firebaseio.com/"

# --- データ同期関数 ---
def load_data(path):
    try:
        res = requests.get(f"{FIREBASE_URL}{path}.json")
        data = res.json()
        if data is None:
            return [] if path == "jobs" else {}
        return data
    except:
        return [] if path == "jobs" else {}

def save_data(path, data):
    requests.put(f"{FIREBASE_URL}{path}.json", json.dumps(data))

# --- アプリの基本設定 ---
st.set_page_config(page_title="あきたワーク Web", page_icon="🌾")

# ログイン状態の管理
if "user" not in st.session_state:
    st.session_state.user = None

# --- 画面切り替えロジック ---
if not st.session_state.user:
    st.title("🌾 あきたワーク")
    st.subheader("ログイン または 新規登録")
    
    tab1, tab2 = st.tabs(["ログイン", "新規登録"])
    
    with tab1:
        phone = st.text_input("電話番号（ログイン用）")
        password = st.text_input("暗証番号", type="password", key="login_pw")
        if st.button("ログイン"):
            users = load_data("users")
            if phone in users and users[phone]["pass"] == password:
                st.session_state.user = users[phone]
                st.session_state.phone = phone
                st.success("ログイン成功！")
                st.rerun()
            else:
                st.error("電話番号かパスワードが違います")

    with tab2:
        new_name = st.text_input("お名前")
        new_phone = st.text_input("電話番号（登録用）")
        new_pw = st.text_input("暗証番号(4桁)", type="password", key="reg_pw")
        city = st.selectbox("お住まいの市町村", ["秋田市", "能代市", "横手市", "大仙市", "その他"])
        if st.button("登録する"):
            if new_name and new_phone and new_pw:
                users = load_data("users")
                users[new_phone] = {"name": new_name, "pass": new_pw, "city": city, "history": []}
                save_data("users", users)
                st.success("登録完了！ログインしてください")
            else:
                st.warning("すべての項目を入力してください")

else:
    # ログイン後のメイン画面
    st.sidebar.title(f"👤 {st.session_state.user['name']}さん")
    menu = st.sidebar.radio("メニュー", ["お仕事を探す", "お願いを投稿する", "管理者メニュー", "ログアウト"])

    if menu == "お仕事を探す":
        st.header("📍 募集中の仕事")
        jobs = load_data("jobs")
        # リスト形式への変換
        job_list = jobs if isinstance(jobs, list) else (list(jobs.values()) if jobs else [])
        
        approved_jobs = [j for j in job_list if j.get("status") == "approved"]
        
        if not approved_jobs:
            st.info("現在、募集中の仕事はありません。")
        else:
            for job in reversed(approved_jobs):
                with st.container():
                    st.markdown(f"### {job['title']}")
                    st.write(f"💰 謝礼: {job['pay']} / 📍 場所: {job['loc']}")
                    if st.button("応募する", key=f"apply_{job['id']}"):
                        st.balloons()
                        st.success(f"「{job['title']}」に応募しました！")

    elif menu == "お願いを投稿する":
        st.header("➕ お願いを投稿する")
        title = st.text_input("依頼内容 (例: 雪かき、買い物)")
        pay = st.text_input("謝礼 (例: 1500円)")
        loc = st.selectbox("場所", ["秋田市", "能代市", "横手市", "大仙市", "その他"])
        
        if st.button("投稿（管理者の承認待ちへ）"):
            if title and pay:
                jobs = load_data("jobs")
                job_list = jobs if isinstance(jobs, list) else (list(jobs.values()) if jobs else [])
                new_id = len(job_list) + 1
                new_job = {
                    "id": new_id, "title": title, "pay": pay, "loc": loc,
                    "status": "pending", "posted_by": st.session_state.user["name"]
                }
                if isinstance(jobs, list): jobs.append(new_job)
                else: jobs[str(new_id)] = new_job
                save_data("jobs", jobs)
                st.success("申請を送りました！管理者が承認すると一覧に載ります。")

    elif menu == "管理者メニュー":
        st.header("🏢 管理者専用")
        admin_pw = st.text_input("管理者パスワード", type="password")
        if admin_pw == "9999":
            jobs = load_data("jobs")
            job_dict = jobs if isinstance(jobs, dict) else {str(i): v for i, v in enumerate(jobs)}
            
            pending_found = False
            for k, j in job_dict.items():
                if j.get("status") == "pending":
                    pending_found = True
                    st.write(f"【未承認】 {j['title']} (依頼者: {j['posted_by']})")
                    if st.button("承認する", key=f"adm_{k}"):
                        job_dict[k]["status"] = "approved"
                        save_data("jobs", job_dict)
                        st.rerun()
            if not pending_found:
                st.write("現在、承認待ちの依頼はありません。")

    elif menu == "ログアウト":
        st.session_state.user = None
        st.rerun()
