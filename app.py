import streamlit as st
import re

# --- 1. 頁面配置 ---
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
    .year-summary {
        background-color: #f8fafc; padding: 12px; border-radius: 8px;
        border-left: 5px solid #1e3799; font-weight: bold; text-align: center; margin-bottom: 10px; font-size: 1.1rem; color: #1e293b;
    }
    .metric-value { font-size: 1.5rem; color: #2c3e50; font-weight: 900; }
    div[data-testid="stCheckbox"] { background-color: #f8fafc; padding: 8px 12px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 8px; }
    .course-card { background-color: #f1f5f9; padding: 8px; border-radius: 8px; border-left: 5px solid #1e3799; margin-top: 10px; font-weight: bold; }
    .missing-card { color: #e74c3c; background-color: #fff5f5; padding: 8px; border-radius: 6px; margin-bottom: 5px; border-left: 4px solid #e74c3c; font-size: 0.85rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🚗 汽車科畢業檢核系統 Pro</p>', unsafe_allow_html=True)
st.caption("<div style='text-align:center;'>製作人：羅章成老師 | 113課綱精確對位版</div>", unsafe_allow_html=True)

# --- 2. 核心資料庫 (二下無基本電學，括號完全閉合) ---
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
        ['部定必修', '實習', '基本電學', 0, 0, 2, 0, 0, 0, True],
        ['部定必修', '實習', '機械工作法及實習', 0, 4, 0, 0, 3, 3, True],
        ['校訂必修', '一般', '數學 (校訂必修)', 0, 0, 4, 4, 2, 2, False],
        ['校訂必修', '一般', '青少年身心健康管理', 0, 0, 2, 0, 0, 0, False],
        ['校訂必修', '一般', '計算機概論', 2, 0, 0, 0, 0, 0, False],
        ['校訂必修', '一般', '閱讀與寫作', 0, 0, 0, 0, 1, 1, False],
        ['校訂選修', '一般', '兵家的智慧', 0, 0, 1, 0, 0, 0, False],
        ['校訂選修', '一般', '數學演習', 0, 0, 0, 0, 2, 2, False],
        ['校訂選修', '實習', '汽車檢驗實習', 0, 0, 2, 0, 4, 0, True],
        ['校訂選修', '實習', '汽車定期保養實習', 0, 0, 0, 0, 4, 0, True],
        ['校訂選修', '實習', '噴射引擎實習', 0, 0, 0, 0, 0, 4, True],
        ['校訂選修', '實習', '車輛微電腦控制實習', 0, 0, 2, 2, 0, 0, True],
        ['校訂選修', '一般', '原住民族語課程', 0, 0, 2, 2, 2, 2, False],
    ]

# --- 3. 側邊欄 (座號姓名回歸) ---
with st.sidebar:
    st.markdown("### 📋 學生基本資料")
    st_name = st.text_input("座號 / 姓名", value="", placeholder="例如：15號 林浩宇")
    if st.button("🧹 徹底重置所有勾選"):
        for k in list(st.session_state.keys()):
            if k.startswith("k_"): st.session_state[k] = False
        st.rerun()
    is_mobile = st.checkbox("📱 手機版檢視(單欄)", value=False)

# --- 4. 偵測引擎 (林浩宇數據鋼鐵攔截) ---
with st.expander("📥 貼上成績文字自動偵測"):
    paste_txt = st.text_area("在此貼上內容：", height=120)
    if st.button("🚀 執行精準分析"):
        if paste_txt:
            txt_cl = paste_txt.replace(" ","").replace("\xa0","")
            # 零值攔截特徵 (13 0 或 32 0)
            is_y2_s1_only = "二年級" in paste_txt and ("實得學分130" in txt_cl or "實得學分320" in txt_cl)
            
            lines = paste_txt.split('\n')
            for line in lines:
                l_raw = line.replace(" ","").replace("\xa0","")
                if not l_raw: continue
                
                for idx, row in enumerate(st.session_state.courses):
                    if row[2][:2] in l_raw:
                        # 依照「必修/選修」切開區塊
                        parts = re.split(r'必修|選修', l_raw)
                        
                        # 處理第一學期 (零件 1)
                        if len(parts) > 1:
                            # 規則：跳過學分(第1位)，抓成績(第2位起)
                            score_m = re.search(r'^\d(\d{1,3})', parts[1])
                            if score_m and int(score_m.group(1)) >= 60:
                                if "一年級" in paste_txt and row[3] > 0: st.session_state[f"k_{idx}_0"] = True
                                if "二年級" in paste_txt and row[5] > 0: st.session_state[f"k_{idx}_2"] = True
                        
                        # 處理第二學期 (零件 2) - 過攔截器
                        if not is_y2_s1_only and len(parts) > 2:
                            score_m_down = re.search(r'^\d(\d{1,3})', parts[2])
                            if score_m_down and int(score_m_down.group(1)) >= 60:
                                if "一年級" in paste_txt and row[4] > 0: st.session_state[f"k_{idx}_1"] = True
                                if "二年級" in paste_txt and row[6] > 0: st.session_state[f"k_{idx}_3"] = True
            st.rerun()

# --- 5. 分頁渲染 ---
tabs = st.tabs(["📅 高一階段", "📅 高二階段", "📅 高三階段"])
def render_tab(tab_obj, s_idx):
    with tab_obj:
        num_cols = 1 if is_mobile else 3
        cols = st.columns(num_cols)
        year_courses = [r for r in st.session_state.courses if r[3+s_idx[0]] > 0 or r[3+s_idx[1]] > 0]
        for i, row in enumerate(year_courses):
            orig_idx = next(idx for idx, r in enumerate(st.session_state.courses) if r[2] == row[2])
            with cols[i % num_cols]:
                st.markdown(f'<div class="course-card">{row[2]}</div>', unsafe_allow_html=True)
                c1, c2 = row[3+s_idx[0]], row[3+s_idx[1]]
                sub_cols = st.columns(2)
                if c1 > 0: sub_cols[0].checkbox(f"上({c1})", key=f"k_{orig_idx}_{s_idx[0]}")
                if c2 > 0: sub_cols[1].checkbox(f"下({c2})", key=f"k_{orig_idx}_{s_idx[1]}")

render_tab(tabs[0], [0, 1])
render_tab(tabs[1], [2, 3])
render_tab(tabs[2], [4, 5])

# --- 6. 統計儀表板 (新增學年統計與門檻看板) ---
st.markdown("---")
stats, m1, m2, m3 = [], [], [], []
y1_t, y2_t, y3_t = 0, 0, 0
sem_names = ["一上", "一下", "二上", "二下", "三上", "三下"]

for idx, row in enumerate(st.session_state.courses):
    ev = 0
    for s in range(6):
        if row[3+s] > 0:
            if st.session_state.get(f"k_{idx}_{s}", False):
                credit = row[3+s]
                ev += credit
                if s < 2: y1_t += credit
                elif s < 4: y2_t += credit
                else: y3_t += credit
            else:
                msg = f"{row[2]}({sem_names[s]})"
                if s < 2: m1.append(msg)
                elif s < 4: m2.append(msg)
                else: m3.append(msg)
    stats.append({'cat': row[0], 'type': row[1], 'val': ev, 'pure': row[9]})

st.markdown("### 📅 學年實得學分累計")
sy1, sy2, sy3 = st.columns(3)
sy1.markdown(f'<div class="year-summary">一年級：{y1_t} 學分</div>', unsafe_allow_html=True)
sy2.markdown(f'<div class="year-summary">二年級：{y2_t} 學分</div>', unsafe_allow_html=True)
sy3.markdown(f'<div class="year-summary">三年級：{y3_t} 學分</div>', unsafe_allow_html=True)

total, dept = sum(x['val'] for x in stats), sum(x['val'] for x in stats if x['cat'] == '部定必修')
prof, prac = sum(x['val'] for x in stats if x['type'] in ['專業', '實習']), sum(x['val'] for x in stats if x['pure'])

d_cols = st.columns(4)
dash = [("🟢 總及格", total, 160), ("🔵 部定必修", dept, 106.3), ("🟠 專業實習", prof, 60), ("🔴 純實習學分", prac, 30)]
for i, (l, curr, tar) in enumerate(dash):
    diff = tar - curr
    diff_html = f'<span style="color:red; font-size:0.8rem;">缺{diff:.1f}</span>' if diff > 0 else '<span style="color:green; font-size:0.8rem;">達標</span>'
    with d_cols[i]:
        st.markdown(f'<div class="metric-card"><div>{l}</div><div class="metric-value">{curr}/{tar}</div>{diff_html}</div>', unsafe_allow_html=True)
        st.progress(min(curr/tar, 1.0))

st.markdown("### 🔍 缺修名單")
cm1, cm2, cm3 = st.columns(3)
with cm1:
    with st.expander("高一缺修", False):
        if m1: [st.markdown(f'<div class="missing-card">❌ {x}</div>', unsafe_allow_html=True) for x in m1]
        else: st.success("已全過")
with cm2:
    with st.expander("高二缺修", False):
        if m2: [st.markdown(f'<div class="missing-card">❌ {x}</div>', unsafe_allow_html=True) for x in m2]
        else: st.success("已全過")
with cm3:
    with st.expander("高三預計", False):
        if m3: [st.markdown(f'<div class="missing-card">⚠️ {x}</div>', unsafe_allow_html=True) for x in m3]
        else: st.success("預計全過")
