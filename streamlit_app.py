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

# Thiết lập cấu hình trang và tiêu đề
st.set_page_config(page_title='Hệ Thống Báo Cáo', layout='wide')

# Hiển thị logo
st.image('logo.png', width=100)

# Tạo thanh bên với các menu
st.sidebar.title('Menu')

# Tạo các menu chính và phụ
menu = {
    'Dashboard': [],
    'Bis': ['Bảng kê thu chi', 'Bảng kê tạm ứng', 'Doanh thu'],
    'His': ['Cấp cứu', 'Khám bệnh', 'Nội Trú', 'Tổng hợp'],
    'Phis': ['Báo cáo NXT', 'Báo cáo tổng hợp', 'Nhập kho', 'Xuất kho'],
    'Ris': [],
    'Ensua': [],
    'System': []
}

# Tạo các menu con
sub_menu = {
    'Khám bệnh': ['Danh sách đăng ký', 'Danh sách khám bệnh'],
    'Nội Trú': ['Danh sách hiện diện'],
    'Tổng hợp': ['Vụ kế hoạch', 'Vụ điều trị']
}

# Hiển thị toàn bộ menu chính và các mục con
for main_item, sub_items in menu.items():
    st.sidebar.markdown(f'**{main_item}**')
    for sub_item in sub_items:
        if sub_item in sub_menu:
            for sub_sub_item in sub_menu[sub_item]:
                st.sidebar.markdown(f'- {sub_sub_item}')
        else:
            st.sidebar.markdown(f'- {sub_item}')

# Phần điều kiện lọc
st.title('Hệ Thống Báo Cáo')
st.markdown('### Điều kiện lọc')
col1, col2 = st.columns(2)
with col1:
    from_date = st.date_input('Từ ngày', value=pd.to_datetime('2025-01-01'))
with col2:
    to_date = st.date_input('Đến ngày', value=pd.to_datetime('2025-12-31'))

col3, col4 = st.columns(2)
with col3:
    ma = st.text_input('Mã')
with col4:
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

# Nút in ra PDF
if filter_button:
    col5, col6 = st.columns(2)
    with col5:
        st.button('Xem trước mẫu in')
    with col6:
        st.button('In ra PDF')

# Hiển thị bảng dữ liệu mẫu khi chưa chọn báo cáo
if not filter_button:
    st.write('Bảng dữ liệu mẫu:')
    st.dataframe(report_data)
