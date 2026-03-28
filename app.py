import streamlit as st

# --- 1. 頁面配置 ---
st.set_page_config(page_title="畢業學分清單", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: "Microsoft JhengHei", sans-serif; }
    .main-title { font-size: 2.2rem; font-weight: 800; text-align: center; color: #2c3e50; }
    .stProgress > div > div > div > div { background-color: #ff9f43; border-radius: 10px; }
    .course-card { background-color: #f8f9fa; padding: 8px 12px; border-radius: 5px; border-left: 5px solid #3498db; margin-top: 10px; font-weight: bold; }
    .missing-card { color: #e74c3c; background-color: #fff5f5; padding: 5px; border-radius: 4px; margin-bottom: 3px; border-left: 3px solid #e74c3c; font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🚗 畢業學分清單</p>', unsafe_allow_html=True)
st.caption("製作人：羅章成老師")

# --- 2. 核心資料庫 (嚴格校對 113 課綱全科目) ---
if 'courses' not in st.session_state:
    st.session_state.courses = [
        # --- 部定必修 一般科目 (PDF 第1頁) ---
        ['部定必修', '一般', '國語文', 3, 3, 3, 3, 2, 2, False],
        ['部定必修', '一般', '英語文', 2, 2, 2, 2, 2, 2, False],
        ['部定必修', '一般', '數學 (部定)', 4, 4, 0, 0, 0, 0, False],
        ['部定必修', '一般', '歷史', 2, 0, 0, 0, 0, 0, False],
        ['部定必修', '一般', '地理', 0, 2, 0, 0, 0, 0, False],
        ['部定必修', '一般', '公民與社會', 0, 0, 0, 0, 2, 0, False],
        ['部定必修', '一般', '物理', 2, 2, 0, 0, 0, 0, False], # 參照王茂鈞成績
        ['部定必修', '一般', '化學', 0, 2, 0, 0, 0, 0, False], # 參照王茂鈞成績
        ['部定必修', '一般', '音樂', 0, 0, 1, 1, 0, 0, False],
        ['部定必修', '一般', '美術', 2, 0, 0, 0, 0, 0, False],
        ['部定必修', '一般', '法律與生活', 0, 0, 0, 0, 0, 2, False],
        ['部定必修', '一般', '資訊科技', 0, 2, 0, 0, 0, 0, False],
        ['部定必修', '一般', '健康與護理', 0, 2, 0, 0, 0, 0, False], # 參照王茂鈞成績
        ['部定必修', '一般', '體育', 2, 2, 2, 2, 2, 2, False],
        ['部定必修', '一般', '全民國防教育', 1, 1, 0, 0, 0, 0, False],
        ['部定必修', '一般', '本土語/臺灣手語', 0, 0, 0, 2, 0, 0, False],
        
        # --- 部定必修 專業/實習 ---
        ['部定必修', '專業', '引擎原理', 3, 0, 0, 0, 0, 0, False],
        ['部定必修', '專業', '底盤原理', 0, 3, 0, 0, 0, 0, False],
        ['部定必修', '專業', '應用力學', 0, 0, 2, 0, 0, 0, False],
        ['部定必修', '專業', '機件原理', 0, 0, 2, 0, 0, 0, False],
        ['部定必修', '實習', '機電製圖實習', 2, 2, 0, 0, 0, 0, True],
        ['部定必修', '實習', '引擎實習', 4, 0, 0, 0, 0, 0, True],
        ['部定必修', '實習', '底盤實習', 0, 4, 4, 0, 0, 0, True],
        ['部定必修', '實習', '電工電子實習', 0, 0, 3, 0, 0, 0, True],
        ['部定必修', '實習', '機器腳踏車基礎實習', 3, 0, 0, 0, 0, 0, True],
        ['部定必修', '實習', '機器腳踏車檢修實習', 0, 3, 0, 0, 0, 0, True],
        ['部定必修', '實習', '電系實習', 0, 0, 0, 3, 0, 0, True],
        ['部定必修', '實習', '車輛底盤檢修實習', 0, 0, 0, 4, 0, 0, True],
        ['部定必修', '實習', '機械工作法及實習', 0, 4, 0, 0, 3, 3, True],
        ['部定必修', '實習', '車輛空調檢修實習', 0, 0, 0, 0, 3, 0, True],
        ['部定必修', '實習', '車身電器系統綜合檢修實習', 0, 0, 0, 0, 4, 0, True],

        # --- 校訂必修 (PDF 第4-5頁) ---
        ['校訂必修', '一般', '數學 (校訂必修)', 0, 0, 4, 4, 0, 0, False], # 王茂鈞格式 4+4
        ['校訂必修', '一般', '青少年身心健康管理', 0, 0, 2, 0, 0, 0, False],
        ['校訂必修', '一般', '計算機概論', 0, 2, 0, 0, 0, 0, False],
        ['校訂必修', '一般', '閱讀與寫作', 0, 0, 0, 0, 1, 1, False],
        ['校訂必修', '專業', '汽車工業英文', 0, 0, 0, 0, 0, 2, False],
        ['校訂必修', '專業', '電動車概論', 0, 0, 0, 2, 0, 0, False],
        ['校訂必修', '實習', '專題實作', 0, 0, 0, 0, 2, 2, True],
        ['校訂必修', '實習', '訊號量測與分析實習', 0, 0, 0, 0, 2, 2, True],
        ['校訂必修', '實習', '電動機車實習', 0, 0, 0, 0, 0, 2, True],

        # --- 校訂選修 (PDF 第6頁 - 全科目補回) ---
        ['校訂選修', '一般', '兵家的智慧', 0, 0, 1, 0, 0, 0, False],
        ['校訂選修', '一般', '野外求生', 0, 0, 0, 1, 0, 0, False],
        ['校訂選修', '一般', '數學演習', 0, 0, 0, 0, 2, 2, False],
        ['校訂選修', '專業', '交通安全與法規', 0, 0, 0, 0, 1, 0, False],
        ['校訂選修', '專業', '汽車新式裝備', 0, 0, 0, 0, 0, 1, False],
        ['校訂選修', '專業', '先進車輛電控概論', 0, 0, 0, 0, 3, 0, False],
        ['校訂選修', '實習', '汽車檢驗實習', 0, 0, 2, 0, 4, 0, True], # 參照茂鈞成績
        ['校訂選修', '實習', '汽車綜合實習', 0, 0, 0, 0, 4, 0, True],
        ['校訂選修', '實習', '汽車定期保養實習', 0, 0, 0, 0, 4, 0, True],
        ['校訂選修', '實習', '汽車塗裝實習', 0, 0, 0, 0, 4, 0, True],
        ['校訂選修', '實習', '車輛儀器檢修實務', 0, 0, 0, 0, 0, 3, True],
        ['校訂選修', '實習', '汽車美容實務', 0, 0, 0, 0, 0, 3, True],
        ['校訂選修', '實習', '車輪定位檢修實習', 0, 0, 0, 0, 0, 4, True],
        ['校訂選修', '實習', '噴射引擎實習', 0, 0, 0, 0, 0, 4, True],
        ['校訂選修', '實習', '柴油引擎實習', 0, 0, 0, 0, 0, 4, True],
        ['校訂選修', '實習', '車輛微電腦控制實習', 0, 0, 2, 2, 0, 0, True],
        ['校訂選修', '一般', '原住民族語課程', 0, 0, 2, 2, 2, 2, False],
    ]

# --- 3. UI 與功能 ---
with st.sidebar:
    st_info = st.text_input("座號 / 姓名", placeholder="王茂鈞")
    if st.button("🧹 清空"):
        for k in list(st.session_state.keys()):
            if k.startswith("k_"): st.session_state[k] = False
        st.rerun()

with st.expander("📥 貼上成績文字"):
    paste_txt = st.text_area("在此貼上文字：", height=150)
    if st.button("🚀 執行解析"):
        if paste_txt:
            is_y1 = "一年級" in paste_txt
            is_y2 = "二年級" in paste_txt
            for line in paste_txt.split('\n'):
                for idx, row in enumerate(st.session_state.courses):
                    if row[2][:2] in line:
                        if is_y1:
                            if row[3]>0: st.session_state[f"k_{idx}_0"] = True
                            if row[4]>0: st.session_state[f"k_{idx}_1"] = True
                        if is_y2:
                            if row[5]>0: st.session_state[f"k_{idx}_2"] = True
                            if row[6]>0: st.session_state[f"k_{idx}_3"] = True
            st.rerun()

tabs = st.tabs(["高一", "高二", "高三"])
sem_names = ["一上", "一下", "二上", "二下", "三上", "三下"]

def render_year(tab, s_idx):
    with tab:
        for idx, row in enumerate(st.session_state.courses):
            c1, c2 = row[3+s_idx[0]], row[3+s_idx[1]]
            if c1 > 0 or c2 > 0:
                st.markdown(f'<div class="course-card">{row[2]}</div>', unsafe_allow_html=True)
                cols = st.columns(2)
                k1, k2 = f"k_{idx}_{s_idx[0]}", f"k_{idx}_{s_idx[1]}"
                if c1 > 0: cols[0].checkbox(f"上({c1})", key=k1)
                if c2 > 0: cols[1].checkbox(f"下({c2})", key=k2)

render_year(tabs[0], [0, 1])
render_year(tabs[1], [2, 3])
render_year(tabs[2], [4, 5])

# --- 4. 統計 ---
stats = []
unpassed = []
for idx, row in enumerate(st.session_state.courses):
    ev = 0
    for s in range(6):
        if row[3+s] > 0:
            if st.session_state.get(f"k_{idx}_{s}", False): ev += row[3+s]
            else: unpassed.append(f"{row[2]} ({sem_names[s]})")
    stats.append({'cat': row[0], 'type': row[1], 'val': ev, 'pure': row[9]})

t_s = sum(x['val'] for x in stats)
d_s = sum(x['val'] for x in stats if x['cat'] == '部定必修')
p_s = sum(x['val'] for x in stats if x['type'] in ['專業', '實習'])
s_s = sum(x['val'] for x in stats if x['pure'])

c_l, c_r = st.columns(2)
with c_l:
    st.write(f"**總學分: {t_s} / 160**"); st.progress(min(t_s/160, 1.0))
    st.write(f"**部定必修: {d_s} / 106.3**"); st.progress(min(d_s/106.3, 1.0))
with c_r:
    st.write(f"**專業實習: {p_s} / 60**"); st.progress(min(p_s/60, 1.0))
    st.write(f"**純實習: {s_s} / 30**"); st.progress(min(s_s/30, 1.0))

with st.expander("🔍 未取得學分清單"):
    for item in unpassed: st.markdown(f'<div class="missing-card">❌ {item}</div>', unsafe_allow_html=True)
