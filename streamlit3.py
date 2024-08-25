import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import streamlit as st

# 폰트 파일 경로 설정
font_path = r'C:\Windows\Fonts\Hancom Gothic Regular.ttf'
font_prop = fm.FontProperties(fname=font_path, size=12)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# 데이터 로드
file_path = r'C:\Users\user\Desktop\도서관_공모전\최종\book_analysis_final.xlsx'
df = pd.read_excel(file_path, sheet_name=2)

# 연령대 문자열 처리
df['연령대'] = df['연령'].astype(str)

# 장르별 대출 건수 집계
genre_age_sex = df.groupby(['연령대', '성별', '주제분류명'])['대출건수'].sum().unstack().fillna(0)

# 상위 3개의 주제분류명 추출
top_genres = df.groupby(['연령대', '성별', '주제분류명'])['대출건수'].sum().reset_index()
top_genres = top_genres.sort_values(by=['연령대', '성별', '대출건수'], ascending=[True, True, False])

# 각 연령대와 성별별로 상위 3개의 주제분류명을 추출
top_3_genres = top_genres.groupby(['연령대', '성별']).head(3).reset_index(drop=True)

# Streamlit 애플리케이션 설정
st.title('연령/성별에 따른 상위 장르')

# 선택 박스 생성
selected_age_group = st.selectbox('연령대를 선택하세요:', df['연령대'].unique())
selected_gender = st.selectbox('성별을 선택하세요:', df['성별'].unique())

# 선택된 카테고리에 해당하는 데이터 필터링
filtered_data = top_3_genres[(top_3_genres['연령대'] == selected_age_group) & (top_3_genres['성별'] == selected_gender)]

# 상위 3개의 주제분류명 시각화
if not filtered_data.empty:
    st.subheader(f'{selected_age_group} - {selected_gender}의 상위 3 장르')

    plt.figure(figsize=(10, 6))
    sns.barplot(data=filtered_data, x='주제분류명', y='대출건수', palette='viridis')
    plt.title(f'{selected_age_group} - {selected_gender}의 상위 3 장르')
    plt.xlabel('주제분류명')
    plt.ylabel('대출건수')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)
else:
    st.write('선택된 연령대와 성별에 대한 데이터가 없습니다.')

# 상위 3개의 주제분류명 엑셀로 저장 (추가 옵션)
if st.button('상위 3 장르 엑셀로 저장'):
    excel_path = r'C:\Users\user\Desktop\상위_3_장르.xlsx'
    top_3_genres.to_excel(excel_path, index=False)
    st.write(f'엑셀 파일이 저장되었습니다: {excel_path}')
