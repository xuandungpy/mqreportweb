# Model cho Viện phí
import requests
from datetime import datetime
from app.config import Config
from abc import ABC, abstractmethod

class BaseModel(ABC):
    """
    Lớp cơ sở cho tất cả các model dữ liệu
    """
    @abstractmethod
    def to_dict(self):
        """Chuyển đổi đối tượng thành dict"""
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        """Tạo đối tượng từ dict"""
        pass

class ThanhToanRecord(BaseModel):
    """
    Đối tượng đại diện cho một bản ghi thanh toán viện phí
    """
    def __init__(self, ngay=None, sobienlai=None, mabn=None, hoten=None, sotien=0):
        self.ngay = ngay
        self.sobienlai = sobienlai
        self.mabn = mabn
        self.hoten = hoten
        self.sotien = sotien
    
    def to_dict(self):
        return {
            'ngay': self.ngay.strftime('%d/%m/%Y') if isinstance(self.ngay, datetime) else self.ngay,
            'sobienlai': self.sobienlai,
            'mabn': self.mabn,
            'hoten': self.hoten,
            'sotien': self.sotien
        }
    
    @classmethod
    def from_dict(cls, data):
        ngay = data.get('ngay')
        if isinstance(ngay, str):
            try:
                ngay = datetime.strptime(ngay, '%d/%m/%Y')
            except ValueError:
                # Xử lý nếu định dạng ngày không đúng
                pass
        
        return cls(
            ngay=ngay,
            sobienlai=data.get('sobienlai'),
            mabn=data.get('mabn'),
            hoten=data.get('hoten'),
            sotien=data.get('sotien', 0)
        )

class ThuChiRaVien:
    """
    Quản lý dữ liệu thu chi ra viện
    """
    @staticmethod
    def get_data(ngay_bat_dau=None, ngay_ket_thuc=None, mabn=None, hoten=None):
        """
        Lấy dữ liệu thu chi ra viện từ API
        """
        # Trong thực tế, sẽ gọi API thực, nhưng ở đây tạo dữ liệu mẫu
        # Giả lập gọi API
        try:
            # Đối với trường hợp thực tế, bạn sẽ sử dụng requests để gọi API
            # response = requests.get(
            #     f"{Config.API_ENDPOINT}/vien-phi/thu-chi-ra-vien",
            #     params={
            #         'ngay_bat_dau': ngay_bat_dau,
            #         'ngay_ket_thuc': ngay_ket_thuc,
            #         'mabn': mabn,
            #         'hoten': hoten
            #     }
            # )
            # data = response.json()
            
            # Tạo dữ liệu mẫu
            data = [
                {
                    'ngay': '01/03/2025',
                    'sobienlai': 'BL0001',
                    'mabn': '25000123',
                    'hoten': 'Nguyễn Văn A',
                    'sotien': 1500000
                },
                {
                    'ngay': '01/03/2025',
                    'sobienlai': 'BL0002',
                    'mabn': '25000124',
                    'hoten': 'Trần Thị B',
                    'sotien': 2300000
                },
                {
                    'ngay': '02/03/2025',
                    'sobienlai': 'BL0003',
                    'mabn': '25000125',
                    'hoten': 'Lê Văn C',
                    'sotien': 1800000
                },
                {
                    'ngay': '03/03/2025',
                    'sobienlai': 'BL0004',
                    'mabn': '25000126',
                    'hoten': 'Phạm Thị D',
                    'sotien': 950000
                },
                {
                    'ngay': '04/03/2025',
                    'sobienlai': 'BL0005',
                    'mabn': '25000127',
                    'hoten': 'Hoàng Văn E',
                    'sotien': 3200000
                }
            ]
            
            # Lọc dữ liệu nếu có điều kiện tìm kiếm
            if mabn:
                data = [item for item in data if mabn in item['mabn']]
            if hoten:
                data = [item for item in data if hoten.lower() in item['hoten'].lower()]
            
            # Chuyển đổi dữ liệu thành đối tượng ThanhToanRecord
            records = [ThanhToanRecord.from_dict(item) for item in data]
            return records
            
        except Exception as e:
            # Xử lý ngoại lệ
            print(f"Lỗi khi lấy dữ liệu từ API: {e}")
            return []