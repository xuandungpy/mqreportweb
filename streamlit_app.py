import streamlit as st
import pandas as pd
import requests

# Gọi API để lấy dữ liệu
response = requests.get('http://mqsoft.ddns.net:5000/get-data')
data = response.json()

# Chuyển dữ liệu thành DataFrame
df = pd.DataFrame(data)

st.title('MQ Report web')
st.dataframe(df)
