from flask import Blueprint, render_template, session, redirect, url_for, request
from models.payment_report import PaymentReport
from datetime import datetime

report_bp = Blueprint('report', __name__)

def login_required(f):
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@report_bp.route('/main')
@login_required
def main():
    return render_template('main.html')

@report_bp.route('/report/payment/in_out')
@login_required
def payment_in_out():
    report = PaymentReport()
    data = report.fetch_data()
    processed_data = report.process_data()
    return render_template('report_payment.html', data=processed_data)

@report_bp.route('/report/his/examination/register_list', methods=['GET', 'POST'])
@login_required
def register_list():
    # Giả lập dữ liệu ban đầu - 10 dòng
    mock_data = [
        {"ngay_dk": "20-03-2025", "ma_dk": "DK001", "mabn": "BN001", "hoten": "Nguyễn Văn A", "trang_thai": "Chờ khám", "ma_khoa": "KP001"},
        {"ngay_dk": "21-03-2025", "ma_dk": "DK002", "mabn": "BN002", "hoten": "Trần Thị B", "trang_thai": "Đã khám", "ma_khoa": "KP002"},
        {"ngay_dk": "21-03-2025", "ma_dk": "DK003", "mabn": "BN003", "hoten": "Lê Văn C", "trang_thai": "Chờ khám", "ma_khoa": "KP001"},
        {"ngay_dk": "22-03-2025", "ma_dk": "DK004", "mabn": "BN004", "hoten": "Phạm Thị D", "trang_thai": "Đã khám", "ma_khoa": "KP003"},
        {"ngay_dk": "22-03-2025", "ma_dk": "DK005", "mabn": "BN005", "hoten": "Hoàng Văn E", "trang_thai": "Chờ khám", "ma_khoa": "KP002"},
        {"ngay_dk": "23-03-2025", "ma_dk": "DK006", "mabn": "BN006", "hoten": "Nguyễn Thị F", "trang_thai": "Đã khám", "ma_khoa": "KP001"},
        {"ngay_dk": "23-03-2025", "ma_dk": "DK007", "mabn": "BN007", "hoten": "Trần Văn G", "trang_thai": "Chờ khám", "ma_khoa": "KP003"},
        {"ngay_dk": "24-03-2025", "ma_dk": "DK008", "mabn": "BN008", "hoten": "Lê Thị H", "trang_thai": "Đã khám", "ma_khoa": "KP002"},
        {"ngay_dk": "24-03-2025", "ma_dk": "DK009", "mabn": "BN009", "hoten": "Phạm Văn I", "trang_thai": "Chờ khám", "ma_khoa": "KP001"},
        {"ngay_dk": "25-03-2025", "ma_dk": "DK010", "mabn": "BN010", "hoten": "Hoàng Thị K", "trang_thai": "Đã khám", "ma_khoa": "KP003"}
    ]
    
    # Ngày hiện tại
    current_date = datetime.now()
    current_date_display = current_date.strftime('%d-%m-%Y')  # Định dạng hiển thị: dd-mm-yyyy
    current_date_input = current_date.strftime('%Y-%m-%d')    # Định dạng cho input date: yyyy-mm-dd
    
    filtered_data = mock_data.copy()
    error = None

    # Giá trị tìm kiếm mặc định hoặc từ form
    ngay_tu = request.form.get('ngay_tu', current_date_input) if request.method == 'POST' else current_date_input
    ngay_den = request.form.get('ngay_den', current_date_input) if request.method == 'POST' else current_date_input
    ma_khoa = request.form.get('ma_khoa', '').strip().upper()
    mabn = request.form.get('mabn', '').strip().upper()

    if request.method == 'POST' and (not ngay_tu or not ngay_den):
        error = "Vui lòng nhập đầy đủ Từ ngày và Đến ngày."
    else:
        # Chuyển đổi định dạng ngày từ yyyy-mm-dd (input) hoặc dd-mm-yyyy (dữ liệu) sang datetime để so sánh
        def parse_date(date_str, format='%Y-%m-%d'):
            try:
                return datetime.strptime(date_str, format)
            except ValueError:
                return None

        ngay_tu_dt = parse_date(ngay_tu)
        ngay_den_dt = parse_date(ngay_den)

        if not ngay_tu_dt or not ngay_den_dt:
            error = "Định dạng ngày không hợp lệ."
        else:
            # Lọc dữ liệu ngay cả khi GET (mở trang lần đầu)
            filtered_data = [item for item in filtered_data if parse_date(item['ngay_dk'], '%d-%m-%Y') >= ngay_tu_dt]
            filtered_data = [item for item in filtered_data if parse_date(item['ngay_dk'], '%d-%m-%Y') <= ngay_den_dt]
            if ma_khoa:
                filtered_data = [item for item in filtered_data if item['ma_khoa'] == ma_khoa]
            if mabn:
                filtered_data = [item for item in filtered_data if item['mabn'] == mabn]

    # Truyền các giá trị tìm kiếm để giữ nguyên trong form
    return render_template('register_list.html', data=filtered_data, current_date_input=current_date_input, 
                           ngay_tu=ngay_tu, ngay_den=ngay_den, ma_khoa=ma_khoa, mabn=mabn, error=error)