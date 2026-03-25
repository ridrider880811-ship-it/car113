import streamlit as st
import pandas as pd

# 網頁基本設定
st.set_page_config(page_title="114汽車二甲-畢業門檻檢核", layout="wide")
st.title("🚗 汽車科 113 課綱畢業門檻自動檢核系統")
st.markdown("---")

# 1. 核心資料庫 (依據您的 Excel 結構)
if 'courses' not in st.session_state:
    st.session_state.courses = [
        # 類別, 性質, 科目名稱, 一上, 一下, 二上, 二下, 三上, 三下, 是否實習
        ['部定必修', '一般', '國語文', 3, 3, 3, 3, 2, 2, False],
        ['部定必修', '一般', '英語文', 2, 2, 2, 2, 2, 2, False],
        ['部定必修', '一般', '數學', 4, 4, 0, 0, 0, 0, False],
        ['部定必修', '專業', '引擎原理', 0, 0, 3, 0, 0, 0, False],
        ['部定必修', '實習', '機械工作法及實習', 3, 3, 3, 3, 0, 0, True],
        ['部定必修', '實習', '引擎實習', 0, 0, 4, 0, 0, 0, True],
        ['校訂必修', '一般', '數學演習', 0, 0, 2, 2, 2, 2, False],
        ['校訂必修', '實習', '專題實作', 0, 0, 0, 0, 2, 2, True],
        ['校訂選修', '實習', '汽車美容實務', 0, 0, 0, 0, 0, 3, True],
        ['校訂選修', '一般', '原住民族語課程', 0, 0, 2, 2, 2, 2, False],
    ]

# 2. 介面佈局
col_table, col_summary = st.columns([3, 1])

with col_table:
    st.write("### 📖 學分勾選區 (及格請打勾)")
    
    # 建立表頭
    header = st.columns([2, 1, 1, 1, 1, 1, 1, 1, 1])
    header[0].write("**科目名稱**")
    sems = ["一上", "一下", "二上", "二下", "三上", "三下"]
    for idx, sem in enumerate(sems):
        header[idx+1].write(f"**{sem}**")
    
    earned_data = []

    # 產生每一列的勾選框
    for i, row in enumerate(st.session_state.courses):
        cols = st.columns([2, 1, 1, 1, 1, 1, 1, 1, 1])
        cols[0].write(f"{row[2]}")
        
        course_earned = 0
        for s_idx in range(6):
            base_credit = row[3 + s_idx]
            if base_credit > 0:
                # 這裡模擬 Excel 的 1/0 勾選
                if cols[s_idx+1].checkbox(f"{base_credit}", key=f"c_{i}_{s_idx}"):
                    course_earned += base_credit
            else:
                cols[s_idx+1].write("-")
        
        # 儲存這一門課最後得到的學分資訊
        earned_data.append({
            '類別': row[0],
            '性質': row[1],
            '學分': course_earned,
            '是否實習': row[9]
        })

with col_summary:
    st.write("### 📊 畢業門檻即時檢核")
    
    # 計算各項指標
    total_earned = sum(item['學分'] for item in earned_data)
    dept_earned = sum(item['學分'] for item in earned_data if item['類別'] == '部定必修')
    pro_intern_earned = sum(item['學分'] for item in earned_data if item['性質'] in ['專業', '實習'])
    pure_intern_earned = sum(item['學分'] for item in earned_data if item['是否實習'])

    # 顯示結果儀表板
    def show_status(label, val, target):
        st.write(f"**{label}**")
        color = "green" if val >= target else "red"
        st.markdown(f"<h2 style='color: {color};'>{val} / {target}</h2>", unsafe_allow_html=True)
        st.progress(min(val/target, 1.0))

    show_status("1. 總學分 (>=160)", total_earned, 160)
    show_status("2. 部定必修 (>=106.3)", dept_earned, 106.3)
    show_status("3. 專業及實習 (>=60)", pro_intern_earned, 60)
    show_status("4. 純實習科目 (>=30)", pure_intern_earned, 30)

    if total_earned >= 160 and dept_earned >= 106.3 and pro_intern_earned >= 60 and pure_intern_earned >= 30:
        st.balloons()
        st.success("🎓 准予畢業！")
    else:
        st.warning("⚠️ 尚未達成畢業門檻")
