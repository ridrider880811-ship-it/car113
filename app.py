import streamlit as st
import re

# --- 1. 頁面配置與樣式 ---
st.set_page_config(page_title="汽車科學分檢核 Pro", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: "Microsoft JhengHei", sans-serif; }
    .main-title { font-size: 2.2rem; font-weight: 800; text-align: center; color: #1e3799; margin-bottom: 5px; }
    .metric-card {
        background-color: #ffffff; padding: 15px; border-radius: 12px;
        border-top: 5px solid #1e3799; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center; margin-bottom: 15px; min-height: 110px;
    }
    .metric-label { font-size: 0.9rem; color: #576574; font-weight: bold; }
    .metric-value { font-size: 1.4rem; color: #2c3e50; font-weight: 900; margin: 5px 0; }
    .metric-diff { font-size: 0.8rem; font-weight: bold; padding: 2px 8px; border-radius: 10px; }
    .diff-red { color: #e74c3c; background-color: #fff5f5; }
    .diff-green { color: #27ae60; background-color: #f0fff4; }
    div[data-testid="stCheckbox"] { background-color: #f8fafc; padding: 8px 12px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 8px; }
    .course-card { background-color: #f1f5f9; padding: 8px; border-radius: 8px; border-left: 5px solid #1e3799; margin-top: 10px; font-weight: bold; font-size: 0.95rem; }
    .missing-card { color: #e74c3c; background-color: #fff5f5; padding: 8px; border-radius: 6px; margin-bottom: 5px; border-left: 4px solid #e74c3c; font-size: 0.85rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🚗 汽車科畢業檢核系統 Pro</p>', unsafe_allow_html=True)
st.caption("<div style='text-align:center;'>製作人：羅章成老師 | 113課綱精確對位版</div>", unsafe_allow_html=True)

# --- 2. 核心資料庫 (鎖定 210 學分配置) ---
if 'courses' not in st.session_state:
    st.session_state.courses = [
        ['部定必修', '一般', '國語文', 3, 3, 3, 3, 2, 2, False],
        ['部定必修', '一般', '英語文', 2, 2, 2, 2, 2, 2, False],
        ['部定必修', '一般', '數學 (部定)', 4, 4, 0, 0, 0, 0, False],
        ['部定必修', '一般', '歷史', 2, 0, 0, 0, 0, 0, False],
        ['部定必修', '一般', '地理', 0, 0, 0, 2, 0, 0, False], 
        ['部定必修', '一般', '公民與社會', 0, 0, 0, 0, 2, 0, False],
        ['部定必修', '一般', '物理', 2, 2, 0, 0, 0, 0, False],
        ['部定必修', '一般', '化學', 0, 2, 0, 0, 0, 0, False],
        ['部定必修', '一般', '音樂', 0, 0, 1, 1, 0, 0, False],
        ['部定必修', '一般', '美術', 2, 0, 0, 0, 0, 0, False],
        ['部定必修', '一般', '法律與生活', 0, 0, 0, 0, 0, 2, False],
        ['部定必修', '一般', '資訊科技', 0, 2, 0, 0, 0, 0, False],
        ['部定必修', '一般', '健康與護理', 0, 2, 0, 0, 0, 0, False],
        ['部定必修', '一般', '體育', 2, 2, 2, 2, 2, 2, False],
        ['部定必修', '一般', '全民國防教育', 1, 1, 0, 0, 0, 0, False],
        ['部定必修', '一般', '本土語/臺灣手語', 0, 0, 0, 2, 0, 0, False],
        ['部定必修', '專業', '引擎原理', 3, 0, 0, 0, 0, 0, False],
        ['部定必修', '專業', '底盤原理', 0, 3, 0, 0, 0, 0, False],
        ['部定必修', '專業', '應用力學', 0, 0, 2, 0, 0, 0, False],
        ['部定必修', '專業', '機件原理', 0, 0, 2, 0, 0, 0, False],
        ['部定必修', '實習', '機電製圖實習', 2, 2, 0, 0, 0, 0, True],
        ['部定必修', '實習', '引擎實習', 4, 0, 0, 0, 0, 0, True],
        ['部定必修', '實習', '底盤實習', 0, 0, 4, 4, 0, 0, True],
        ['部定必修', '實習', '機器腳踏車基礎實習', 3, 0, 0, 0, 0, 0, True],
        ['部定必修', '實習', '機器腳踏車檢修實習', 0, 3, 0, 0, 0, 0, True],
        ['部定必修', '實習', '電工電子實習', 0, 0, 3, 0, 0, 0, True],
        ['部定必修', '實習', '基本電學', 0, 0, 2, 2, 0, 0, True],
        ['部定必修', '實習', '電系實習', 0, 0, 0, 3, 0, 0, True],
        ['部定必修', '實習', '車輛底盤檢修實習', 0, 0, 0, 4, 0, 0, True],
        ['部定必修', '實習', '機械工作法及實習', 0, 4, 0, 0, 3, 3, True],
        ['部定必修', '實習', '車輛空調檢修實習', 0, 0, 0, 0, 3, 0, True],
        ['部定必修', '實習', '車身電器系統綜合檢修實習', 0, 0, 0, 0, 4, 0, True],
        ['校訂必修', '一般', '數學 (校訂必修)', 0, 0, 4, 4, 2, 2, False],
        ['校訂必修', '一般', '青少年身心健康管理', 0, 0, 2, 0, 0, 0, False],
        ['校訂必修', '一般', '計算機概論', 2, 0, 0, 0, 0, 0, False],
        ['校訂必修', '一般', '閱讀與寫作', 0, 0, 0, 0, 1, 1, False],
        ['校訂必修', '專業', '汽車工業英文', 0, 0, 0, 0, 0, 2, False],
        ['校訂必修', '專業', '電動車概論', 0, 0, 0, 2, 0, 0, False],
        ['校訂必修', '實習', '專題實作', 0, 0, 0, 0, 2, 2, True],
        ['校訂必修', '實習', '訊號量測與分析實習', 0, 0, 0, 0, 2, 2, True],
        ['校訂必修', '實習', '電動機車實習', 0, 0, 0, 0, 0, 2, True],
        ['校訂選修', '一般', '兵家的智慧', 0, 0, 1, 0, 0, 0, False],
        ['校訂選修', '一般', '野外求生', 0, 0, 0, 1, 0, 0, False],
        ['校訂選修', '一般', '數學演習', 0, 0, 0, 0, 2, 2, False],
        ['校訂選修', '專業', '交通安全與法規', 0, 0, 0, 0, 1, 0, False],
        ['校訂選修', '專業', '汽車新式裝備', 0, 0, 0, 0, 0, 1, False],
        ['校訂選修', '專業', '先進車輛電控概論', 0, 0, 0, 0, 3, 0, False],
        ['校訂選修', '實習', '汽車檢驗實習', 0, 0, 2, 0, 4, 0, True],
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

# --- 3. 側邊欄 (手機版功能回歸) ---
with st.sidebar:
    st_name = st.text_input("座號/姓名", value="")
    if st.button("🧹 重置勾選"):
        for k in list(st.session_state.keys()):
            if k.startswith("k_"): st.session_state[k] = False
        st.rerun()
    is_mobile = st.checkbox("📱 手機版檢視(單欄)", value=False) # 功能補回

with st.expander("📥 貼上成績文字自動偵測"):
    paste_txt = st.text_area("在此貼上內容：", height=100)
    if st.button("🚀 開始偵測"):
        if paste_txt:
            clean_txt = re.sub(r'\s+', ' ', paste_txt)
            is_y2_s1_only = "二年級" in clean_txt and ("實得學分 32 0" in clean_txt or "實得學分320" in clean_txt.replace(" ",""))
            lines = paste_txt.split('\n')
            for line in lines:
                clean_l = line.replace(" ", "").replace("\xa0", "")
                for idx, row in enumerate(st.session_state.courses):
                    if row[2][:2] in clean_l:
                        scores = re.findall(r"(?<!\d)(?:[4-9]\d|100)(?!\d)", clean_l)
                        if "一年級" in paste_txt:
                            if row[3]>0: st.session_state[f"k_{idx}_0_Y1"] = True
                            if row[4]>0 and len(scores) >= 2: st.session_state[f"k_{idx}_1_Y1"] = True
                        if "二年級" in paste_txt:
                            if row[5]>0: st.session_state[f"k_{idx}_2_Y2"] = True
                            if not is_y2_s1_only and row[6]>0 and len(scores) >= 3:
                                st.session_state[f"k_{idx}_3_Y2"] = True
            st.rerun()

# --- 4. 分頁渲染 (整合單欄檢視邏輯) ---
tabs = st.tabs(["📅 高一", "📅 高二", "📅 高三"])
def render_tab(tab_obj, s_idx, year_label):
    with tab_obj:
        num_cols = 1 if is_mobile else 3 # 響應式欄位
        cols = st.columns(num_cols)
        year_courses = [r for r in st.session_state.courses if r[3+s_idx[0]] > 0 or r[3+s_idx[1]] > 0]
        for i, row in enumerate(year_courses):
            orig_idx = next(idx for idx, r in enumerate(st.session_state.courses) if r[2] == row[2])
            with cols[i % num_cols]:
                st.markdown(f'<div class="course-card">{row[2]}</div>', unsafe_allow_html=True)
                c1, c2 = row[3+s_idx[0]], row[3+s_idx[1]]
                sub_cols = st.columns(2)
                if c1 > 0: sub_cols[0].checkbox(f"上({c1})", key=f"k_{orig_idx}_{s_idx[0]}_{year_label}")
                if c2 > 0: sub_cols[1].checkbox(f"下({c2})", key=f"k_{orig_idx}_{s_idx[1]}_{year_label}")

render_tab(tabs[0], [0, 1], "Y1")
render_tab(tabs[1], [2, 3], "Y2")
render_tab(tabs[2], [4, 5], "Y3")

# --- 5. 數據看板與警告 ---
st.markdown("---")
stats, m1, m2, m3 = [], [], [], []
sem_names = ["一上", "一下", "二上", "二下", "三上", "三下"]
for idx, row in enumerate(st.session_state.courses):
    ev = 0
    for s in range(6):
        y_tag = "Y1" if s < 2 else ("Y2" if s < 4 else "Y3")
        if row[3+s] > 0:
            if st.session_state.get(f"k_{idx}_{s}_{y_tag}", False): ev += row[3+s]
            else:
                msg = f"{row[2]} ({sem_names[s]})"
                if s < 2: m1.append(msg)
                elif s < 4: m2.append(msg)
                else: m3.append(msg)
    stats.append({'cat': row[0], 'type': row[1], 'val': ev, 'pure': row[9]})

total, dept = sum(x['val'] for x in stats), sum(x['val'] for x in stats if x['cat'] == '部定必修')
prof, prac = sum(x['val'] for x in stats if x['type'] in ['專業', '實習']), sum(x['val'] for x in stats if x['pure'])

d_cols = st.columns(4)
dash = [("🟢 總及格學分", total, 160), ("🔵 部定必修", dept, 106.3), ("🟠 專業與實習", prof, 60), ("🔴 純實習學分", prac, 30)]
for i, (l, curr, tar) in enumerate(dash):
    diff = tar - curr
    diff_html = f'<span class="metric-diff diff-red">還差 {diff:.1f}</span>' if diff > 0 else '<span class="metric-diff diff-green">已達標</span>'
    with d_cols[i]:
        st.markdown(f'<div class="metric-card"><div class="metric-label">{l}</div><div class="metric-value">{curr}/{tar}</div><div>{diff_html}</div></div>', unsafe_allow_html=True)
        st.progress(min(curr/tar, 1.0))

st.markdown("### 🔍 欠修/未及格科目")
cm1, cm2, cm3 = st.columns(3)
with cm1:
    with st.expander(f"{'🔴' if m1 else '🟢'} 一年級", False):
        if m1: [st.markdown(f'<div class="missing-card">❌ {x}</div>', unsafe_allow_html=True) for x in m1]
        else: st.success("學分已全數取得")
with cm2:
    with st.expander(f"{'🔴' if m2 else '🟢'} 二年級", False):
        if m2: [st.markdown(f'<div class="missing-card">❌ {x}</div>', unsafe_allow_html=True) for x in m2]
        else: st.success("學分已全數取得")
with cm3:
    with st.expander(f"{'🔴' if m3 else '🟢'} 三年級", False):
        if m3: [st.markdown(f'<div class="missing-card">⚠️ {x}</div>', unsafe_allow_html=True) for x in m3]
        else: st.success("預計將拿滿學分")
