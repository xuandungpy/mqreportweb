# Xác thực đăng nhập
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app import login_manager

auth = Blueprint('auth', __name__)

# Giả lập người dùng (trong thực tế, lấy từ CSDL)
class User:
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        return str(self.id)

# Giả lập cơ sở dữ liệu người dùng
users = {
    1: User(1, 'admin', 'pbkdf2:sha256:150000$abc123$...'),  # Password: admin123
    2: User(2, 'user', 'pbkdf2:sha256:150000$def456$...')    # Password: user123
}

@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Trong thực tế, kiểm tra từ CSDL
        # Giả lập đăng nhập
        if username == 'admin' and password == 'admin123':
            login_user(users[1])
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không chính xác', 'danger')
    
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))