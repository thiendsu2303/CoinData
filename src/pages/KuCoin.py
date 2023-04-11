import streamlit as st
import datetime
import pandas as pd
import numpy as np
import ProcessingData as tt

apiKey = "PSI4IFEFAUF8USVB6M5BSEAM1VB9CX7FJZ"
data = pd.read_csv('./input.csv')
test_address = data['address'].values
address = test_address[0]
page = 1
offset = 10000
list = tt.ProcessingData(address, page, offset,apiKey)

st.title("Dữ liệu của sàn :red[KuCoin]:chart_with_upwards_trend:")

# Lấy thời gian hiện tại
# now = str(datetime.datetime.now())
# st.subheader("Thời gian hiện tại là: "+ "_:red["+now+"]_")
st.subheader("Mời chọn Token muốn xem biểu đồ: ")
