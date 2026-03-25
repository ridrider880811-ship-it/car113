import streamlit as st

st.set_page_config(page_title="114汽車二甲學分檢核", layout="wide")
st.title("🚗 汽車科 113 課綱學分檢核系統")
st.write("---")

# 畢業門檻設定 [cite: 1]
courses = [
    ['部定必修', '一般', '國語文', 16, False],
    ['部定必修', '一般', '英語文', 12, False],
    ['部定必修', '一般', '數學', 8, False],
    ['部定必修', '實習', '機械工作法及實習', 12, True],
    ['部定必修', '實習', '引擎實習', 4, True],
    ['校訂必修', '實習', '專題實作', 4, True],
    ['校訂選修', '實習', '汽車美容', 3, True],
    ['校訂選修', '一般', '原住民族語課程', 4, False],
]

col1, col2 = st.columns([2, 1])
with col1:
    st.write("### 📝 勾選已取得學分科目")
    selected = [c for c in courses if st.checkbox(f"{c[2]} ({c[3]}學分)", key=c[2])]

with col2:
    st.write("### 📊 畢業資格檢核")
    total = sum(c[3] for c in selected)
    dept = sum(c[3] for c in selected if c[0] == '部定必修')
    pure_intern = sum(c[3] for c in selected if c[4])
    
    # 顯示指標 [cite: 1]
    st.metric("總學分 (門檻 160)", f"{total} / 160")
    st.metric("部定必修 (門檻 106.3)", f"{dept} / 106.3")
    st.metric("純實習科目 (門檻 30)", f"{pure_intern} / 30")

    if total >= 160 and dept >= 106.3 and pure_intern >= 30:
        st.balloons()
        st.success("🎉 符合畢業資格！")
