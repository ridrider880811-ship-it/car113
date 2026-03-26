import streamlit as st

# 1. 頁面配置
st.set_page_config(page_title="汽車科學分檢核系統", layout="wide")

# CSS 樣式設定
st.markdown("""
    <style>
    .stCheckbox { margin-bottom: -15px; }
    .main .block-container { padding-top: 2rem; }
    div[data-testid="stExpander"] { border: 1px solid #ff4b4b; border-radius: 5px; }
    /* 自定義進度條樣式 */
    .stProgress > div > div > div > div {
        background-color: #ff9f43; /* 橘色 (可愛風) */
        background-image: linear-gradient(45deg, rgba(255, 255, 255, .15) 25%, transparent 25%, transparent 50%, rgba(255, 255, 255, .15) 50%, rgba(255, 255, 255, .15) 75%, transparent 75%, transparent);
        background-size: 1rem 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("汽車科學分檢核系統")
st.write("---")

# 側邊欄與登錄資訊
st.sidebar.header("學生登入")
seat_num = st.sidebar.text_input("輸入座號", "01")
student_name = st.sidebar.text_input("輸入姓名", "學生姓名")

st.sidebar.markdown("---")
if st.sidebar.button("🧹 一鍵清空勾選"):
    for key in list(st.session_state.keys()):
        if key.startswith("k_"):
            st.session_state[key] = False
    st.rerun()

# 2. 原始科目資料庫 (共 48 門)
if 'courses' not in st.session_state:
    st.session_state.courses = [
        # --- 部定必修 (一般) ---
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
        # --- 部定必修 (專業/實習) ---
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
        ['校訂選修', '一般', '兵家的智慧', 0, 0, 1, 0, 0, 0, False],
        ['校訂選修', '一般', '野外求生', 0, 0, 0, 1, 0, 0, False],
        ['校訂選修', '一般', '數學演習', 0, 0, 0, 0, 2, 2, False],
        ['校訂選修', '專業', '交通安全與法規', 0, 0, 0, 0, 1, 0, False],
        ['校訂選修', '專業', '汽車新式裝備', 0, 0, 0, 0, 0, 1, False],
        ['校訂選修', '專業', '先進車輛電控概論', 0, 0, 0, 0, 0, 3, False],
        ['校訂選修', '實習', '車輛微電腦控制實習', 0, 0, 2, 2, 0, 0, True],
    ]

# 3. 介面佈局
col_input, col_status = st.columns([2, 1])

with col_input:
    st.write("### 📖 學分勾選 (按學年分頁)")
    t1, t2, t3 = st.tabs(["高一", "高二", "高三"])
    
    checked = {}

    def draw_tab(tab, s_indices, label):
        with tab:
            h = st.columns([3, 1, 1])
            h[0].write("**科目名稱**")
            h[1].write(f"**{label}上**")
            h[2].write(f"**{label}下**")
            for idx, row in enumerate(st.session_state.courses):
                c1, c2 = row[3+s_indices[0]], row[3+s_indices[1]]
                if c1 > 0 or c2 > 0:
                    cols = st.columns([3, 1, 1])
                    cols[0].write(f"{row[2]}")
                    k1, k2 = f"k_{idx}_{s_indices[0]}", f"k_{idx}_{s_indices[1]}"
                    checked[f"{idx}_{s_indices[0]}"] = cols[1].checkbox(f"{c1}", key=k1) if c1 > 0 else False
                    checked[f"{idx}_{s_indices[1]}"] = cols[2].checkbox(f"{c2}", key=k2) if c2 > 0 else False

    draw_tab(t1, [0, 1], "高一")
    draw_tab(t2, [2, 3], "高二")
    draw_tab(t3, [4, 5], "高三")

# 4. 計算與顯示結果
with col_status:
    st.write(f"### 學生：{seat_num} 號 {student_name}")
    
    summary = []
    missing_list = []
    
    for idx, row in enumerate(st.session_state.courses):
        earned = 0
        missing = 0
        for s in range(6):
            c_val = row[3+s]
            if c_val > 0:
                if checked.get(f"{idx}_{s}", False):
                    earned += c_val
                else:
                    missing += c_val
        
        summary.append({'cat': row[0], 'type': row[1], 'val': earned, 'is_pure': row[9]})
        if missing > 0:
            missing_list.append(f"{row[2]} (缺 {missing} 學分)")

    t_val = sum(s['val'] for s in summary)
    d_val = sum(s['val'] for s in summary if s['cat'] == '部定必修')
    p_val = sum(s['val'] for s in summary if s['type'] in ['專業', '實習'])
    s_val = sum(s['val'] for s in summary if s['is_pure'])

    # 顯示指標 (加入進度條)
    def show_m(title, now, target):
        percent = min(now / target, 1.0)
        st.write(f"**{title}**")
        color = "green" if now >= target else "red"
        st.markdown(f"<h3 style='color:{color}; margin:0;'>{now} / {target}</h3>", unsafe_allow_html=True)
        st.progress(percent)
        st.write("")

    st.write("### 📊 畢業檢核看板")
    show_m("1. 總學分 (要超過160學分)", t_val, 160)
    show_m("2. 部定必修 (要超過106.3學分)", d_val, 106.3)
    show_m("3. 專業課目及實習科目 (要超過60學分)", p_val, 60)
    show_m("4. 純實習科目 (要超過30學分)", s_val, 30)

    with st.expander("❌ 待修科目清單", expanded=True):
        if not missing_list:
            st.success("全部科目皆已及格！")
        else:
            for m in missing_list:
                st.write(f"- {m}")

    st.write("---")
    st.write("本系統製作人：羅章成老師")

    if t_val >= 160 and d_val >= 106.3 and p_val >= 60 and s_val >= 30:
        st.balloons()
        st.success("准予畢業！")
