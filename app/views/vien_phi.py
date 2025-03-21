# Route cho Viện phí
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.services.vien_phi_service import VienPhiService
from datetime import datetime

vien_phi = Blueprint('vien_phi', __name__, url_prefix='/vien-phi')

@vien_phi.route('/bang-ke/thu-chi-ra-vien')
@login_required
def thu_chi_ra_vien():
    """
    Hiển thị trang báo cáo thu chi ra viện
    """
    ngay_bat_dau = request.args.get('ngay_bat_dau')
    ngay_ket_thuc = request.args.get('ngay_ket_thuc')
    mabn = request.args.get('mabn')
    hoten = request.args.get('hoten')
    
    # Chuyển đổi định dạng ngày nếu cần
    if ngay_bat_dau:
        try:
            ngay_bat_dau = datetime.strptime(ngay_bat_dau, '%Y-%m-%d').strftime('%d/%m/%Y')
        except ValueError:
            ngay_bat_dau = None
    
    if ngay_ket_thuc:
        try:
            ngay_ket_thuc = datetime.strptime(ngay_ket_thuc, '%Y-%m-%d').strftime('%d/%m/%Y')
        except ValueError:
            ngay_ket_thuc = None
    
    # Lấy dữ liệu từ service
    data = VienPhiService.get_thu_chi_ra_vien(ngay_bat_dau, ngay_ket_thuc, mabn, hoten)
    
    return render_template('vien_phi/thu_chi_ra_vien.html', data=data)

@vien_phi.route('/api/bang-ke/thu-chi-ra-vien')
@login_required
def api_thu_chi_ra_vien():
    """
    API endpoint để lấy dữ liệu thu chi ra viện (cho AJAX)
    """
    ngay_bat_dau = request.args.get('ngay_bat_dau')
    ngay_ket_thuc = request.args.get('ngay_ket_thuc')
    mabn = request.args.get('mabn')
    hoten = request.args.get('hoten')
    
    # Lấy dữ liệu từ service
    data = VienPhiService.get_thu_chi_ra_vien(ngay_bat_dau, ngay_ket_thuc, mabn, hoten)
    
    # Chuyển đổi đối tượng thành dict để trả về JSON
    result = {
        'records': [record.to_dict() for record in data['records']],
        'tong_tien': data['tong_tien'],
        'tong_tien_fmt': data['tong_tien_fmt'],
        'so_luong': data['so_luong']
    }
    
    return jsonify(result)