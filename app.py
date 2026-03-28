import streamlit as st
import re

# --- 1. 頁面配置與進階樣式 (美化 Dashboard) ---
st.set_page_config(page_title="汽車科畢業學分檢核", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: "Microsoft JhengHei", sans-serif; }
    .main-title { font-size: 2.2rem; font-weight: 800; text-align: center; color: #1e3799; margin-bottom: 5px; }
    
    /* 畢業門檻儀表板卡片 */
    .metric-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        border-top: 5px solid #1e3799;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-label { font-size: 0.9rem; color: #576574; font-weight: bold; }
    .metric-value { font-size: 1.5rem; color: #2c3e50; font-weight: 900; margin: 5px 0; }
    
    .course-card { background-color: #ffffff; padding: 8px; border-radius: 8px; border-left: 5px solid #4a69bd; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); margin-top: 8px; font-weight: bold; font-size: 0.95rem; }
    .missing-card { color: #eb2f06; background-color: #ffeef0; padding: 6px; border-radius: 5px; margin-bottom: 4px; border-left: 4px solid #eb2f06; font-size: 0.85rem; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🚗 畢業學分檢核系統</p>', unsafe_allow_html=True)
st.caption("<div style='text-align:center;'>製作人：羅章成老師 | 113課綱標準版</div>", unsafe_allow_html=True)

# --- 2. 核心資料庫 (嚴格鎖定科目) ---
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
        ['校訂必修', '一般', '閱讀與寫作', 0, 0, 0, 0, 1, 1, False],
        ['校訂選修', '一般', '兵家的智慧', 0, 0, 1, 0, 0, 0, False],
        ['校訂選修', '實習', '汽車檢驗實習', 0, 0, 2, 0, 4, 0, True],
        ['校訂選修', '實習', '車輛微電腦控制實習', 0, 0, 2, 2, 0, 0, True],
        ['校訂選修', '一般', '原住民族語課程', 0, 0, 2, 2, 2, 2, False],
    ]

# --- 3. UI 與解析功能 ---
with st.sidebar:
    st_name = st.text_input("座號 / 姓名", value="王茂鈞")
    if st.button("🧹 重新檢測 (清空勾選)"):
        for k in list(st.session_state.keys()):
            if k.startswith("k_"): st.session_state[k] = False
        st.rerun()

with st.expander("📥 第一步：貼上成績文字自動解析"):
    paste_txt = st.text_area("請在此貼上歷年成績文字：", height=150)
    if st.button("🚀 開始偵測學分"):
        if paste_txt:
            # 處理特殊空格：將所有種類的空白字元都轉為標準空格
            clean_full_txt = re.sub(r'\s+', ' ', paste_txt)
            
            # 偵測「只有二上」的特徵：實得學分 32 後面跟著 0
            is_y2_s1_only = "二年級" in clean_full_txt and "實得學分 32 0" in clean_full_txt
            
            lines = paste_txt.split('\n')
            for line in lines:
                # 移除行內雜訊以便比對
                clean_line = line.replace(" ", "").replace("\xa0", "")
                for idx, row in enumerate(st.session_state.courses):
                    if row[2][:2] in clean_line:
                        # 算這一行出現了幾個「40-100」之間的數字
                        # 茂鈞的二上文字：必修285必修85 -> 會有兩個分數
                        scores = re.findall(r"(?<!\d)(?:[4-9]\d|100)(?!\d)", clean_line)
                        
                        if "一年級" in paste_txt:
                            if row[3]>0: st.session_state[f"k_{idx}_0"] = True
                            # 一年級如果整年讀完，一行會有 3 個分數（上、下、學年）
                            if row[4]>0 and len(scores) >= 2: st.session_state[f"k_{idx}_1"] = True
                        
                        if "二年級" in paste_txt:
                            # 勾選二上
                            if row[5]>0: st.session_state[f"k_{idx}_2"] = True
                            # 嚴格勾選二下：
                            # 1. 不能符合「二上專用資料」特徵
                            # 2. 該行分數數量必須足夠（通常有三組分數才代表上下學期都及格）
                            if not is_y2_s1_only and row[6]>0 and len(scores) >= 3:
                                st.session_state[f"k_{idx}_3"] = True
            st.rerun()

tabs = st.tabs(["📅 高一階段", "📅 高二階段", "📅 高三階段"])
sem_names = ["一上", "一下", "二上", "二下", "三上", "三下"]
def render_year(tab_obj, s_idx):
    with tab_obj:
        for idx, row in enumerate(st.session_state.courses):
            c1, c2 = row[3+s_idx[0]], row[3+s_idx[1]]
            if c1 > 0 or c2 > 0:
                st.markdown(f'<div class="course-card">{row[2]}</div>', unsafe_allow_html=True)
                cols = st.columns(2)
                k1, k2 = f"k_{idx}_{s_idx[0]}", f"k_{idx}_{s_idx[1]}"
                if c1 > 0: cols[0].checkbox(f"上及格({c1})", key=k1)
                if c2 > 0: cols[1].checkbox(f"下及格({c2})", key=k2)

render_year(tabs[0], [0, 1])
render_year(tabs[1], [2, 3])
render_year(tabs[2], [4, 5])

# --- 4. 畢業門檻達成看板 ---
st.markdown("---")
st.subheader("📊 畢業資格達成檢測")

stats, m1, m2, m3 = [], [], [], []
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

d_cols = st.columns(4)
items = [("總學分 (>=160)", f"{total}/160", total/160), 
         ("部定必修 (>=106.3)", f"{dept}/106.3", dept/106.3),
         ("專業及實習 (>=60)", f"{prof}/60", prof/60),
         ("純實習 (>=30)", f"{prac}/30", prac/30)]

for i, (l, v, p) in enumerate(items):
    with d_cols[i]:
        st.markdown(f'<div class="metric-card"><div class="metric-label">{l}</div><div class="metric-value">{v}</div></div>', unsafe_allow_html=True)
        st.progress(min(p, 1.0))

st.markdown("### 🔍 未取得學分清單")
c_m1, c_m2, c_m3 = st.columns(3)
with c_m1:
    with st.expander("📅 高一缺修", expanded=True):
        if m1: [st.markdown(f'<div class="missing-card">{x}</div>', unsafe_allow_html=True) for x in m1]
        else: st.success("✅ 全部取得")
with c_m2:
    with st.expander("📅 高二缺修", expanded=True):
        if m2: [st.markdown(f'<div class="missing-card">{x}</div>', unsafe_allow_html=True) for x in m2]
        else: st.success("✅ 全部取得")
with c_m3:
    with st.expander("📅 高三缺修", expanded=True):
        if m3: [st.markdown(f'<div class="missing-card">{x}</div>', unsafe_allow_html=True) for x in m3]
        else: st.success("✅ 預計拿滿")
