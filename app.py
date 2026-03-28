import streamlit as st

# --- 1. 頁面基礎配置 ---
st.set_page_config(page_title="汽車科學分檢核系統", layout="wide")

# CSS 樣式：手機與電腦版排版區隔
st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: "Microsoft JhengHei", sans-serif; }
    .main-title { font-size: 2.2rem; font-weight: 800; text-align: center; color: #2c3e50; margin-bottom: 0px; }
    .stProgress > div > div > div > div { background-color: #ff9f43; border-radius: 10px; }
    @media (max-width: 768px) {
        .main-title { font-size: 1.5rem; }
        .stCheckbox { font-size: 0.9rem; margin-bottom: 8px !important; }
        div[data-testid="column"] { width: 48% !important; flex: 1 1 45% !important; }
    }
    .course-card { background-color: #f8f9fa; padding: 8px 12px; border-radius: 5px; border-left: 5px solid #3498db; margin-top: 15px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🚗 汽車科學分檢核系統</p>', unsafe_allow_html=True)
st.caption("製作人：羅章成老師 | 114 級汽車二甲專用精確版")

# --- 2. 核心資料庫 (嚴格校對數學與所有學分數) ---
if 'courses' not in st.session_state:
    st.session_state.courses = [
        # [類別, 屬性, 科目名稱, 一上, 一下, 二上, 二下, 三上, 三下, 是否純實習]
        ['部定必修', '一般', '國語文', 3, 3, 3, 3, 2, 2, False],
        ['部定必修', '一般', '英語文', 2, 2, 2, 2, 2, 2, False],
        ['部定必修', '一般', '數學', 4, 4, 0, 0, 0, 0, False], # 高一數學
        ['部定必修', '一般', '歷史', 2, 0, 0, 0, 0, 0, False],
        ['部定必修', '一般', '地理', 0, 2, 0, 0, 0, 0, False],
        ['部定必修', '一般', '公民與社會', 0, 0, 2, 0, 0, 0, False],
        ['部定必修', '一般', '物理', 0, 0, 2, 2, 0, 0, False],
        ['部定必修', '一般', '化學', 2, 0, 0, 0, 0, 0, False],
        ['部定必修', '一般', '美術', 2, 0, 0, 0, 0, 0, False],
        ['部定必修', '一般', '音樂', 0, 0, 1, 1, 0, 0, False],
        ['部定必修', '一般', '資訊科技', 0, 2, 0, 0, 0, 0, False],
        ['部定必修', '一般', '健康與護理', 2, 0, 0, 0, 0, 0, False],
        ['部定必修', '一般', '體育', 2, 2, 2, 2, 2, 2, False],
        ['部定必修', '一般', '全民國防教育', 1, 1, 0, 0, 0, 0, False],
        ['部定必修', '一般', '本土語/台灣手語', 0, 0, 2, 0, 0, 0, False],
        
        ['部定必修', '專業', '應用力學', 0, 0, 2, 0, 0, 0, False],
        ['部定必修', '專業', '機件原理', 0, 0, 0, 3, 0, 0, False],
        ['部定必修', '專業', '引擎原理', 0, 0, 3, 0, 0, 0, False],
        ['部定必修', '專業', '底盤原理', 0, 0, 0, 3, 0, 0, False],
        
        ['部定必修', '實習', '機械工作法及實習', 3, 3, 3, 3, 0, 0, True],
        ['部定必修', '實習', '機電製圖實習', 2, 2, 0, 0, 0, 0, True],
        ['部定必修', '實習', '引擎實習', 0, 0, 4, 0, 0, 0, True],
        ['部定必修', '實習', '底盤實習', 0, 0, 0, 4, 0, 0, True],
        ['部定必修', '實習', '電工電子實習', 3, 0, 0, 0, 0, 0, True],
        
        ['校訂必修', '一般', '閱讀與寫作', 2, 0, 0, 0, 0, 0, False],
        ['校訂必修', '一般', '計算機概論', 0, 2, 0, 0, 0, 0, False],
        ['校訂必修', '一般', '數學(校訂)', 0, 0, 4, 4, 0, 0, False], # 高二數學
        ['校訂必修', '專業', '電動車概論', 0, 0, 2, 0, 0, 0, False],
        ['校訂必修', '專業', '汽車工業英文', 2, 0, 0, 0, 0, 0, False],
        ['校訂必修', '實習', '專題實作', 0, 0, 0, 0, 2, 2, True],
        
        ['校訂選修', '實習', '汽車定期保養實習', 0, 0, 0, 0, 4, 0, True],
        ['校訂選修', '實習', '車輛儀器檢修實務', 0, 0, 0, 0, 0, 3, True],
        ['校訂選修', '專業', '先進車輛電控概論', 0, 0, 0, 0, 3, 0, False],
        ['校訂選修', '實習', '噴射引擎實習', 0, 0, 0, 0, 4, 0, True],
        ['校訂選修', '實習', '汽車美容實務', 0, 0, 0, 0, 0, 3, True],
        ['校訂選修', '一般', '數學演習', 0, 0, 0, 0, 2, 2, False], # 高三數學演習
        ['校訂選修', '一般', '原住民族語課程', 0, 0, 2, 2, 2, 2, False]
    ]

# --- 3. 解析邏輯 (修正學期對位) ---
with st.expander("📝 點此貼上成績文字 (自動鎖定學年期)", expanded=True):
    paste_txt = st.text_area("請貼上成績文字：", height=150)
    if st.button("🚀 執行解析"):
        if paste_txt:
            sem_map = {
                "112學年度第1學期": 0, "112學年度第2學期": 1,
                "113學年度第1學期": 2, "113學年度第2學期": 3,
                "114學年度第1學期": 4, "114學年度第2學期": 5
            }
            lines = paste_txt.split('\n')
            for line in lines:
                for key, s_idx in sem_map.items():
                    if key in line:
                        for idx, row in enumerate(st.session_state.courses):
                            # 比對科目名，若該學期有學分則勾選
                            if row[2] in line or row[2][:2] in line:
                                if row[3+s_idx] > 0:
                                    st.session_state[f"k_{idx}_{s_idx}"] = True
            st.success("✅ 解析完畢！")

if st.sidebar.button("🧹 清空勾選"):
    for k in list(st.session_state.keys()):
        if k.startswith("k_"): st.session_state[k] = False
    st.rerun()

# --- 4. 勾選介面 ---
tabs = st.tabs(["一年級", "二年級", "三年級"])
def render_year(tab_obj, s_idx):
    with tab_obj:
        for idx, row in enumerate(st.session_state.courses):
            c1, c2 = row[3+s_idx[0]], row[3+s_idx[1]]
            if c1 > 0 or c2 > 0:
                st.markdown(f'<div class="course-card">{row[2]}</div>', unsafe_allow_html=True)
                cols = st.columns(2)
                k1, k2 = f"k_{idx}_{s_idx[0]}", f"k_{idx}_{s_idx[1]}"
                if k1 not in st.session_state: st.session_state[k1] = False
                if k2 not in st.session_state: st.session_state[k2] = False
                if c1 > 0: cols[0].checkbox(f"上學期 ({c1})", key=k1)
                if c2 > 0: cols[1].checkbox(f"下學期 ({c2})", key=k2)

render_year(tabs[0], [0, 1])
render_year(tabs[1], [2, 3])
render_year(tabs[2], [4, 5])

# --- 5. 計算畢業門檻 ---
st.markdown("---")
stats = []
for idx, row in enumerate(st.session_state.courses):
    ev = 0
    for s in range(6):
        if st.session_state.get(f"k_{idx}_{s}", False): ev += row[3+s]
    stats.append({'cat': row[0], 'type': row[1], 'val': ev, 'pure': row[9]})

total_s = sum(x['val'] for x in stats)
# 部定必修 85% 動態門檻
dept_total = sum(sum(r[3:9]) for r in st.session_state.courses if r[0] == '部定必修')
dept_earned = sum(x['val'] for x in stats if x['cat'] == '部定必修')
dept_goal = round(dept_total * 0.85, 1)

prof_s = sum(x['val'] for x in stats if x['type'] in ['專業', '實習'])
pure_s = sum(x['val'] for x in stats if x['pure'])

def bar(label, now, goal):
    st.write(f"**{label}**")
    color = "#27ae60" if now >= goal else "#e74c3c"
    st.markdown(f"<h3 style='color:{color}; margin:0;'>{now} / {goal}</h3>", unsafe_allow_html=True)
    st.progress(min(now/goal, 1.0))

c_l, c_r = st.columns(2)
with c_l:
    bar("1. 總學分 (>=160)", total_s, 160)
    bar(f"2. 部定必修 (>=85%, 總{dept_total})", dept_earned, dept_goal)
with c_r:
    bar("3. 專業及實習 (>=60)", prof_s, 60)
    bar("4. 純實習 (>=30)", pure_s, 30)

if total_score >= 160 and dept_earned >= dept_goal and prof_s >= 60 and pure_s >= 30:
    st.balloons(); st.success("🎓 畢業條件達成！")
