import streamlit as st

# --- 1. 頁面配置 ---
st.set_page_config(page_title="汽車科畢業學分檢核", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: "Microsoft JhengHei", sans-serif; }
    .main-title { font-size: 2.5rem; font-weight: 800; text-align: center; color: #1e3799; margin-bottom: 5px; }
    .stProgress > div > div > div > div { background-color: #38ada9; border-radius: 10px; }
    .course-card { background-color: #ffffff; padding: 10px; border-radius: 8px; border-left: 6px solid #4a69bd; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); margin-top: 10px; font-weight: bold; }
    .metric-container { background-color: #f1f2f6; padding: 15px; border-radius: 10px; border-top: 4px solid #1e3799; }
    .missing-card { color: #eb2f06; background-color: #ffeef0; padding: 8px; border-radius: 6px; margin-bottom: 5px; border-left: 4px solid #eb2f06; font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🚗 汽車科畢業學分檢核系統</p>', unsafe_allow_html=True)
st.caption("<div style='text-align:center;'>製作人：羅章成老師 | 應修總學分：210</div>", unsafe_allow_html=True)

# --- 2. 核心資料庫 (嚴格依照課綱與王茂鈞成績單校對) ---
if 'courses' not in st.session_state:
    st.session_state.courses = [
        # [類別, 屬性, 科目名稱, 一上, 一下, 二上, 二下, 三上, 三下, 是否純實習]
        # 部定必修 一般
        ['部定必修', '一般', '國語文', 3, 3, 3, 3, 2, 2, False],
        ['部定必修', '一般', '英語文', 2, 2, 2, 2, 2, 2, False],
        ['部定必修', '一般', '數學 (部定)', 4, 4, 0, 0, 0, 0, False],
        ['部定必修', '一般', '歷史', 2, 0, 0, 0, 0, 0, False],
        ['部定必修', '一般', '地理', 0, 0, 0, 2, 0, 0, False], 
        ['部定必修', '一般', '公民與社會', 0, 0, 0, 0, 2, 0, False],
        ['部定必修', '一般', '物理', 2, 2, 0, 0, 0, 0, False],
        ['部定必修', '一般', '化學', 0, 2, 0, 0, 0, 0, False],
        ['部定必修', '一般', '音樂', 0, 0, 1, 1, 0, 0, False],      # 茂鈞二上：1
        ['部定必修', '一般', '美術', 2, 0, 0, 0, 0, 0, False],
        ['部定必修', '一般', '法律與生活', 0, 0, 0, 0, 0, 2, False],
        ['部定必修', '一般', '資訊科技', 0, 2, 0, 0, 0, 0, False],
        ['部定必修', '一般', '健康與護理', 0, 2, 0, 0, 0, 0, False],
        ['部定必修', '一般', '體育', 2, 2, 2, 2, 2, 2, False],
        ['部定必修', '一般', '全民國防教育', 1, 1, 0, 0, 0, 0, False],
        ['部定必修', '一般', '本土語/臺灣手語', 0, 0, 0, 2, 0, 0, False],

        # 部定必修 專業/實習
        ['部定必修', '專業', '引擎原理', 3, 0, 0, 0, 0, 0, False],
        ['部定必修', '專業', '底盤原理', 0, 3, 0, 0, 0, 0, False],
        ['部定必修', '專業', '應用力學', 0, 0, 2, 0, 0, 0, False],      # 茂鈞二上：2
        ['部定必修', '專業', '機件原理', 0, 0, 2, 0, 0, 0, False],      # 茂鈞二上：2
        ['部定必修', '實習', '機電製圖實習', 2, 2, 0, 0, 0, 0, True],
        ['部定必修', '實習', '引擎實習', 4, 0, 0, 0, 0, 0, True],
        ['部定必修', '實習', '底盤實習', 0, 0, 4, 4, 0, 0, True],      # 修正：二上4、二下4
        ['部定必修', '實習', '機器腳踏車基礎實習', 3, 0, 0, 0, 0, 0, True],
        ['部定必修', '實習', '機器腳踏車檢修實習', 0, 3, 0, 0, 0, 0, True],
        ['部定必修', '實習', '電工電子實習', 0, 0, 3, 0, 0, 0, True],      # 茂鈞二上：3
        ['部定必修', '實習', '基本電學', 0, 0, 2, 2, 0, 0, True],      # 茂鈞二上：2
        ['部定必修', '實習', '電系實習', 0, 0, 0, 3, 0, 0, True],
        ['部定必修', '實習', '車輛底盤檢修實習', 0, 0, 0, 4, 0, 0, True],
        ['部定必修', '實習', '機械工作法及實習', 0, 4, 0, 0, 3, 3, True],
        ['部定必修', '實習', '車輛空調檢修實習', 0, 0, 0, 0, 3, 0, True],
        ['部定必修', '實習', '車身電器系統綜合檢修實習', 0, 0, 0, 0, 4, 0, True],

        # 校訂必修
        ['校訂必修', '一般', '數學 (校訂必修)', 0, 0, 4, 4, 2, 2, False],   # 茂鈞二上：4
        ['校訂必修', '一般', '青少年身心健康管理', 0, 0, 2, 0, 0, 0, False], # 茂鈞二上：2
        ['校訂必修', '一般', '計算機概論', 2, 0, 0, 0, 0, 0, False],
        ['校訂必修', '一般', '閱讀與寫作', 0, 0, 0, 0, 1, 1, False],
        ['校訂必修', '專業', '汽車工業英文', 0, 0, 0, 0, 0, 2, False],
        ['校訂必修', '專業', '電動車概論', 0, 0, 0, 2, 0, 0, False],
        ['校訂必修', '實習', '專題實作', 0, 0, 0, 0, 2, 2, True],
        ['校訂必修', '實習', '訊號量測與分析實習', 0, 0, 0, 0, 2, 2, True],
        ['校訂必修', '實習', '電動機車實習', 0, 0, 0, 0, 0, 2, True],

        # 校訂選修
        ['校訂選修', '一般', '兵家的智慧', 0, 0, 1, 0, 0, 0, False],      # 茂鈞二上：1
        ['校訂選修', '一般', '野外求生', 0, 0, 0, 1, 0, 0, False],
        ['校訂選修', '一般', '數學演習', 0, 0, 0, 0, 2, 2, False],
        ['校訂選修', '專業', '交通安全與法規', 0, 0, 0, 0, 1, 0, False],
        ['校訂選修', '專業', '汽車新式裝備', 0, 0, 0, 0, 0, 1, False],
        ['校訂選修', '專業', '先進車輛電控概論', 0, 0, 0, 0, 3, 0, False],
        ['校訂選修', '實習', '汽車檢驗實習', 0, 0, 2, 0, 4, 0, True],      # 茂鈞二上：2
        ['校訂選修', '實習', '汽車綜合實習', 0, 0, 0, 0, 4, 0, True],
        ['校訂選修', '實習', '汽車定期保養實習', 0, 0, 0, 0, 4, 0, True],
        ['校訂選修', '實習', '汽車塗裝實習', 0, 0, 0, 0, 4, 0, True],
        ['校訂選修', '實習', '車輛儀器檢修實務', 0, 0, 0, 0, 0, 3, True],
        ['校訂選修', '實習', '汽車美容實務', 0, 0, 0, 0, 0, 3, True],
        ['校訂選修', '實習', '車輪定位檢修實習', 0, 0, 0, 0, 0, 4, True],
        ['校訂選修', '實習', '噴射引擎實習', 0, 0, 0, 0, 0, 4, True],
        ['校訂選修', '實習', '柴油引擎實習', 0, 0, 0, 0, 0, 4, True],
        ['校訂選修', '實習', '車輛微電腦控制實習', 0, 0, 2, 2, 0, 0, True], # 茂鈞二上：2
        ['校訂選修', '一般', '原住民族語課程', 0, 0, 2, 2, 2, 2, False],
    ]

# --- 3. 解析功能 (精準過濾二下) ---
with st.sidebar:
    st_name = st.text_input("座號 / 姓名", value="王茂鈞")
    if st.button("🧹 清空勾選"):
        for k in list(st.session_state.keys()):
            if k.startswith("k_"): st.session_state[k] = False
        st.rerun()

with st.expander("📥 貼上成績文字自動勾選"):
    paste_txt = st.text_area("在此貼上文字：", height=150)
    if st.button("🚀 執行自動勾選"):
        if paste_txt:
            y1, y2, y3 = "一年級" in paste_txt, "二年級" in paste_txt, "三年級" in paste_txt
            # 關鍵：若文字內沒有出現「下學期」成績數字，就不勾選下學期
            has_s2_data = "下學期" in paste_txt and "必修" in paste_txt.split("下學期")[1]
            
            lines = paste_txt.split('\n')
            for line in lines:
                for idx, row in enumerate(st.session_state.courses):
                    if row[2][:2] in line:
                        if y1:
                            if row[3]>0: st.session_state[f"k_{idx}_0"] = True
                            if row[4]>0: st.session_state[f"k_{idx}_1"] = True
                        if y2:
                            if row[5]>0: st.session_state[f"k_{idx}_2"] = True
                            # 只有文字確實包含二下成績才勾
                            if has_s2_data and row[6]>0: st.session_state[f"k_{idx}_3"] = True
            st.rerun()

tabs = st.tabs(["📅 高一階段", "📅 高二階段", "📅 高三階段"])
def render_year(tab_obj, s_idx):
    with tab_obj:
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
st.markdown("---")
st.subheader("📊 畢業門檻達成檢測")
stats, m1, m2, m3 = [], [], [], []
sem_names = ["一上", "一下", "二上", "二下", "三上", "三下"]
for idx, row in enumerate(st.session_state.courses):
    ev = 0
    for s in range(6):
        if row[3+s] > 0:
            if st.session_state.get(f"k_{idx}_{s}", False): ev += row[3+s]
            else:
                msg = f"❌ {row[2]} ({sem_names[s]})"
                if s < 2: m1.append(msg)
                elif s < 4: m2.append(msg)
                else: m3.append(msg)
    stats.append({'cat': row[0], 'type': row[1], 'val': ev, 'pure': row[9]})

total, dept = sum(x['val'] for x in stats), sum(x['val'] for x in stats if x['cat'] == '部定必修')
prof, prac = sum(x['val'] for x in stats if x['type'] in ['專業', '實習']), sum(x['val'] for x in stats if x['pure'])

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("總學分", f"{total} / 160"); st.progress(min(total/160, 1.0)); st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("部定必修", f"{dept} / 106.3"); st.progress(min(dept/106.3, 1.0)); st.markdown('</div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("專業實習", f"{prof} / 60"); st.progress(min(prof/60, 1.0)); st.markdown('</div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.metric("純實習", f"{prac} / 30"); st.progress(min(prac/30, 1.0)); st.markdown('</div>', unsafe_allow_html=True)

st.markdown("### 🔍 未取得學分清單")
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    with st.expander("📅 一年級缺修", expanded=True):
        if m1: 
            for m in m1: st.markdown(f'<div class="missing-card">{m}</div>', unsafe_allow_html=True)
        else: st.write("✅ 已拿滿")
with col_m2:
    with st.expander("📅 二年級缺修", expanded=True):
        if m2:
            for m in m2: st.markdown(f'<div class="missing-card">{m}</div>', unsafe_allow_html=True)
        else: st.write("✅ 已拿滿")
with col_m3:
    with st.expander("📅 三年級缺修", expanded=True):
        if m3:
            for m in m3: st.markdown(f'<div class="missing-card">{m}</div>', unsafe_allow_html=True)
        else: st.write("✅ 已拿滿")
