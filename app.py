from flask import Flask, redirect, url_for
from routes import register_routes
from models import User, Session
from flask_login import LoginManager, login_required

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your-secret-key'    # 用於 session 加密，是 Flask-Login 管理登入狀態所必需的（可設為任意長字串）
#'your-secret-key' = 這是一組伺服器用來加密 session 的密碼，Flask 要求這個名字不可改
login_manager = LoginManager()      # 初始化 LoginManager，讓 Flask-Login 能管理使用者登入狀態
login_manager.login_view = 'auth.login'     # 指定未登入使用者如果訪問需要登入的頁面時，自動導向的 endpoint 名稱（後面我們會在 routes/auth.py 中實作 `login`）

# 這個函式讓 Flask-Login 知道「如何根據 user_id 找出對應的使用者」
# 每次頁面刷新、登入狀態檢查都會自動觸發
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with Session() as session:
        return session.get(User, int(user_id))
        # 這裡的 session 是你自己建立的資料庫操作環境
        # session.get(User, id) 會回傳符合 id 的 User 物件，或是 None


register_routes(app)
@app.route("/")
@login_required
def home():
    return redirect(url_for("expense.expense"))






if __name__ == "__main__":
    app.run(debug = True)

