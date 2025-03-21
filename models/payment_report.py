from models.base_model import BaseModel
import requests
from config import Config

class PaymentReport(BaseModel):
    def __init__(self):
        super().__init__()

    def fetch_data(self):
        """Lấy dữ liệu từ API - giả lập response"""
        # Thay vì gọi API thật, ta giả lập dữ liệu
        mock_api_response = [
            {"ngay": "2025-03-21", "sobienlai": "BL001", "mabn": "BN001", "hoten": "Nguyễn Văn A", "sotien": 1500000},
            {"ngay": "2025-03-21", "sobienlai": "BL002", "mabn": "BN002", "hoten": "Trần Thị B", "sotien": 2000000}
        ]
        self.data = mock_api_response
        return self.data

    def process_data(self):
        """Xử lý dữ liệu báo cáo thu chi"""
        processed_data = []
        for item in self.data:
            item['sotien_formatted'] = "{:,.0f}".format(item['sotien'])
            processed_data.append(item)
        return processed_data