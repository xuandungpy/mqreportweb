import streamlit as st
import pandas as pd
import requests

# Hàm để giả lập dữ liệu báo cáo
def generate_report_data():
    data = {
        'ID': [1, 2, 3, 4, 5],
        'MA': ['A001', 'A002', 'A003', 'A004', 'A005'],
        'TEN': ['Sản phẩm 1', 'Sản phẩm 2', 'Sản phẩm 3', 'Sản phẩm 4', 'Sản phẩm 5'],
        'Ngay': ['2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01']
    }
    df = pd.DataFrame(data)
    return df

# Hàm để hiển thị báo cáo
def display_report(df, title):
    st.subheader(title)
    st.dataframe(df)

# Thiết lập tiêu đề và mô tả cho ứng dụng
st.title('Hệ Thống Báo Cáo')
st.markdown('Chọn menu báo cáo và điều kiện lọc để hiển thị báo cáo.')

# Tạo các menu báo cáo
menu = ['Báo cáo theo Ngày', 'Báo cáo theo Mã', 'Báo cáo theo Tên']
choice = st.sidebar.selectbox('Chọn báo cáo', menu)

# Sinh dữ liệu báo cáo giả lập
report_data = generate_report_data()

# Các điều kiện lọc chung
from_date = st.sidebar.date_input('Từ ngày', value=pd.to_datetime('2025-01-01'))
to_date = st.sidebar.date_input('Đến ngày', value=pd.to_datetime('2025-12-31'))
filtered_data = report_data[(report_data['Ngay'] >= str(from_date)) & (report_data['Ngay'] <= str(to_date))]

# Hiển thị báo cáo dựa trên menu đã chọn
if choice == 'Báo cáo theo Ngày':
    st.sidebar.subheader('Điều kiện lọc')
    display_report(filtered_data, 'Báo cáo theo Ngày')

elif choice == 'Báo cáo theo Mã':
    st.sidebar.subheader('Điều kiện lọc')
    ma = st.sidebar.text_input('Nhập mã')
    filtered_data = filtered_data[filtered_data['MA'].str.contains(ma)]
    display_report(filtered_data, 'Báo cáo theo Mã')

elif choice == 'Báo cáo theo Tên':
    st.sidebar.subheader('Điều kiện lọc')
    ten = st.sidebar.text_input('Nhập tên')
    filtered_data = filtered_data[filtered_data['TEN'].str.contains(ten)]
    display_report(filtered_data, 'Báo cáo theo Tên')
