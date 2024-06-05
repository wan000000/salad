import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

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
        data = data.append(new_record, ignore_index=True)
        data.to_csv("salad_intake.csv", index=False)
        st.success("記録が追加されました")

    # 月間累計摂取量の表示
    if not data.empty:
        data["日付"] = pd.to_datetime(data["日付"])
        monthly_data = data[data["職員番号"] == employee_id].groupby(data["日付"].dt.to_period("M")).sum()

        st.write("月間累計摂取量")
        st.bar_chart(monthly_data["摂取グラム数"])

    # カレンダー表示
    st.write("摂取日カレンダー")
    calendar = data[data["職員番号"] == employee_id].set_index("日付").resample("D").sum()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(calendar.index, calendar["摂取グラム数"], marker='o', linestyle='-')
    ax.set_title("サラダ摂取量")
    ax.set_xlabel("日付")
    ax.set_ylabel("摂取グラム数")
    st.pyplot(fig)

    # ランキング表示
    st.write("月間サラダ摂取量ランキング")
    monthly_rank = data.groupby(["職員番号", data["日付"].dt.to_period("M")]).sum().reset_index()
    monthly_rank = monthly_rank.groupby("職員番号").sum().sort_values(by="摂取グラム数", ascending=False)
    st.write(monthly_rank)
