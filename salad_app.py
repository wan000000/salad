import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import calendar
import matplotlib.font_manager as fm

# 日本語フォントの設定
font_path = '/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()

# データフレームの初期化
@st.cache(allow_output_mutation=True)
def get_data():
    return pd.DataFrame(columns=["職員番号", "日付", "摂取グラム数"])

data = get_data()

# ログインセクション
st.title("サラダ摂取量記録アプリ")
employee_id = st.text_input("職員番号を入力してください (6桁)", max_chars=6)

if employee_id:
    st.write(f"職員番号: {employee_id}")

    # 毎日の摂取量記録
    intake = st.number_input("今日のサラダ摂取量 (グラム)", min_value=0)
    record_button = st.button("記録")

    if record_button:
        new_record = {"職員番号": employee_id, "日付": datetime.date.today(), "摂取グラム数": intake}
        data = pd.concat([data, pd.DataFrame([new_record])], ignore_index=True)
        data.to_csv("salad_intake.csv", index=False)
        st.success("記録が追加されました")

    # 月間累計摂取量の表示
    if not data.empty:
        data["日
