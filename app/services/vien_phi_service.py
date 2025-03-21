# Xử lý logic nghiệp vụ
from app.models.vien_phi import ThuChiRaVien
from abc import ABC, abstractmethod

class BaseService(ABC):
    """
    Lớp cơ sở cho các service
    """
    pass

class VienPhiService(BaseService):
    """
    Service xử lý logic nghiệp vụ cho Viện phí
    """
    
    @staticmethod
    def get_thu_chi_ra_vien(ngay_bat_dau=None, ngay_ket_thuc=None, mabn=None, hoten=None):
        """
        Lấy dữ liệu thu chi ra viện và thực hiện xử lý bổ sung nếu cần
        """
        records = ThuChiRaVien.get_data(ngay_bat_dau, ngay_ket_thuc, mabn, hoten)
        
        # Xử lý bổ sung (nếu cần)
        # Ví dụ: tính tổng tiền
        tong_tien = sum(record.sotien for record in records)
        
        # Định dạng số tiền
        for record in records:
            record.sotien_fmt = f"{record.sotien:,} VNĐ"
        
        return {
            'records': records,
            'tong_tien': tong_tien,
            'tong_tien_fmt': f"{tong_tien:,} VNĐ",
            'so_luong': len(records)
        }