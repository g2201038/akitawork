# ==========================================
# 2. 仕事一覧画面
# ==========================================
def show_job_list():
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user.get('name', 'ゲスト')} さん")
        st.markdown(f"📍 拠点: **{st.session_state.user.get('city', '未設定')}**")
        st.divider()
        if st.button("➕ お願いを新規投稿", use_container_width=True): change_page("post_job")
        if st.button("📢 自分の募集・応募者を見る", use_container_width=True): change_page("my_posts")
        if st.button("📋 自分の応募履歴", use_container_width=True): change_page("history")
        st.divider()
        if st.button("ログアウト", use_container_width=True):
            st.session_state.user = None
            st.session_state.phone = None
            change_page("login")

    st.markdown('<div class="beauty-title">🌾 募集中の求人一覧</div>', unsafe_allow_html=True)
    
    user_history = st.session_state.user.get("history", [])
    now = get_japan_now()
    available_jobs = {}
    
    for jid, j in db["jobs"].items():
        # 💡 【追加】自分が投稿した仕事は、一覧画面には表示しない（スキップする）
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
