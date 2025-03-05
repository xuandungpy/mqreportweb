from flask import Flask, render_template, request, Response, send_file
import requests
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Sử dụng backend Agg để tránh lỗi GUI
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table
import xlsxwriter
import json

app = Flask(__name__)

# URL API mẫu
API_URL = "https://jsonplaceholder.typicode.com/posts"

# Danh sách dữ liệu nhập liệu (lưu tạm trong bộ nhớ)
input_data = []

# Lấy dữ liệu từ API
def fetch_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    return []

# Lọc dữ liệu và chỉ lấy tối đa 20 record
def filter_data(date=None, user_id=None, title=None):
    data = fetch_data()
    df = pd.DataFrame(data)
    
    if user_id and user_id != "all":
        df = df[df['userId'] == int(user_id)]
    if title:
        df = df[df['title'].str.contains(title, case=False, na=False)]
    return df.head(20)

# Trang chủ
@app.route('/')
def index():
    return render_template('index.html')

# Menu Báo cáo
@app.route('/report', methods=['GET', 'POST'])
def report():
    date = request.form.get('date')
    user_id = request.form.get('userId')
    title = request.form.get('title')
    
    df = filter_data(date, user_id, title)
    all_data = fetch_data()
    user_ids = sorted(set([str(item['userId']) for item in all_data]))
    
    table_html = df.to_html(classes='table table-striped', index=False) if not df.empty else "<p>Không có dữ liệu</p>"
    
    plt.figure(figsize=(8, 6))
    if not df.empty:
        df['userId'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Tỷ lệ bài viết theo UserID')
        plt.ylabel('')
    img_pie = BytesIO()
    plt.savefig(img_pie, format='png')
    img_pie.seek(0)
    pie_url = base64.b64encode(img_pie.getvalue()).decode('utf8')
    plt.close()
    
    plt.figure(figsize=(10, 6))
    if not df.empty:
        df.groupby('userId')['id'].count().plot(kind='line', marker='o')
        plt.title('Số lượng bài viết theo UserID')
        plt.xlabel('UserID')
        plt.ylabel('Số lượng')
    img_line = BytesIO()
    plt.savefig(img_line, format='png')
    img_line.seek(0)
    line_url = base64.b64encode(img_line.getvalue()).decode('utf8')
    plt.close()
    
    return render_template('report.html', table=table_html, pie_url=pie_url, line_url=line_url, user_ids=user_ids,
                          selected_date=date, selected_user_id=user_id, selected_title=title)

# Xuất PDF
@app.route('/report/export_pdf', methods=['POST'])
def export_pdf():
    date = request.form.get('date')
    user_id = request.form.get('userId')
    title = request.form.get('title')
    df = filter_data(date, user_id, title)
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    data = [df.columns.values.tolist()] + df.values.tolist()
    table = Table(data)
    elements.append(table)
    doc.build(elements)
    
    buffer.seek(0)
    return Response(buffer.getvalue(), mimetype='application/pdf',
                   headers={'Content-Disposition': 'attachment;filename=report.pdf'})

# Xuất Excel
@app.route('/report/export_excel', methods=['POST'])
def export_excel():
    date = request.form.get('date')
    user_id = request.form.get('userId')
    title = request.form.get('title')
    df = filter_data(date, user_id, title)
    
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Report', index=False)
    writer.close()
    output.seek(0)
    return send_file(output, download_name="report.xlsx", as_attachment=True)

# Menu Nhập liệu
@app.route('/input', methods=['GET', 'POST'])
def input():
    global input_data
    all_data = fetch_data()
    user_ids = sorted(set([str(item['userId']) for item in all_data]))
    
    if request.method == 'POST':
        if 'add' in request.form:
            # Thêm dữ liệu từ form
            date = request.form.get('date')
            user_id = request.form.get('userId')
            title = request.form.get('title')
            is_active = request.form.get('is_active') == 'on'
            input_data.append({'date': date, 'userId': user_id, 'title': title, 'is_active': is_active})
        elif 'update' in request.form:
            # Cập nhật dữ liệu từ grid
            input_data = json.loads(request.form.get('grid_data'))
    
    df_input = pd.DataFrame(input_data)
    grid_html = df_input.to_html(classes='table table-striped', index=False) if not df_input.empty else "<p>Chưa có dữ liệu</p>"
    
    return render_template('input.html', user_ids=user_ids, grid_html=grid_html, input_data=input_data)

if __name__ == '__main__':
    app.run(debug=True)