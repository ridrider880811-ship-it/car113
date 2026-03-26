import streamlit as st

st.set_page_config(page_title="114汽車二甲畢業檢核", layout="wide")
st.title("🚗 汽車科 113 課綱畢業門檻 - 專業檢核系統")
st.info("請對照成績單，在及格的學分空格打勾。系統會自動計算四大畢業門檻。")

# 1. 完整科目資料庫：嚴格依照 Excel 表格順序
# 格式：[類別, 性質, 科目名稱, 一上, 一下, 二上, 二下, 三上, 三下, 是否純實習]
if 'courses' not in st.session_state:
    st.session_state.courses = [
        # --- 部定必修 (一般科目) ---
        ['部定必修', '一般', '國語文', 3, 3, 3, 3, 2, 2, False],
        ['部定必修', '一般', '英語文', 2, 2, 2, 2, 2, 2, False],
        ['部定必修', '一般', '數學', 4, 4, 0, 0, 0, 0, False],
        ['部定必修', '一般', '歷史', 2, 0, 0, 0, 0, 0, False],
        ['部定必修', '一般', '地理', 0, 0, 0, 2, 0, 0, False],
        ['部定必修', '一般', '公民與社會', 0, 0, 0, 0, 2, 0, False],
        ['部定必修', '一般', '法律與生活', 0, 0, 0, 0, 0, 2, False],
        ['部定必修', '一般', '物理', 2, 2, 0, 0, 0, 0, False],
        ['部定必修', '一般', '化學', 0, 2, 0, 0, 0, 0, False],
        ['部定必修', '一般', '音樂', 0, 0, 1, 1, 0, 0, False],
        ['部定必修', '一般', '美術', 2, 0, 0, 0, 0, 0, False],
        ['部定必修', '一般', '資訊科技', 0, 2, 0, 0, 0, 0, False],
        ['部定必修', '一般', '健康與護理', 2, 0, 0, 0, 0, 0, False],
        ['部定必修', '一般', '體育', 2, 2, 2, 2, 2, 2, False],
        ['部定必修', '一般', '全民國防教育', 1, 1, 0, 0, 0, 0, False],
        ['部定必修', '一般', '本土語/台灣手語', 0, 0, 0, 2, 0, 0, False],
        # --- 部定必修 (專業/實習科目) ---
        ['部定必修', '專業', '應用力學', 0, 0, 2, 0, 0, 0, False],
        ['部定必修', '專業', '機件原理', 0, 0, 2, 0, 0, 0, False],
        ['部定必修', '專業', '引擎原理', 3, 0, 0, 0, 0, 0, False],
        ['部定必修', '專業', '底盤原理', 0, 3, 0, 0, 0, 0, False],
        ['部定必修', '專業', '基本電學', 0, 0, 2, 0, 0, 0, False],
        ['部定必修', '實習', '機械工作法及實習', 0, 4, 0, 0, 0, 0, True],
        ['部定必修', '實習', '機電製圖實習', 2, 2, 0, 0, 0, 0, True],
        ['部定必修', '實習', '引擎實習', 0, 0, 4, 0, 0, 0, True],
        ['部定必修', '實習', '底盤實習', 0, 0, 3, 0, 0, 0, True],
        ['部定必修', '實習', '電系實習', 0, 0, 0, 3, 0, 0, True],
        ['部定必修', '實習', '電工電子實習', 0, 0, 3, 0, 0, 0, True],
        ['部定必修', '實習', '車輛空調檢修實習', 0, 0, 0, 0, 3, 0, True],
        ['部定必修', '實習', '車輛底盤檢修實習', 0, 0, 0, 4, 0, 0, True],
        ['部定必修', '實習', '車身電器系統綜合檢修實習', 0, 0, 0, 0, 4, 0, True],
        ['部定必修', '實習', '機器腳踏車基礎實習', 3, 0, 0, 0, 0, 0, True],
        ['部定必修', '實習', '機器腳踏車檢修實習', 0, 3, 0, 0, 0, 0, True],
        # --- 校訂必修 ---
        ['校訂必修', '一般', '青少年身心健康管理', 0, 2, 0, 0, 0, 0, False],
        ['校訂必修', '一般', '數學', 0, 0, 4, 4, 0, 0, False],
        ['校訂必修', '一般', '閱讀與寫作', 0, 0, 0, 0, 1, 1, False],
        ['校訂必修', '一般', '計算機概論', 2, 0, 0, 0, 0, 0, False],
        ['校訂必修', '專業', '電動車概論', 0, 0, 0, 2, 0, 0, False],
        ['校訂必修', '專業', '汽車工業英文', 0, 0, 0, 0, 0, 2, False],
        ['校訂必修', '實習', '電動機車實習', 0, 0, 0, 0, 2, 0, True],
        ['校訂必修', '實習', '專題實作', 0, 0, 0, 0, 2, 2, True],
        ['校訂必修', '實習', '訊號量測與分析實習', 0, 0, 0, 0, 0, 2, True],
        # --- 校訂選修 ---
        ['校訂選修', '一般', '兵家的智慧', 0, 0, 1, 0, 0, 0, False]
        ['校訂選修', '一般', '兵家的智慧', 0, 0, 0, 1, 0, 0, False]
        ['校訂選修', '一般', '數學演習', 0, 0, 0, 0, 2, 2, False]
        ['校訂選修', '專業', '交通安全與法規', 0, 0, 0, 0, 1, 0, False],
        ['校訂選修', '專業', '汽車新式裝備', 0, 0, 0, 0, 0, 1, False],
        ['校訂選修', '專業', '先進車輛電控概論', 0, 0, 0, 0, 0, 3, False],
        ['校訂選修', '實習', '車輛微電腦控制實習', 0, 0, 2, 2, 0, 0, True],

        
    ]

# 2. 顯示與計算邏輯
col_main, col_res = st.columns([3, 1])

with col_main:
    st.write("### 📂 課程學分清單")
    # 建立表頭
    h = st.columns([2, 1, 1, 1, 1, 1, 1])
    h[0].write("**科目名稱**")
    for i, name in enumerate(["一上", "一下", "二上", "二下", "三上", "三下"]):
        h[i+1].write(f"**{name}**")
    
    final_stats = []
    for row_idx, row in enumerate(st.session_state.courses):
        cols = st.columns([2, 1, 1, 1, 1, 1, 1])
        cols[0].write(f"{row[2]}") # 科目名
        
        row_total = 0
        for s in range(6):
            credit = row[3+s]
            if credit > 0:
                # 每個勾選框代表該學期的學分
                if cols[s+1].checkbox(f"{credit}", key=f"c_{row_idx}_{s}"):
                    row_total += credit
            else:
                cols[s+1].write("-")
        
        final_stats.append({'cat': row[0], 'type': row[1], 'credit': row_total, 'is_pure': row[9]})

with col_res:
    st.write("### 📊 畢業檢核")
    # 計算各項數值
    t_val = sum(x['credit'] for x in final_stats)
    d_val = sum(x['credit'] for x in final_stats if x['cat'] == '部定必修')
    p_val = sum(x['credit'] for x in final_stats if x['type'] in ['專業', '實習'])
    s_val = sum(x['credit'] for x in final_stats if x['is_pure'])

    def show_metric(name, val, target):
        st.write(f"**{name}**")
        color = "green" if val >= target else "red"
        st.markdown(f"<h3 style='color:{color}'>{val} / {target}</h3>", unsafe_allow_html=True)
        st.progress(min(val/target, 1.0))

    show_metric("1. 總學分 (>=160)", t_val, 160)
    show_metric("2. 部定必修 (>=106)", d_val, 106.3) # 125 * 85%
    show_metric("3. 專業及實習 (>=60)", p_val, 60)
    show_metric("4. 純實習 (>=30)", s_val, 30)

    if t_val >= 160 and d_val >= 106.3 and p_val >= 60 and s_val >= 30:
        st.balloons()
        st.success("🎉 恭喜畢業！")
