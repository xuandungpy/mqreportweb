# Cấu hình chung
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # Cấu hình kết nối Oracle
    ORACLE_USERNAME = os.environ.get('ORACLE_USERNAME') or 'username'
    ORACLE_PASSWORD = os.environ.get('ORACLE_PASSWORD') or 'password'
    ORACLE_HOST = os.environ.get('ORACLE_HOST') or 'localhost'
    ORACLE_PORT = os.environ.get('ORACLE_PORT') or '1521'
    ORACLE_SERVICE = os.environ.get('ORACLE_SERVICE') or 'xe'
    
    # API endpoint (giả lập)
    API_ENDPOINT = os.environ.get('API_ENDPOINT') or 'http://localhost:5000/api'