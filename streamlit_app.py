import streamlit as st
import pandas as pd

# Hàm để giả lập dữ liệu báo cáo
def generate_report_data():
    data = {
        'ID': [1, 2, 3, 4, 5],
        'Mã': ['A001', 'A002', 'A003', 'A004', 'A005'],
        'Tên': ['Sản phẩm 1', 'Sản phẩm 2', 'Sản phẩm 3', 'Sản phẩm 4', 'Sản phẩm 5'],
        'Ngày': ['2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01']
    }
    df = pd.DataFrame(data)
    return df

# Thiết lập cấu hình trang và tiêu đề
st.set_page_config(page_title='Hệ Thống Báo Cáo', layout='wide')

# Hiển thị tiêu đề và logo
st.markdown("<h1 style='text-align: center; color: black;'>Hệ Thống Báo Cáo</h1>", unsafe_allow_html=True)
st.image('logo.png', use_container_width=True)

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
    'System': ['Danh mục biệt dược', 'Danh mục viện phí', 'Danh mục icd']
}

# Tạo các menu con
sub_menu = {
    'Khám bệnh': ['Danh sách đăng ký', 'Danh sách khám bệnh'],
    'Nội Trú': ['Danh sách hiện diện'],
    'Tổng hợp': ['Vụ kế hoạch', 'Vụ điều trị']
}

# Hiển thị toàn bộ menu chính và các mục con khi click vào mục chính
for main_item, sub_items in menu.items():
    if sub_items:
        with st.sidebar.expander(main_item, expanded=False):
            for sub_item in sub_items:
                if sub_item in sub_menu:
                    with st.sidebar.expander(sub_item, expanded=False):
                        for sub_sub_item in sub_menu[sub_item]:
                            st.sidebar.markdown(f'- {sub_sub_item}')
                else:
                    st.sidebar.markdown(f'- {sub_item}')
    else:
        st.sidebar.markdown(main_item)

# Phần điều kiện lọc
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

# Nút thực hiện lọc và in ra PDF
col5, col6 = st.columns(2)
with col5:
    filter_button = st.button('Thực hiện lọc')
with col6:
    pdf_button = st.button('In ra PDF')

# Sinh dữ liệu báo cáo giả lập
report_data = generate_report_data()

# Lọc và hiển thị dữ liệu khi bấm nút Thực hiện lọc
if filter_button:
    filtered_data = report_data[
        (report_data['Ngày'] >= str(from_date)) &
        (report_data['Ngày'] <= str(to_date)) &
        (report_data['Mã'].str.contains(ma, case=False)) &
        (report_data['Tên'].str.contains(ten, case=False))
    ]
    st.subheader('Dữ liệu báo cáo')
    st.dataframe(filtered_data)

    if pdf_button:
        st.write('Dữ liệu sẽ được in ra PDF')

# Hiển thị dữ liệu mẫu khi click vào Danh mục biệt dược hoặc Danh mục viện phí
if 'Danh mục biệt dược' in menu['System']:
    with st.sidebar.expander('Danh mục biệt dược', expanded=False):
        if st.sidebar.button('Hiển thị dữ liệu', key='1'):
            df = generate_report_data()
            st.subheader('Danh mục biệt dược')
            st.dataframe(df)

if 'Danh mục viện phí' in menu['System']:
    with st.sidebar.expander('Danh mục viện phí', expanded=False):
        if st.sidebar.button('Hiển thị dữ liệu', key='2'):
            df = generate_report_data()
            df['Đơn giá'] = [1000, 1500, 2000, 2500, 3000]
            st.subheader('Danh mục viện phí')
            st.dataframe(df)

