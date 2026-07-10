def show_job_list():
    # ==========================================
    # 1. サイドバー（自分の情報と評価）
    # ==========================================
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.user.get('name', 'ゲスト')} さん")
        
        my_rating = st.session_state.user.get("rating", 0.0)
        my_reviews_count = st.session_state.user.get("reviews_count", 0)
        
        if my_reviews_count > 0:
            my_stars = "★" * int(my_rating) + "☆" * (5 - int(my_rating))
            st.markdown(f"<span style='color:#FF9900; font-size:1.1rem;'>{my_stars}</span> **{my_rating:.1f}** <span style='color:gray; font-size:0.9rem;'>({my_reviews_count}件)</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color:gray; font-size:0.9rem;'>評価: まだありません</span>", unsafe_allow_html=True)

        st.markdown(f"📍 拠点: **{st.session_state.user.get('city', '未設定')}**")

    # ==========================================
    # 2. メイン画面（求人一覧の表示）
    # ==========================================
    st.header("📋 募集中の仕事一覧")

    # ⚠️ 注意: ここで available_jobs を取得する処理が元のコードにあるはずです。
    # 例: available_jobs = get_available_jobs() や、データの読み込み処理など
    # もし消してしまっていたら、元の取得処理をここに残してください。

    # エラーが起きていた箇所（インデント修正済み）
    if not available_jobs:
        st.info("現在募集中の求人はありません（すべて応募済み、もしくは期限切れです）。")
    else:
        for jid, job in reversed(list(available_jobs.items())):
            with st.container(border=True):
                st.markdown(f"### 💼 {job.get('title', 'タイトル未設定')}")
                
                # 依頼者の名前と口コミ評価を表示
                poster_name = job.get("posted_by", "名無し")
                poster_rating = job.get("poster_rating", 0.0)
                poster_reviews_count = job.get("poster_reviews_count", 0)
                
                if poster_reviews_count > 0:
                    stars = "★" * int(poster_rating) + "☆" * (5 - int(poster_rating))
                    st.markdown(f"👤 **{poster_name}** さんの評価: <span style='color:#FF9900;'>{stars}</span> **{poster_rating:.1f}** <span style='font-size:0.8rem; color:gray;'>({poster_reviews_count}件)</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"👤 **{poster_name}** さんの評価: <span style='color:gray; font-size:0.9rem;'>まだ評価はありません</span>", unsafe_allow_html=True)
                
                st.write("") # 少し余白を空ける

                # 期限などの表示（元のコードの続き）
                deadline_str = job.get("deadline", "未設定")
                st.write(f"📅 **期限:** {deadline_str}")
                
                # ※この下に「詳細を見る」ボタンなど、元のコードの続きが入ります
                # ...
