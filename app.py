import streamlit as st

st.set_page_config(page_title="114汽車二甲畢業檢核", layout="wide")
st.title("🚗 汽車科 113 課綱畢業門檻 - 完整檢核系統")
st.markdown("---")

# 1. 完整科目資料庫 (類別, 性質, 科目名稱, 一上, 一下, 二上, 二下, 三上, 三下, 是否純實習)
if 'courses' not in st.session_state:
    st.session_state.courses = [
        # --- 部定必修 ---
        ['部定必修', '一般', '國語文', 3, 3, 3, 3, 2, 2, False],
        ['部定必修', '一般', '英語文', 2, 2, 2, 2, 2, 2, False],
        ['部定必修', '一般', '數學', 4, 4, 0, 0, 0, 0, False],
        ['部定必修', '一般', '歷史/地理/公民', 2, 2, 2, 0, 0, 0, False],
        ['部定必修', '一般', '物理/化學', 2, 2, 2, 2, 0, 0, False],
        ['部定必修', '一般', '體育', 2, 2, 2, 2, 2, 2, False],
        ['部定必修', '一般', '資訊科技/健康護理', 2, 2, 0, 0, 0, 0, False],
        ['部定必修', '專業', '引擎原理', 0, 0, 3, 0, 0, 0, False],
        ['部定必修', '專業', '底盤原理', 0, 0, 0, 3, 0, 0, False],
        ['部定必修', '專業', '應用力學/機件原理', 0, 0, 2, 3, 0, 0, False],
        ['部定必修', '實習', '機械工作法及實習', 3, 3, 3, 3, 0, 0, True],
        ['部定必修', '實習', '機電製圖實習', 2, 2, 0, 0, 0, 0, True],
        ['部定必修', '實習', '引擎實習', 0, 0, 4, 0, 0, 0, True],
        ['部定必修', '實習', '底盤實習', 0, 0, 0, 4, 0, 0, True],
        ['部定必修', '實習', '電工電子實習', 3, 0, 0, 0, 0, 0, True],
        # --- 校訂必修 ---
        ['校訂必修', '一般', '數學演習/閱讀寫作', 2, 2, 2, 2, 2, 2, False],
        ['校訂必修', '實習', '專題實作', 0, 0, 0, 0, 2, 2, True],
        # --- 校訂選修 ---
        ['校訂選修', '實習', '汽車美容實務', 0, 0, 0, 0, 0, 3, True],
        ['校訂選修', '實習', '噴射引擎實習', 0, 0, 0, 0, 4, 0, True],
        ['校訂選修', '一般', '原住民族語', 0, 0, 2, 2, 2, 2, False],
    ]

# 2. 介面呈現
col_table, col_summary = st.columns([3, 1])

with col_table:
    st.write("### 📝 學分勾選 (及格請打勾)")
    # 表頭顯示
    h = st.columns([2, 1, 1, 1, 1, 1, 1])
    h[0].write("**科目**")
    for idx, name in enumerate(["一", "二", "三", "四", "五", "六"]):
        h[idx+1].write(f"**{name}**")
    
    results = []
    for i, row in enumerate(st.session_state.courses):
        c = st.columns([2, 1, 1, 1, 1, 1, 1])
        c[0].write(f"{row[2]}")
        course_earned = 0
        for s in range(6):
            credit = row[3+s]
            if credit > 0:
                if c[s+1].checkbox(f"{credit}", key=f"k_{i}_{s}"):
                    course_earned += credit
            else:
                c[s+1].write("-")
        results.append({'cat': row[0], 'type': row[1], 'val': course_earned, 'is_pure': row[9]})

with col_summary:
    st.write("### 📊 畢業檢核指標")
    total = sum(r['val'] for r in results)
    dept = sum(r['val'] for r in results if r['cat'] == '部定必修')
    pro_intern = sum(r['val'] for r in results if r['type'] in ['專業', '實習'])
    pure_intern = sum(r['val'] for r in results if r['is_pure'])

    # 顯示指標與顏色提醒
    def metric_box(title, val, target):
        color = "green" if val >= target else "red"
        st.markdown(f"**{title}**")
        st.markdown(f"<h2 style='color:{color}'>{val} / {target}</h2>", unsafe_allow_html=True)
        st.progress(min(val/target, 1.0))

    metric_box("總學分 (>=160)", total, 160)
    metric_box("部定必修 (>=106.3)", dept, 106.3)
    metric_box("專業及實習 (>=60)", pro_intern, 60)
    metric_box("純實習 (>=30)", pure_intern, 30)

    if total >= 160 and dept >= 106.3 and pro_intern >= 60 and pure_intern >= 30:
        st.balloons()
        st.success("✅ 准予畢業！")
