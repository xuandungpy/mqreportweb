# Kết nối CSDL Oracle
import cx_Oracle
from app.config import Config

class Database:
    """
    Lớp quản lý kết nối đến cơ sở dữ liệu Oracle
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            # Khởi tạo kết nối
            connection_string = f"{Config.ORACLE_USERNAME}/{Config.ORACLE_PASSWORD}@{Config.ORACLE_HOST}:{Config.ORACLE_PORT}/{Config.ORACLE_SERVICE}"
            cls._instance.pool = cx_Oracle.SessionPool(
                user=Config.ORACLE_USERNAME,
                password=Config.ORACLE_PASSWORD,
                dsn=f"{Config.ORACLE_HOST}:{Config.ORACLE_PORT}/{Config.ORACLE_SERVICE}",
                min=2,
                max=5,
                increment=1,
                encoding="UTF-8"
            )
        return cls._instance
    
    def get_connection(self):
        """Lấy kết nối từ pool"""
        return self.pool.acquire()
    
    def release_connection(self, connection):
        """Trả kết nối về pool"""
        self.pool.release(connection)
    
    def execute_query(self, query, params=None):
        """Thực thi truy vấn và trả về kết quả dưới dạng danh sách dict"""
        connection = self.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(query, params or {})
            columns = [col[0].lower() for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return results
        finally:
            self.release_connection(connection)