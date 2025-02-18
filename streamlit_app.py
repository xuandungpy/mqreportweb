import streamlit as st
import pandas as pd

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
st.set_page_config(page_title='Hệ Thống Báo Cáo', layout='wide')
st.image('logo.png', width=100)

st.sidebar.title('Menu')
st.sidebar.markdown('<div style="background-color: #f8d7da; padding: 10px;">', unsafe_allow_html=True)

# Tạo các menu chính
menu = {
    'Dashboard': [],
    'Bis': ['Bảng kê thu chi', 'Bảng kê tạm ứng', 'Doanh thu'],
    'His': ['Cấp cứu', 'Khám bệnh', 'Nội Trú', 'Tổng hợp'],
    'Phis': ['Báo cáo NXT', 'Báo cáo tổng hợp', 'Nhập kho', 'Xuất kho'],
    'Ris': [],
    'Ensua': [],
    'System': []
}

# Tạo các menu phụ
sub_menu = {
    'Khám bệnh': ['Danh sách đăng ký', 'Danh sách khám bệnh'],
    'Nội Trú': ['Danh sách hiện diện'],
    'Tổng hợp': ['Vụ kế hoạch', 'Vụ điều trị']
}

# Chọn menu chính
main_menu = st.sidebar.selectbox('Chọn menu', list(menu.keys()))

# Chọn menu phụ nếu có
if menu[main_menu]:
    sub_menu_choice = st.sidebar.selectbox('Chọn loại báo cáo', menu[main_menu])
else:
    sub_menu_choice = None

# Chọn menu con nếu có
if sub_menu_choice in sub_menu:
    sub_sub_menu_choice = st.sidebar.selectbox('Chọn loại báo cáo chi tiết', sub_menu[sub_menu_choice])
else:
    sub_sub_menu_choice = None

st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Phần điều kiện lọc
st.title('Hệ Thống Báo Cáo')
st.markdown('### Điều kiện lọc')
from_date = st.date_input('Từ ngày', value=pd.to_datetime('2025-01-01'))
to_date = st.date_input('Đến ngày', value=pd.to_datetime('2025-12-31'))
ma = st.text_input('Mã')
ten = st.text_input('Tên')
filter_button = st.button('Thực hiện lọc')

# Sinh dữ liệu báo cáo giả lập
report_data = generate_report_data()

# Lọc dữ liệu khi bấm nút Thực hiện lọc
if filter_button:
    filtered_data = report_data[
        (report_data['Ngay'] >= str(from_date)) &
        (report_data['Ngay'] <= str(to_date)) &
        (report_data['MA'].str.contains(ma, case=False)) &
        (report_data['TEN'].str.contains(ten, case=False))
    ]
    display_report(filtered_data, 'Dữ liệu báo cáo')

# Nút xem trước mẫu in và in ra PDF
if filter_button:
    st.button('Xem trước mẫu in')
    st.button('In ra PDF')

# Hiển thị bảng dữ liệu mẫu khi chưa chọn báo cáo
if not filter_button:
    st.write('Bảng dữ liệu mẫu:')
    st.dataframe(report_data)
