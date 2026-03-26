import streamlit as st

# 1. 頁面配置
st.set_page_config(page_title="汽車科學分檢核系統", layout="wide")

# 手機版面優化 CSS
st.markdown("""
    <style>
    /* 縮小手機端間距 */
    .stCheckbox { margin-bottom: -18px; }
    .main .block-container { padding-top: 1rem; padding-left: 1rem; padding-right: 1rem; }
    
    /* 進度條可愛風樣式 */
    .stProgress > div > div > div > div {
        background-color: #ff9f43; 
        background-image: linear-gradient(45deg, rgba(255, 255, 255, .2) 25%, transparent 25%, transparent 50%, rgba(255, 255, 255, .2) 50%, rgba(255, 255, 255, .2) 75%, transparent 75%, transparent);
        background-size: 1rem 1rem;
    }

    /* 調整字體大小以符合手機閱讀 */
    @media (max-width: 640px) {
        .stMarkdown div p { font-size: 14px; }
        h3 { font-size: 18px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚗 汽車科學分檢核系統")
st.subheader("加油，一定能順利畢業的！")
st.caption("製作人：羅章成老師")
st.write("---")

# 側邊欄：學生資訊
st.sidebar.header("👤 學生登入")
seat_num = st.sidebar.text_input("座號", "01")
student_name = st.sidebar.text_input("姓名", "學生姓名")

if st.sidebar.button("🧹 一鍵清空勾選"):
    for key in list(st.session_state.keys()):
        if key.startswith("k_"):
            st.session_state[key] = False
    st.rerun()

# 2. 原始科目資料庫 (48 門)
sem_names = ["一上", "一下", "二上", "二下", "三上", "三下"]
if 'courses' not in st.session_state:
    st.session_state.courses = [
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
        ['校訂必修', '一般', '青少年身心健康管理', 0, 2, 0, 0, 0, 0, False],
        ['校訂必修', '一般', '數學', 0, 0, 4, 4, 0, 0, False],
        ['校訂必修', '一般', '閱讀與寫作', 0, 0, 0, 0, 1, 1, False],
        ['校訂必修', '一般', '計算機概論', 2, 0, 0, 0, 0, 0, False],
        ['校訂必修', '專業', '電動車概論', 0, 0, 0, 2, 0, 0, False],
        ['校訂必修', '專業', '汽車工業英文', 0, 0, 0, 0, 0, 2, False],
        ['校訂必修', '實習', '電動機車實習', 0, 0, 0, 0, 2, 0, True],
        ['校訂必修', '實習', '專題實作', 0, 0, 0, 0, 2, 2, True],
        ['校訂必修', '實習', '訊號量測與分析實習', 0, 0, 0, 0, 0, 2, True],
        ['校訂選修', '一般', '兵家的智慧', 0, 0, 1, 0, 0, 0, False],
        ['校訂選修', '一般', '野外求生', 0, 0, 0, 1, 0, 0, False],
        ['校訂選修', '一般', '數學演習', 0, 0, 0, 0, 2, 2, False],
        ['校訂選修', '專業', '交通安全與法規', 0, 0, 0, 0, 1, 0, False],
        ['校訂選修', '專業', '汽車新式裝備', 0, 0, 0, 0, 0, 1, False],
        ['校訂選修', '專業', '先進車輛電控概論', 0, 0, 0, 0, 0, 3, False],
        ['校訂選修', '實習', '車輛微電腦控制實習', 0, 0, 2, 2, 0, 0, True],
    ]

# 3. 介面佈局
col_input, col_status = st.columns([1.6, 1.4])

checked = {}
with col_input:
    st.subheader("📖 學分勾選區")
    tabs = st.tabs(["高一", "高二", "高三"])
    
    def draw_semester(tab_obj, s_indices, label):
        with tab_obj:
            h = st.columns([2.5, 1, 1])
            h[0].write("**科目**")
            h[1].write("**上**")
            h[2].write("**下**")
            for idx, row in enumerate(st.session_state.courses):
                c1, c2 = row[3+s_indices[0]], row[3+s_indices[1]]
                if c1 > 0 or c2 > 0:
                    cols = st.columns([2.5, 1, 1])
                    cols[0].write(f"{row[2]}")
                    k1, k2 = f"k_{idx}_{s_indices[0]}", f"k_{idx}_{s_indices[1]}"
                    checked[f"{idx}_{s_indices[0]}"] = cols[1].checkbox(f"{c1}", key=k1) if c1 > 0 else False
                    checked[f"{idx}_{s_indices[1]}"] = cols[2].checkbox(f"{c2}", key=k2) if c2 > 0 else False

    draw_semester(tabs[0], [0, 1], "高一")
    draw_semester(tabs[1], [2, 3], "高二")
    draw_semester(tabs[2], [4, 5], "高三")

# 4. 計算與顯示結果
with col_status:
    st.subheader(f"📊 {seat_num}號 {student_name}")
    
    summary = []
    missing_by_year = { "📍 一年級": [], "📍 二年級": [], "📍 三年級": [] }
    
    for idx, row in enumerate(st.session_state.courses):
        earned_row = 0
        for s in range(6):
            c_val = row[3+s]
            if c_val > 0:
                if checked.get(f"{idx}_{s}", False):
                    earned_row += c_val
                else:
                    year_key = "📍 一年級" if s < 2 else ("📍 二年級" if s < 4 else "📍 三年級")
                    missing_by_year[year_key].append(f"{sem_names[s]} {row[2]} ({c_val})")
        
        summary.append({'cat': row[0], 'type': row[1], 'val': earned_row, 'is_pure': row[9]})

    # 指標計算
    t_sum = sum(s['val'] for s in summary)
    d_sum = sum(s['val'] for s in summary if s['cat'] == '部定必修')
    p_sum = sum(s['val'] for s in summary if s['type'] in ['專業', '實習'])
    s_sum = sum(s['val'] for s in summary if s['is_pure'])

    def show_progress(title, now, target):
        st.write(f"**{title}**")
        color = "#27ae60" if now >= target else "#e74c3c"
        st.markdown(f"<h3 style='color:{color}; margin:0;'>{now} / {target}</h3>", unsafe_allow_html=True)
        st.progress(min(now / target, 1.0))
        st.write("")

    st.write("### 畢業進度看板")
    show_progress("1. 總學分 (>=160)", t_sum, 160)
    show_progress("2. 部定必修 (>=106.3)", d_sum, 106.3)
    show_progress("3. 專業及實習 (>=60)", p_sum, 60)
    show_progress("4. 純實習科目 (>=30)", s_sum, 30)

    st.write("### ❌ 待修科目明細 (點開查看)")
    for year, items in missing_by_year.items():
        with st.expander(f"{year} (剩餘 {len(items)} 門)", expanded=False):
            if not items:
                st.success("✅ 本學年科目已全數及格！")
            else:
                for item in items:
                    st.write(f"• {item}")

    st.write("---")
    st.write("本系統製作人：羅章成老師")

    if t_sum >= 160 and d_sum >= 106.3 and p_sum >= 60 and s_sum >= 30:
        st.balloons()
        st.success("🏁 恭喜！您已達成所有畢業門檻！")
