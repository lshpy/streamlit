import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import os

# Streamlit 앱 설정
st.title('연령/성별에 따른 예측 대출 건수')

# 이미지 경로 설정
image_paths = [
    r'C:\Users\user\Desktop\도서관_공모전\최종\12_다대출그룹\대출건수 예측\book_analysis_plots-이미지-0.jpg',
    r'C:\Users\user\Desktop\도서관_공모전\최종\12_다대출그룹\대출건수 예측\book_analysis_plots-이미지-1.jpg'
]

# 두 개의 이미지를 Streamlit에 표시
for image_path in image_paths:
    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image, caption=os.path.basename(image_path))
    else:
        st.error(f"이미지 파일을 찾을 수 없습니다: {image_path}")

# Excel 파일 경로 설정
excel_path = r'C:\Users\user\Desktop\도서관_공모전\최종\12_다대출그룹\대출건수 예측\book_analysis_summary.xlsx'

# Excel 데이터 로드
if os.path.exists(excel_path):
    df = pd.read_excel(excel_path)

    # '연령_성별' 열에서 유니크한 카테고리 추출
    categories = df['연령_성별'].unique()
    selected_category = st.selectbox('카테고리 선택', categories)

    # 선택한 카테고리에 해당하는 데이터 필터링
    selected_data = df[df['연령_성별'] == selected_category]

    # 필요한 열만 추출 (예측 대출건수, 실제 대출건수)
    filtered_data = selected_data[['예측 대출건수', '실제 대출건수']]

    # 필터링된 데이터 표시
    st.write(f"선택한 카테고리: {selected_category}")
    st.write(filtered_data)

    # 데이터를 세로 막대 그래프로 시각화
    chart_data = filtered_data.reset_index().melt('index', var_name='Type', value_name='Count')

    bar_chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('Type:N', title=None),
        y=alt.Y('Count:Q', title='대출건수'),
        color='Type:N'
    ).properties(
        width=600,
        height=400
    )

    st.altair_chart(bar_chart, use_container_width=True)
else:
    st.error("Excel 파일을 찾을 수 없습니다.")
