import streamlit as st

# --- 1. 頁面配置 ---
st.set_page_config(page_title="汽車科學分檢核 Pro", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: "Microsoft JhengHei", sans-serif; }
    .main-title { font-size: 2.2rem; font-weight: 800; text-align: center; color: #1e3799; }
    .metric-card { background-color: #ffffff; padding: 15px; border-radius: 12px; border-top: 5px solid #1e3799; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; margin-bottom: 15px; }
    .metric-value { font-size: 1.5rem; color: #2c3e50; font-weight: 900; }
    .course-card { background-color: #f8f9fa; padding: 10px; border-radius: 8px; border-left: 5px solid #4a69bd; margin-top: 10px; font-weight: bold; }
    div[data-testid="stCheckbox"] { background-color: #f1f5f9; padding: 5px 10px; border-radius: 5px; border: 1px solid #cbd5e1; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🚗 汽車科畢業檢核系統 Pro</p>', unsafe_allow_html=True)
st.caption("<div style='text-align:center;'>製作人：羅章成老師 | 113課綱精確對位版</div>", unsafe_allow_html=True)

# --- 2. 核心資料庫 (58科完整版) ---
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
        ['校訂選修', '實習', '汽車定期保養實習', 0, 0, 0, 0, 4, 0, True],
        ['校訂選修', '實習', '噴射引擎實習', 0, 0, 0, 0, 0, 4, True],
        ['校訂選修', '實習', '汽車美容實務', 0, 0, 0, 0, 0, 3, True],
        ['校訂選修', '實習', '車輛微電腦控制實習', 0, 0, 2, 2, 0, 0, True],
        ['校訂選修', '一般', '原住民族語課程', 0, 0, 2, 2, 2, 2, False],
    ]

# --- 3. 側邊欄 ---
with st.sidebar:
    st_name = st.text_input("座號/姓名", value="")
    if st.button("🧹 重置所有勾選"):
        for k in list(st.session_state.keys()):
            if k.startswith("k_"): st.session_state[k] = False
        st.rerun()

# --- 4. 偵測引擎 (回歸成功定位邏輯) ---
with st.expander("📥 貼上成績文字自動偵測"):
    paste_txt = st.text_area("在此貼上內容：", height=100)
    if st.button("🚀 開始分析"):
        if paste_txt:
            # 強力攔截：只要看到實得學分 13 0 或 32 0，就禁止勾二下
            txt_cl = paste_txt.replace(" ","").replace("\xa0","")
            is_y2_s1_only = "二年級" in paste_txt and ("實得學分130" in txt_cl or "實得學分320" in txt_cl)
            
            lines = paste_txt.split('\n')
            for line in lines:
                l = line.replace(" ","").replace("\xa0","")
                for idx, row in enumerate(st.session_state.courses):
                    subj = row[2][:2]
                    if subj in l:
                        # 王茂鈞版最強邏輯：只要該科目及格（出現在文字裡且及格），就勾選
                        # 林浩宇特別過濾：只有科目後面的數字 >= 60 才算過
                        # 我們搜尋 "必修" 或 "選修" 之後緊接的數字
                        import re
                        scores = re.findall(r"(?:必修|選修)\d(\d{1,3})", l)
                        
                        if "一年級" in paste_txt:
                            if row[3]>0 and len(scores)>=1 and int(scores[0])>=60:
                                st.session_state[f"k_{idx}_0"] = True
                            if row[4]>0 and len(scores)>=2 and int(scores[1])>=60:
                                st.session_state[f"k_{idx}_1"] = True
                        
                        if "二年級" in paste_txt:
                            if row[5]>0 and len(scores)>=1 and int(scores[0])>=60:
                                st.session_state[f"k_{idx}_2"] = True
                            # 關鍵：二下必須在「非攔截狀態」下才能勾
                            if not is_y2_s1_only and row[6]>0 and len(scores)>=2 and int(scores[1])>=60:
                                st.session_state[f"k_{idx}_3"] = True
            st.rerun()

# --- 5. 分頁渲染 (統一 Key) ---
tabs = st.tabs(["📅 高一階段", "📅 高二階段", "📅 高三階段"])
def render_tab(tab_obj, s_idx):
    with tab_obj:
        cols = st.columns(3)
        year_courses = [r for r in st.session_state.courses if r[3+s_idx[0]] > 0 or r[3+s_idx[1]] > 0]
        for i, row in enumerate(year_courses):
            orig_idx = next(idx for idx, r in enumerate(st.session_state.courses) if r[2] == row[2])
            with cols[i % 3]:
                st.markdown(f'<div class="course-card">{row[2]}</div>', unsafe_allow_html=True)
                c1, c2 = row[3+s_idx[0]], row[3+s_idx[1]]
                sub_cols = st.columns(2)
                if c1 > 0: sub_cols[0].checkbox(f"上學期({c1})", key=f"k_{orig_idx}_{s_idx[0]}")
                if c2 > 0: sub_cols[1].checkbox(f"下學期({c2})", key=f"k_{orig_idx}_{s_idx[1]}")

render_tab(tabs[0], [0, 1])
render_tab(tabs[1], [2, 3])
render_tab(tabs[2], [4, 5])

# --- 6. 統計看板 ---
st.markdown("---")
stats, m1, m2, m3 = [], [], [], []
sem_names = ["一上", "一下", "二上", "二下", "三上", "三下"]
for idx, row in enumerate(st.session_state.courses):
    ev = 0
    for s in range(6):
        if row[3+s] > 0:
            if st.session_state.get(f"k_{idx}_{s}", False):
                ev += row[3+s]
            else:
                msg = f"{row[2]}({sem_names[s]})"
                if s < 2: m1.append(msg)
                elif s < 4: m2.append(msg)
                else: m3.append(msg)
    stats.append({'cat': row[0], 'type': row[1], 'val': ev, 'pure': row[9]})

total = sum(x['val'] for x in stats)
dept = sum(x['val'] for x in stats if x['cat'] == '部定必修')
prof = sum(x['val'] for x in stats if x['type'] in ['專業', '實習'])
prac = sum(x['val'] for x in stats if x['pure'])

d_cols = st.columns(4)
dash = [("總學分", total, 160), ("部定必修", dept, 106.3), ("專業與實習", prof, 60), ("純實習", prac, 30)]
for i, (l, curr, tar) in enumerate(dash):
    with d_cols[i]:
        st.markdown(f'<div class="metric-card"><div>{l}</div><div class="metric-value">{curr}/{tar}</div></div>', unsafe_allow_html=True)
        st.progress(min(curr/tar, 1.0))

st.markdown("### 🔍 缺修科目清單")
cm1, cm2, cm3 = st.columns(3)
with cm1:
    with st.expander("高一缺修", False):
        if m1: [st.markdown(f'<div style="color:red;">❌ {x}</div>', unsafe_allow_html=True) for x in m1]
        else: st.success("已達標")
with cm2:
    with st.expander("高二缺修", False):
        if m2: [st.markdown(f'<div style="color:red;">❌ {x}</div>', unsafe_allow_html=True) for x in m2]
        else: st.success("已達標")
with cm3:
    with st.expander("高三缺修", False):
        if m3: [st.markdown(f'<div style="color:orange;">⚠️ {x}</div>', unsafe_allow_html=True) for x in m3]
        else: st.success("已達標")
