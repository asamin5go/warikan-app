import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="家庭用割り勘", layout="centered")

DATA_FILE = "data.csv"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["who", "amount", "date"])
    df.to_csv(DATA_FILE, index=False)

df = pd.read_csv(DATA_FILE)

st.title("🏠 家庭用 割り勘アプリ")
st.subheader("誰が入力しますか？")

col1, col2 = st.columns(2)
with col1:
    if st.button("アサミが入力"):
        st.session_state["who"] = "アサミ"
with col2:
    if st.button("お母さんが入力"):
        st.session_state["who"] = "お母さん"

if "who" in st.session_state:
    st.divider()
    st.subheader(f"{st.session_state['who']}｜支払い入力")

    amount = st.number_input(
        "💴 支払った金額（円）",
        min_value=0,
        step=1,
        format="%d"
    )

    if st.button("追加する"):
        if amount > 0:
            new_row = {
                "who": st.session_state["who"],
                "amount": amount,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("追加しました！")
        else:
            st.warning("金額を入力してください")

    st.write("📋 入力一覧（最新10件・削除可）")

    st.write("📋 入力一覧（最新10件・削除可）")

recent_df = df.tail(10)

for idx, row in recent_df.iterrows():
    col_who, col_amount, col_date, col_del = st.columns([2, 2, 2, 1])

    with col_who:
        st.write(row["who"])

    with col_amount:
        st.write(f'{int(row["amount"]):,} 円')

    with col_date:
        st.write(row["date"])

    with col_del:
        if st.button("🗑", key=f"trash_{idx}"):
            st.session_state["confirm_delete"] = idx

    # 🔽 確認エリア
    if st.session_state.get("confirm_delete") == idx:
        st.warning("⚠ 本当に削除しますか？")

        col_yes, col_no = st.columns(2)

        with col_yes:
            if st.button("削除する", key=f"yes_{idx}"):
                df = df.drop(idx)
                df.to_csv(DATA_FILE, index=False)
                st.session_state["confirm_delete"] = None
                st.rerun()

        with col_no:
            if st.button("キャンセル", key=f"no_{idx}"):
                st.session_state["confirm_delete"] = None
                st.rerun()



st.divider()
st.subheader("📊 集計結果")

asami_total = df[df["who"] == "アサミ"]["amount"].sum()
mother_total = df[df["who"] == "お母さん"]["amount"].sum()

total = asami_total + mother_total
half = total / 2 if total > 0 else 0

st.write(f"アサミ合計：**{asami_total:,.0f} 円**")
st.write(f"お母さん合計：**{mother_total:,.0f} 円**")

st.markdown("---")
st.write(f"合計：**{total:,.0f} 円**")
st.write(f"1人分：**{half:,.0f} 円**")

diff = asami_total - half

st.markdown("### 👉 結果")
if diff > 0:
    st.success(f"アサミ → お母さんへ\n\n**{diff:,.0f} 円 支払い**")
elif diff < 0:
    st.success(f"お母さん → アサミへ\n\n**{abs(diff):,.0f} 円 支払い**")
else:
    st.info("ちょうど折半です 🎉")
