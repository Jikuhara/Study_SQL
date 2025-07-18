from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # セキュリティのため適切なランダム文字列にしてください

# Flask-Login の初期化
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # ログインが必要なページへアクセスした際にリダイレクト

# Userクラス（Flask-Login用のユーザーモデル）
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def get(user_id):
        conn = sqlite3.connect('SQLtest.db')
        cur = conn.cursor()
        cur.execute("SELECT id, username, password_hash FROM users WHERE id = ?", (user_id,))
        result = cur.fetchone()
        conn.close()
        if result:
            return User(*result)
        return None

# ユーザーIDからユーザーオブジェクトをロードするコールバック
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# ホームページ（認証前も後も表示可能）
@app.route("/")
def index():
    return render_template("index.html", user=current_user)

# ユーザー登録ページ
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)
        conn = sqlite3.connect('SQLtest.db')
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
            conn.commit()
            flash("Registration successful! Please log in.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already exists. Please choose another.")
            return redirect(url_for("register"))
        finally:
            conn.close()
    return render_template("register.html")

# ログインページ
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('SQLtest.db')
        cur = conn.cursor()
        cur.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
        result = cur.fetchone()
        conn.close()
        if result and check_password_hash(result[2], password):
            user = User(*result)
            login_user(user)
            flash("Logged in successfully.")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.")
            return redirect(url_for("login"))
    return render_template("login.html")

# 保護されたダッシュボード（ログインが必須）
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        # ユーザーから送信された新しいユーザー名を取得
        new_username = request.form["username"]
        conn = sqlite3.connect("SQLtest.db")
        cur = conn.cursor()
        try:
            # ユーザー名更新（ユーザーIDで特定）
            cur.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, current_user.id))
            conn.commit()
            flash("Profile updated successfully!")
            # ここで current_user の情報を更新する処理も入れるとよいですが、
            # Flask-Login の User オブジェクトは通常DBから都度ロードする方式なのでここでは省略
        except Exception as e:
            flash("Update failed: " + str(e))
        finally:
            conn.close()
        return redirect(url_for("profile"))
    return render_template("profile.html", user=current_user)

# ログアウト
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("index"))

# 大会一覧表示
@app.route("/tournaments")
def tournaments_list():
    conn = sqlite3.connect("SQLtest.db")
    cur = conn.cursor()
    cur.execute("SELECT id, name, date, location, level FROM tournaments ORDER BY date DESC")
    tournaments = cur.fetchall()
    conn.close()
    return render_template("tournaments/list.html", tournaments=tournaments)

# 大会登録画面
@app.route("/tournaments/create", methods=["GET", "POST"])
@login_required
def tournament_create():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        level = request.form["level"]  # 追加：級の情報を取得
        date = request.form["date"]
        location = request.form["location"]
        max_participants = request.form["max_participants"]
        registration_deadline = request.form["registration_deadline"]
        
        conn = sqlite3.connect("SQLtest.db")
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO tournaments 
                (name, description, level, date, location, max_participants, 
                registration_deadline, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, description, level, date, location, max_participants, 
                registration_deadline, current_user.id))
            conn.commit()
            flash("大会を登録しました")
            return redirect(url_for("tournaments_list"))
        except Exception as e:
            flash(f"大会登録に失敗しました: {str(e)}")
        finally:
            conn.close()
    
    return render_template("tournaments/create.html")

# 大会詳細表示
@app.route("/tournaments/<int:tournament_id>")
def tournament_detail(tournament_id):
    conn = sqlite3.connect("SQLtest.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT t.*, u.username 
        FROM tournaments t 
        JOIN users u ON t.created_by = u.id 
        WHERE t.id = ?
    """, (tournament_id,))
    tournament = cur.fetchone()
    conn.close()
    
    if not tournament:
        flash("大会が見つかりません")
        return redirect(url_for("tournaments_list"))
        
    return render_template("tournaments/detail.html", tournament=tournament)

if __name__ == '__main__':
    app.run(debug=True)
