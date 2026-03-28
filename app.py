import streamlit as st
import re

# --- 1. 介面樣式 ---
st.set_page_config(page_title="學分檢核系統", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: "Microsoft JhengHei", sans-serif; }
    .main-title { font-size: 2.2rem; font-weight: 800; text-align: center; color: #1e3799; margin-bottom: 2px; }
    .metric-card {
        background-color: #ffffff; padding: 15px; border-radius: 12px;
        border-top: 5px solid #1e3799; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center; margin-bottom: 10px;
    }
    .metric-label { font-size: 0.95rem; color: #576574; font-weight: bold; }
    .metric-value { font-size: 1.6rem; color: #2c3e50; font-weight: 900; margin: 5px 0; }
    .course-card { background-color: #f8f9fa; padding: 10px; border-radius: 8px; border-left: 5px solid #4a69bd; margin-top: 10px; font-weight: bold; }
    .missing-card { color: #e74c3c; background-color: #fff5f5; padding: 8px; border-radius: 6px; margin-bottom: 5px; border-left: 4px solid #e74c3c; font-size: 0.9rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🚗 畢業學分檢核 (113課綱)</p>', unsafe_allow_html=True)

# --- 2. 核心資料庫 ---
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
        ['部定必修', '實習', '機械工作法及實習', 0, 4, 0, 0, 3, 3, True],
        ['校訂必修', '一般', '數學 (校訂必修)', 0, 0, 4, 4, 2, 2, False],
        ['校訂必修', '一般', '青少年身心健康管理', 0, 0, 2, 0, 0, 0, False],
        ['校訂必修', '一般', '計算機概論', 2, 0, 0, 0, 0, 0, False],
        ['校訂選修', '一般', '兵家的智慧', 0, 0, 1, 0, 0, 0, False],
        ['校訂選修', '實習', '汽車檢驗實習', 0, 0, 2, 0, 4, 0, True],
        ['校訂選修', '實習', '車輛微電腦控制實習', 0, 0, 2, 2, 0, 0, True],
    ]

# --- 3. 側邊欄與解析邏輯 ---
with st.sidebar:
    st.subheader("👤 學生檢核")
    st_name = st.text_input("姓名", value="王茂鈞")
    if st.button("🧹 重置勾選"):
        for k in list(st.session_state.keys()):
            if k.startswith("k_"): st.session_state[k] = False
        st.rerun()

with st.expander("📥 第一步：貼上成績文字"):
    paste_txt = st.text_area("請貼上成績文字內容：", height=100)
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
                            if row[3]>0: st.session_state[f"k_{idx}_0"] = True
                            if row[4]>0 and len(scores) >= 2: st.session_state[f"k_{idx}_1"] = True
                        if "二年級" in paste_txt:
                            if row[5]>0: st.session_state[f"k_{idx}_2"] = True
                            if not is_y2_s1_only and row[6]>0 and len(scores) >= 3:
                                st.session_state[f"k_{idx}_3"] = True
            st.rerun()

# --- 4. 數據計算 ---
stats, m1, m2, m3 = [], [], [], []
sem_names = ["一上", "一下", "二上", "二下", "三上", "三下"]
for idx, row in enumerate(st.session_state.courses):
    ev = 0
    for s in range(6):
        if row[3+s] > 0:
            if st.session_state.get(f"k_{idx}_{s}", False): ev += row[3+s]
            else:
                msg = f"{row[2]} ({sem_names[s]})"
                if s < 2: m1.append(msg)
                elif s < 4: m2.append(msg)
                else: m3.append(msg)
    stats.append({'cat': row[0], 'type': row[1], 'val': ev, 'pure': row[9]})

total, dept = sum(x['val'] for x in stats), sum(x['val'] for x in stats if x['cat'] == '部定必修')
prof, prac = sum(x['val'] for x in stats if x['type'] in ['專業', '實習']), sum(x['val'] for x in stats if x['pure'])

# --- 5. 視覺化 Dashboard (置頂) ---
d_cols = st.columns(4)
dash_data = [
    ("🟢 總及格學分", f"{total}/160", total/160),
    ("🔵 部定必修", f"{dept}/106.3", dept/106.3),
    ("🟠 專業與實習", f"{prof}/60", prof/60),
    ("🔴 純實習學分", f"{prac}/30", prac/30)
]
for i, (l, v, p) in enumerate(dash_data):
    with d_cols[i]:
        st.markdown(f'<div class="metric-card"><div class="metric-label">{l}</div><div class="metric-value">{v}</div></div>', unsafe_allow_html=True)
        st.progress(min(p, 1.0))

# --- 6. 未通過學分追蹤 (改為點擊展開，預設關閉) ---
st.markdown("### 🔍 欠修/未及格科目 (點擊展開)")
cm1, cm2, cm3 = st.columns(3)
with cm1:
    with st.expander("高一未過清單", expanded=False): # expanded=False 代表預設收合
        if m1: [st.markdown(f'<div class="missing-card">❌ {x}</div>', unsafe_allow_html=True) for x in m1]
        else: st.success("✅ 全部取得")
with cm2:
    with st.expander("高二未過清單", expanded=False):
        if m2: [st.markdown(f'<div class="missing-card">❌ {x}</div>', unsafe_allow_html=True) for x in m2]
        else: st.success("✅ 全部取得")
with cm3:
    with st.expander("高三預計欠修", expanded=False):
        if m3: [st.markdown(f'<div class="missing-card">⚠️ {x}</div>', unsafe_allow_html=True) for x in m3]
        else: st.success("✅ 預計拿滿")

# --- 7. 分頁勾選區 ---
st.markdown("---")
tabs = st.tabs(["📅 高一", "📅 高二", "📅 高三"])
def render_tab(tab_obj, s_idx):
    with tab_obj:
        cols = st.columns(3)
        current_year_courses = [r for r in st.session_state.courses if r[3+s_idx[0]]>0 or r[3+s_idx[1]]>0]
        for i, row in enumerate(current_year_courses):
            orig_idx = next(idx for idx, r in enumerate(st.session_state.courses) if r[2] == row[2])
            with cols[i % 3]:
                st.markdown(f'<div class="course-card">{row[2]}</div>', unsafe_allow_html=True)
                c1, c2 = row[3+s_idx[0]], row[3+s_idx[1]]
                sub_cols = st.columns(2)
                if c1 > 0: sub_cols[0].checkbox(f"上({c1})", key=f"k_{orig_idx}_{s_idx[0]}")
                if c2 > 0: sub_cols[1].checkbox(f"下({c2})", key=f"k_{orig_idx}_{s_idx[1]}")

render_tab(tabs[0], [0, 1])
render_tab(tabs[1], [2, 3])
render_tab(tabs[2], [4, 5])
