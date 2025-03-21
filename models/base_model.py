class BaseModel:
    def __init__(self):
        self.data = []

    def fetch_data(self):
        """Phương thức cơ bản để lấy dữ liệu - sẽ được override ở các class con"""
        pass

    def process_data(self):
        """Phương thức cơ bản để xử lý dữ liệu"""
        return self.data