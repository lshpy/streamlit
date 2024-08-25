import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# 폰트 파일 경로 설정
font_path = r'C:\Windows\Fonts\Hancom Gothic Regular.ttf'

# 폰트 등록
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

# Excel 파일 경로
excel_path = "C:/Users/user/Desktop/도서관_공모전/최종/12_다대출그룹/도서 대출 패턴 분석/상위_5_도서.xlsx"

# Excel 파일의 시트들을 읽어오기
@st.cache_data
def load_excel_sheets(file_path):
    xls = pd.ExcelFile(file_path)
    sheets = {}
    for sheet_name in xls.sheet_names:
        sheets[sheet_name] = pd.read_excel(xls, sheet_name)
    return sheets

sheets = load_excel_sheets(excel_path)
sheet_names = list(sheets.keys())

# Streamlit 애플리케이션
st.title('연령/성별에 따른 상위 5개 대출 도서')


# 카테고리 선택
selected_category = st.selectbox('카테고리를 선택하세요:', sheet_names)

# 선택한 카테고리의 Excel 데이터 불러오기
df = sheets[selected_category]

# 데이터 프레임 확인
st.write(f'선택한 카테고리: {selected_category}')
st.dataframe(df)

# 데이터 프레임에서 상위 5개 도서와 대출 건수 추출
top_5_books = df.head(5)

# 막대 그래프 생성
fig, ax = plt.subplots(figsize=(10, 6))  # 그래프 크기 조정
ax.bar(top_5_books['도서명'], top_5_books['대출건수'])

# 레이블 회전 및 레이블 간격 조정
ax.set_xlabel('도서명')
ax.set_ylabel('대출건수')
ax.set_title(f'{selected_category} - 상위 5개 도서 대출 건수')

# X축 레이블 회전
plt.xticks(rotation=45, ha='right')

# Streamlit에서 그래프 표시
st.pyplot(fig)
