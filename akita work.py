import tkinter as tk

from tkinter import messagebox, ttk

import json

import os

import webbrowser

import datetime
 
# 情報を保存するファイル

DB_FILE = "akita_users_pro_v8.json"

JOBS_FILE = "akita_jobs_v1.json"
 
class AkitaJobApp:

    def __init__(self, root):

        self.root = root

        self.root.title("あきたワーク Pro - 令和8年最新版")

        self.root.geometry("500x820")

        self.root.configure(bg="#F0F2F5")
 
        self.akita_cities = [

            "秋田市", "能代市", "横手市", "大館市", "男鹿市", "湯沢市", "鹿角市", 

            "由利本荘市", "潟上市", "大仙市", "北秋田市", "にかほ市", "仙北市",

            "小坂町", "上小阿仁村", "藤里町", "三種町", "八峰町", "五城目町", 

            "八郎潟町", "井川町", "大潟村", "美郷町", "羽後町", "東成瀬村"

        ]
 
        # 詳しい場所の選択肢データ

        self.area_dict = {

            "秋田市": ["中通", "山王", "保戸野", "泉", "牛島", "新屋", "土崎", "茨島", "広面", "その他"],

            "大仙市": ["大曲", "神岡", "西仙北", "中仙", "協和", "南外", "仙北", "太田", "その他"],

            "横手市": ["横手", "増田", "平鹿", "雄物川", "大森", "十文字", "山内", "大雄", "その他"],

            "由利本荘市": ["本荘", "矢島", "岩城", "由利", "西目", "鳥海", "東由利", "大内", "その他"],

            "能代市": ["中心部", "二ツ井", "その他"]

        }
 
        # 時間の選択肢

        self.time_options = []

        for h in range(7, 19):

            self.time_options.append(f"{h:02d}:00")

            self.time_options.append(f"{h:02d}:30")
 
        # データベース読み込み

        self.users_db = self.load_user_db()

        self.job_data = self.load_jobs_db()

        self.current_user = None

        self.current_phone = None

        self.show_login_screen()
 
    # --- データの保存・読み込み ---

    def load_user_db(self):

        if os.path.exists(DB_FILE):

            with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)

        return {}
 
    def save_user_db(self):

        with open(DB_FILE, "w", encoding="utf-8") as f:

            json.dump(self.users_db, f, ensure_ascii=False, indent=4)
 
    def load_jobs_db(self):

        if os.path.exists(JOBS_FILE):

            with open(JOBS_FILE, "r", encoding="utf-8") as f: return json.load(f)

        return []
 
    def save_jobs_db(self):

        with open(JOBS_FILE, "w", encoding="utf-8") as f:

            json.dump(self.job_data, f, ensure_ascii=False, indent=4)
 
    def clear_screen(self):

        for widget in self.root.winfo_children(): widget.destroy()
 
    def open_map(self, query):

        url = f"https://www.google.com/maps/search/?api=1&query={query}"

        webbrowser.open(url)
 
    # ------------------------------------------

    # 1. ログイン関連

    # ------------------------------------------

    def show_login_screen(self):

        self.clear_screen()

        tk.Label(self.root, text="🌾 あきたワーク", font=("MS ゴシック", 28, "bold"), bg="#F0F2F5", fg="#d35400", pady=40).pack()

        frame = tk.Frame(self.root, bg="white", padx=30, pady=30, bd=1, relief="flat")

        frame.pack(padx=40, fill="x")
 
        tk.Label(frame, text="電話番号", bg="white", font=("MS ゴシック", 10)).pack(anchor="w")

        e_phone = tk.Entry(frame, font=("MS ゴシック", 16), bd=1, relief="solid")

        e_phone.pack(fill="x", pady=5)
 
        tk.Label(frame, text="暗証番号(4桁)", bg="white", font=("MS ゴシック", 10)).pack(anchor="w", pady=(10,0))

        e_pass = tk.Entry(frame, font=("MS ゴシック", 16), bd=1, relief="solid", show="●")

        e_pass.pack(fill="x", pady=5)
 
        tk.Button(self.root, text="ログイン", bg="#d35400", fg="white", font=("MS ゴシック", 16, "bold"),

                  pady=10, command=lambda: self.attempt_user_login(e_phone.get(), e_pass.get())).pack(pady=20, padx=40, fill="x")

        tk.Button(self.root, text="初めての方（新規登録）", command=self.show_registration).pack(pady=10)
 
        tk.Frame(self.root, bg="#bdc3c7", height=1).pack(fill="x", padx=40, pady=20)

        tk.Button(self.root, text="🏢 企業・管理者の方はこちら", bg="#34495e", fg="white", font=("MS ゴシック", 12),

                  pady=8, command=self.show_admin_login_screen).pack(padx=40, fill="x")
 
    def show_admin_login_screen(self):

        self.clear_screen()

        tk.Label(self.root, text="🏢 管理者ログイン", font=("MS ゴシック", 24, "bold"), bg="#F0F2F5", fg="#2c3e50", pady=40).pack()

        frame = tk.Frame(self.root, bg="white", padx=30, pady=30, bd=1, relief="flat")

        frame.pack(padx=40, fill="x")
 
        tk.Label(frame, text="管理者ID", bg="white", font=("MS ゴシック", 10)).pack(anchor="w")

        e_id = tk.Entry(frame, font=("MS ゴシック", 16), bd=1, relief="solid")

        e_id.pack(fill="x", pady=5)
 
        tk.Label(frame, text="パスワード", bg="white", font=("MS ゴシック", 10)).pack(anchor="w", pady=(10,0))

        e_pass = tk.Entry(frame, font=("MS ゴシック", 16), bd=1, relief="solid", show="●")

        e_pass.pack(fill="x", pady=5)
 
        tk.Button(self.root, text="ログイン", bg="#2c3e50", fg="white", font=("MS ゴシック", 16, "bold"),

                  pady=10, command=lambda: self.attempt_admin_login(e_id.get(), e_pass.get())).pack(pady=20, padx=40, fill="x")

        tk.Button(self.root, text="一般のログイン画面に戻る", command=self.show_login_screen).pack()
 
    def attempt_user_login(self, phone, password):

        user = self.users_db.get(phone)

        if user and user["pass"] == password:

            self.current_user = user

            self.current_phone = phone

            self.show_job_list()

        else: 

            messagebox.showerror("エラー", "番号かパスワードが違います")
 
    def attempt_admin_login(self, admin_id, password):

        if admin_id == "9999" and password == "9999":

            self.show_admin_screen()

        else:

            messagebox.showerror("エラー", "管理者IDかパスワードが違います")
 
    def show_registration(self):

        self.clear_screen()

        tk.Label(self.root, text="📝 新規登録", font=("MS ゴシック", 22, "bold"), bg="#F0F2F5", pady=30).pack()

        frame = tk.Frame(self.root, bg="white", padx=20, pady=20)

        frame.pack(padx=30, fill="both")
 
        fields = [("お名前", "name"), ("電話番号", "phone"), ("暗証番号(4桁)", "pass")]

        entries = {}

        for label, key in fields:

            tk.Label(frame, text=label, bg="white").pack(anchor="w")

            e = tk.Entry(frame, font=("MS ゴシック", 14)); e.pack(fill="x", pady=5)

            entries[key] = e
 
        tk.Label(frame, text="お住まいの市町村", bg="white").pack(anchor="w", pady=(10,0))

        combo_city = ttk.Combobox(frame, values=self.akita_cities, font=("MS ゴシック", 12), state="readonly")

        combo_city.set("選択してください")

        combo_city.pack(fill="x", pady=5)
 
        def do_register():

            p = entries["phone"].get()

            if not p or combo_city.get() == "選択してください":

                messagebox.showwarning("エラー", "全て入力してください")

                return

            self.users_db[p] = {

                "name": entries["name"].get(), "pass": entries["pass"].get(),

                "city": combo_city.get(), "history": []

            }

            self.save_user_db()

            messagebox.showinfo("完了", "登録しました")

            self.show_login_screen()
 
        tk.Button(frame, text="登録を完了する", bg="#27ae60", fg="white", font=("MS ゴシック", 14, "bold"),

                  pady=10, command=do_register).pack(fill="x", pady=20)

        tk.Button(self.root, text="戻る", command=self.show_login_screen).pack(pady=10)
 
 
    # ------------------------------------------

    # 2. シニア（ユーザー）側：仕事の投稿画面

    # ------------------------------------------

    def show_user_post_screen(self):

        self.clear_screen()

        tk.Label(self.root, text="➕ お願い・募集を投稿する", font=("MS ゴシック", 16, "bold"), bg="#F0F2F5", fg="#d35400", pady=10).pack()
 
        frame = tk.Frame(self.root, bg="white", padx=20, pady=5)

        frame.pack(padx=20, fill="both", expand=True)

        entries = {}
 
        tk.Label(frame, text="困りごと・仕事の内容 (例: 庭の草むしり)", bg="white", font=("MS ゴシック", 10, "bold")).pack(anchor="w", pady=(3,0))

        entries["title"] = tk.Entry(frame, font=("MS ゴシック", 12), bd=1, relief="solid")

        entries["title"].pack(fill="x", pady=2)
 
        tk.Label(frame, text="希望する日にち", bg="white", font=("MS ゴシック", 10, "bold")).pack(anchor="w", pady=(8,0))

        date_frame = tk.Frame(frame, bg="white")

        date_frame.pack(fill="x", pady=2)

        now = datetime.datetime.now()

        combo_month = ttk.Combobox(date_frame, values=[str(i) for i in range(1, 13)], font=("MS ゴシック", 12), width=4, state="readonly")

        combo_month.set(str(now.month))

        combo_month.pack(side="left")

        tk.Label(date_frame, text="月", bg="white", font=("MS ゴシック", 12)).pack(side="left", padx=(0, 10))

        combo_day = ttk.Combobox(date_frame, values=[str(i) for i in range(1, 32)], font=("MS ゴシック", 12), width=4, state="readonly")

        combo_day.set(str(now.day))

        combo_day.pack(side="left")

        tk.Label(date_frame, text="日", bg="white", font=("MS ゴシック", 12)).pack(side="left")
 
        tk.Label(frame, text="希望する時間", bg="white", font=("MS ゴシック", 10, "bold")).pack(anchor="w", pady=(8,0))

        time_frame = tk.Frame(frame, bg="white")

        time_frame.pack(fill="x", pady=2)

        combo_start = ttk.Combobox(time_frame, values=self.time_options, font=("MS ゴシック", 12), width=6, state="readonly")

        combo_start.set("09:00")

        combo_start.pack(side="left")

        tk.Label(time_frame, text=" 〜 ", bg="white", font=("MS ゴシック", 12)).pack(side="left")

        combo_end = ttk.Combobox(time_frame, values=self.time_options, font=("MS ゴシック", 12), width=6, state="readonly")

        combo_end.set("12:00")

        combo_end.pack(side="left")
 
        tk.Label(frame, text="お礼・給与 (例: 2,000円 または お茶菓子)", bg="white", font=("MS ゴシック", 10, "bold")).pack(anchor="w", pady=(8,0))

        entries["pay"] = tk.Entry(frame, font=("MS ゴシック", 12), bd=1, relief="solid")

        entries["pay"].pack(fill="x", pady=2)
 
        tk.Label(frame, text="集まる場所（市町村）", bg="white", font=("MS ゴシック", 10, "bold")).pack(anchor="w", pady=(8,0))

        combo_city = ttk.Combobox(frame, values=self.akita_cities, font=("MS ゴシック", 12), state="readonly")

        combo_city.set(self.current_user["city"])

        combo_city.pack(fill="x", pady=2)
 
        tk.Label(frame, text="詳しい場所・町名 (選択 または 直接入力可能)", bg="white", font=("MS ゴシック", 10, "bold")).pack(anchor="w", pady=(8,0))

        combo_loc_detail = ttk.Combobox(frame, font=("MS ゴシック", 12), state="normal")

        combo_loc_detail.pack(fill="x", pady=2)
 
        def update_areas(event=None):

            city = combo_city.get()

            if city in self.area_dict:

                combo_loc_detail.configure(values=self.area_dict[city])

                combo_loc_detail.set(self.area_dict[city][0])

            else:

                default_areas = ["中心部", "北部", "南部", "東部", "西部", "その他"]

                combo_loc_detail.configure(values=default_areas)

                combo_loc_detail.set(default_areas[0])
 
        combo_city.bind("<<ComboboxSelected>>", update_areas)

        update_areas()
 
        tk.Label(frame, text="持ち物や注意点 (例: 軍手持参)", bg="white", font=("MS ゴシック", 10, "bold")).pack(anchor="w", pady=(8,0))

        entries["items"] = tk.Entry(frame, font=("MS ゴシック", 12), bd=1, relief="solid")

        entries["items"].pack(fill="x", pady=2)
 
        def submit_user_job():

            if not entries["title"].get():

                messagebox.showwarning("エラー", "困りごとの内容は必ず入力してください")

                return
 
            datetime_str = f"{combo_month.get()}月{combo_day.get()}日 {combo_start.get()}〜{combo_end.get()}"

            full_loc = combo_city.get()

            if combo_loc_detail.get() and combo_loc_detail.get() != "その他":

                full_loc += " " + combo_loc_detail.get()
 
            # IDを付与して保存

            # ※将来的に削除機能で正しく識別するためにIDを使います

            max_id = max([j.get("id", 0) for j in self.job_data]) if self.job_data else 0
 
            new_job = {

                "id": max_id + 1,

                "title": entries["title"].get(),

                "time": datetime_str,

                "pay": entries["pay"].get(),

                "loc": full_loc,

                "map": full_loc,

                "items": entries["items"].get(),

                "status": "pending",

                "posted_by": self.current_user["name"]

            }
 
            self.job_data.append(new_job)

            self.save_jobs_db()

            messagebox.showinfo("投稿完了", "管理者に募集を申請しました！\n確認・許可されると一覧に表示されます。")

            self.show_job_list()
 
        tk.Button(self.root, text="確認申請を送る", bg="#e67e22", fg="white", font=("MS ゴシック", 14, "bold"),

                  pady=10, command=submit_user_job).pack(fill="x", padx=20, pady=10)

        tk.Button(self.root, text="やめる（戻る）", command=self.show_job_list).pack(pady=5)
 
 
    # ------------------------------------------

    # 3. 管理者側：管理＆承認画面 ★削除機能追加★

    # ------------------------------------------

    def show_admin_screen(self):

        self.clear_screen()

        header = tk.Frame(self.root, bg="#2c3e50", pady=10)

        header.pack(fill="x")

        tk.Label(header, text="🏢 管理者専用メニュー", fg="white", bg="#2c3e50", font=("MS ゴシック", 14, "bold")).pack(side="left", padx=15)

        tk.Button(header, text="ログアウト", bg="#7f8c8d", fg="white", command=self.show_login_screen).pack(side="right", padx=15)
 
        pending_jobs = [j for j in self.job_data if j.get("status") == "pending"]

        approved_jobs = [j for j in self.job_data if j.get("status") == "approved"]
 
        canvas = tk.Canvas(self.root, bg="#F0F2F5", highlightthickness=0)

        scroll_frame = tk.Frame(canvas, bg="#F0F2F5")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=480)

        canvas.pack(side="left", fill="both", expand=True)
 
        # ====== ① 承認待ちリスト ======

        tk.Label(scroll_frame, text=f"📥 シニアからの承認待ち（{len(pending_jobs)}件）", 

                 font=("MS ゴシック", 14, "bold"), bg="#F0F2F5", fg="#d35400", pady=10).pack(anchor="w", padx=15)

        if not pending_jobs:

            tk.Label(scroll_frame, text="現在、承認を待っている募集はありません。", bg="#F0F2F5", fg="gray", font=("MS ゴシック", 11)).pack(pady=10)

        else:

            for job in pending_jobs:

                card = tk.Frame(scroll_frame, bg="#fef9e7", padx=15, pady=10, bd=1, relief="solid")

                card.pack(fill="x", padx=15, pady=5)

                tk.Label(card, text=f"投稿者: {job.get('posted_by', '不明')}さん", font=("MS ゴシック", 10, "italic"), bg="#fef9e7", fg="#7f8c8d").pack(anchor="w")

                tk.Label(card, text=job["title"], font=("MS ゴシック", 12, "bold"), bg="#fef9e7").pack(anchor="w")

                tk.Label(card, text=f"日時: {job['time']}", font=("MS ゴシック", 10), bg="#fef9e7").pack(anchor="w")

                tk.Label(card, text=f"場所: {job['loc']} / 謝礼: {job['pay']}", font=("MS ゴシック", 10), bg="#fef9e7").pack(anchor="w")

                # ボタン配置用のフレーム

                btn_frame = tk.Frame(card, bg="#fef9e7")

                btn_frame.pack(fill="x", pady=(5,0))
 
                def make_approve_cmd(target_job=job):

                    return lambda: self.approve_job(target_job)

                def make_delete_cmd(target_job=job):

                    return lambda: self.delete_job(target_job)

                tk.Button(btn_frame, text="✅ 許可する", bg="#27ae60", fg="white", font=("MS ゴシック", 10, "bold"),

                          command=make_approve_cmd()).pack(side="right", padx=2)

                tk.Button(btn_frame, text="🗑 削除", bg="#e74c3c", fg="white", font=("MS ゴシック", 10, "bold"),

                          command=make_delete_cmd()).pack(side="right", padx=2)
 
 
        # ====== ② 掲載中の仕事リスト ======

        tk.Label(scroll_frame, text=f"🟢 現在掲載中の仕事（{len(approved_jobs)}件）", 

                 font=("MS ゴシック", 14, "bold"), bg="#F0F2F5", fg="#27ae60", pady=15).pack(anchor="w", padx=15)

        if not approved_jobs:

            tk.Label(scroll_frame, text="掲載中の仕事はありません。", bg="#F0F2F5", fg="gray", font=("MS ゴシック", 11)).pack(pady=10)

        else:

            for job in approved_jobs:

                card = tk.Frame(scroll_frame, bg="white", padx=15, pady=10)

                card.pack(fill="x", padx=15, pady=5)

                tk.Label(card, text=job["title"], font=("MS ゴシック", 12, "bold"), bg="white").pack(anchor="w")

                tk.Label(card, text=f"場所: {job['loc']} (掲載中)", font=("MS ゴシック", 10), bg="white", fg="gray").pack(anchor="w")
 
                def make_delete_cmd(target_job=job):

                    return lambda: self.delete_job(target_job)

                # 掲載中の仕事にも削除ボタンを追加

                tk.Button(card, text="🗑 削除する", bg="#e74c3c", fg="white", font=("MS ゴシック", 10, "bold"),

                          command=make_delete_cmd()).pack(side="right", pady=5)
 
    def approve_job(self, job):

        job["status"] = "approved"

        self.save_jobs_db()

        messagebox.showinfo("承認完了", f"「{job['title']}」の掲載を許可しました！")

        self.show_admin_screen()
 
    # ★追加：仕事を削除する関数★

    def delete_job(self, job):

        # 削除前に確認のポップアップを出します

        confirm = messagebox.askyesno("確認", f"「{job['title']}」を本当に削除しますか？\n※この操作は元に戻せません。")

        if confirm:

            # 同じIDのものをリストから除外して上書きする

            self.job_data = [j for j in self.job_data if j.get("id") != job.get("id")]

            self.save_jobs_db()

            messagebox.showinfo("削除完了", "募集を削除しました。")

            # 画面を再読み込みして最新状態にする

            self.show_admin_screen()
 
 
    # ------------------------------------------

    # 4. シニア側：仕事一覧画面

    # ------------------------------------------

    def show_job_list(self):

        self.clear_screen()

        header = tk.Frame(self.root, bg="#d35400", pady=15)

        header.pack(fill="x")

        tk.Label(header, text=f"👤 {self.current_user['name']}さん", fg="white", bg="#d35400", font=("MS ゴシック", 12)).pack(side="left", padx=15)

        tk.Button(header, text="ログアウト", bg="#e74c3c", fg="white", command=self.show_login_screen, relief="flat", padx=10).pack(side="right", padx=10)

        tk.Button(header, text="応募履歴", bg="#f39c12", fg="white", command=self.show_history, relief="flat", padx=10).pack(side="right", padx=5)

        tk.Button(header, text="➕ お願いを投稿", bg="#27ae60", fg="white", command=self.show_user_post_screen, relief="flat", font=("MS ゴシック", 10, "bold"), padx=10).pack(side="right", padx=5)
 
        tk.Label(self.root, text=f"📍 {self.current_user['city']} 周辺の募集", font=("MS ゴシック", 16, "bold"), bg="#F0F2F5", pady=20).pack()
 
        canvas = tk.Canvas(self.root, bg="#F0F2F5", highlightthickness=0)

        scroll_frame = tk.Frame(canvas, bg="#F0F2F5")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=480)

        canvas.pack(side="left", fill="both", expand=True)
 
        display_jobs = [j for j in self.job_data if j.get("status") == "approved"]
 
        if not display_jobs:

            tk.Label(scroll_frame, text="現在募集中の求人はありません。\n上の「お願いを投稿」から募集もできます！", 

                     font=("MS ゴシック", 12), bg="#F0F2F5", fg="#7f8c8d", pady=50).pack()

        else:

            for job in reversed(display_jobs): 

                card = tk.Frame(scroll_frame, bg="white", padx=15, pady=15, bd=0)

                card.pack(fill="x", padx=20, pady=10)

                if job["title"] in self.current_user.get("history", []):

                    tk.Label(card, text="応募済み", bg="#95a5a6", fg="white", font=("MS ゴシック", 9)).pack(anchor="e")
 
                tk.Label(card, text=job["title"], font=("MS ゴシック", 14, "bold"), bg="white", fg="#2c3e50").pack(anchor="w")

                tk.Label(card, text=f"💰 {job['pay']} ⏰ {job['time']}", font=("MS ゴシック", 12), bg="white", fg="#e67e22").pack(anchor="w", pady=5)

                tk.Label(card, text=f"📍 場所: {job['loc']}", font=("MS ゴシック", 10), bg="white", fg="gray").pack(anchor="w")

                def make_detail_cmd(target_job=job):

                    return lambda: self.show_job_detail(target_job)
 
                tk.Button(card, text="詳しく見る ＞", bg="#3498db", fg="white", font=("MS ゴシック", 11, "bold"),

                          relief="flat", command=make_detail_cmd()).pack(side="right", pady=5)
 
    # ------------------------------------------

    # 5. 仕事詳細画面

    # ------------------------------------------

    def show_job_detail(self, job):

        self.clear_screen()

        tk.Label(self.root, text="お仕事の詳細", font=("MS ゴシック", 18, "bold"), bg="#F0F2F5", pady=20).pack()

        detail_frame = tk.Frame(self.root, bg="white", padx=25, pady=25)

        detail_frame.pack(fill="both", padx=20, expand=True)
 
        tk.Label(detail_frame, text=job["title"], font=("MS ゴシック", 18, "bold"), bg="white", fg="#d35400", wraplength=400).pack(anchor="w")

        specs = [("⏰ 日時", job["time"]), ("💰 給与/お礼", job["pay"]), ("🎒 持ち物", job["items"]), ("📍 勤務地", job["loc"])]

        for icon, val in specs:

            f = tk.Frame(detail_frame, bg="white", pady=5)

            f.pack(fill="x")

            tk.Label(f, text=icon, font=("MS ゴシック", 11, "bold"), bg="white", width=10, anchor="w").pack(side="left")

            tk.Label(f, text=val, font=("MS ゴシック", 11), bg="white").pack(side="left")
 
        tk.Label(detail_frame, text="\n🗺 地図で場所を確認する", font=("MS ゴシック", 12, "bold"), bg="white").pack(anchor="w")

        map_frame = tk.Frame(detail_frame, bg="#ecf0f1", pady=20)

        map_frame.pack(fill="x", pady=10)

        tk.Label(map_frame, text=f"勤務地：{job['loc']}\n(ボタンを押すと地図が開きます)", bg="#ecf0f1", fg="#34495e").pack()

        tk.Button(map_frame, text="📍 Googleマップを開く", bg="#4285F4", fg="white", font=("MS ゴシック", 12, "bold"),

                  padx=20, pady=10, command=lambda: self.open_map(job["map"])).pack(pady=10)
 
        is_applied = job["title"] in self.current_user.get("history", [])

        btn_text = "この仕事に応募する" if not is_applied else "すでに応募済みです"

        btn_color = "#27ae60" if not is_applied else "#95a5a6"

        def do_apply():

            if not is_applied:

                if "history" not in self.current_user:

                    self.current_user["history"] = []

                self.current_user["history"].append(job["title"])

                self.save_user_db()

                messagebox.showinfo("完了", "応募しました！履歴に保存しました。")

                self.show_job_list()
 
        tk.Button(self.root, text=btn_text, bg=btn_color, fg="white", font=("MS ゴシック", 18, "bold"),

                  pady=20, command=do_apply, state="normal" if not is_applied else "disabled").pack(fill="x", side="bottom")

        tk.Button(self.root, text="一覧に戻る", command=self.show_job_list).pack(side="bottom", pady=10)
 
    # ------------------------------------------

    # 6. 応募履歴画面

    # ------------------------------------------

    def show_history(self):

        self.clear_screen()

        tk.Label(self.root, text="📋 応募履歴", font=("MS ゴシック", 22, "bold"), bg="#F0F2F5", pady=30).pack()

        history = self.current_user.get("history", [])

        if not history:

            tk.Label(self.root, text="まだ応募履歴がありません。\nお仕事を探してみましょう！", bg="#F0F2F5", font=("MS ゴシック", 12)).pack(pady=50)

        else:

            for title in history:

                h_card = tk.Frame(self.root, bg="white", padx=20, pady=15, bd=1, relief="flat")

                h_card.pack(fill="x", padx=30, pady=5)

                tk.Label(h_card, text=f"✅ {title}", font=("MS ゴシック", 14, "bold"), bg="white", fg="#27ae60").pack(side="left")

                tk.Label(h_card, text="応募完了", font=("MS ゴシック", 10), bg="white", fg="gray").pack(side="right")
 
        tk.Button(self.root, text="お仕事一覧に戻る", font=("MS ゴシック", 14, "bold"), bg="#d35400", fg="white",

                  pady=10, command=self.show_job_list).pack(side="bottom", pady=40, padx=40, fill="x")
 
if __name__ == "__main__":

    root = tk.Tk()

    app = AkitaJobApp(root)

    root.mainloop()
 

