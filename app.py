import streamlit as st
import re

# --- 1. 頁面基礎配置 ---
st.set_page_config(page_title="汽車科學分檢核系統", layout="wide")

# --- 2. RWD 排版 CSS：區分電腦與手機視覺 ---
st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: "Microsoft JhengHei", sans-serif; }
    .main-title { font-size: 2.2rem; font-weight: 800; text-align: center; color: #2c3e50; margin-bottom: 0px; }
    .sub-title { font-size: 1.1rem; text-align: center; color: #7f8c8d; margin-bottom: 20px; }
    
    /* 進度條樣式 */
    .stProgress > div > div > div > div { background-color: #ff9f43; border-radius: 10px; }
    
    /* 手機版排版優化 (螢幕 < 768px) */
    @media (max-width: 768px) {
        .main-title { font-size: 1.5rem; }
        .stCheckbox { font-size: 0.9rem; margin-bottom: 8px !important; }
        .block-container { padding: 0.5rem !important; }
        /* 讓手機版的 Checkbox 按鈕變大一點，方便點擊 */
        div[data-testid="column"] { width: 48% !important; flex: 1 1 45% !important; }
    }
    
    /* 科目卡片外觀 */
    .course-card { 
        background-color: #f8f9fa; 
        padding: 8px 12px; 
        border-radius: 5px; 
        border-left: 5px solid #3498db; 
        margin-top: 15px; 
        margin-bottom: 5px; 
        font-weight: bold; 
        color: #2c3e50;
    }
    .import-box { 
        background-color: #e3f2fd; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #2196f3; 
        margin-bottom: 20px; 
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🚗 汽車科學分檢核系統</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">114 級汽車二甲專屬 (分頁累加精準版)</p>', unsafe_allow_html=True)
st.caption("製作人：羅章成老師")

# --- 3. 核心資料庫 (科目清單校對：美術音樂分開、含本土語、專業實習科目全入) ---
if 'courses' not in st.session_state:
    st.session_state.courses = [
        # 類別, 屬性, 科目名稱, 一上, 一下, 二上, 二下, 三上, 三下, 是否為實習
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

# --- 4. 頂部導入區 (支援分頁累加) ---
st.markdown('<div class="import-box"><b>💡 貼心提醒：</b><br>您可以分次貼上高一、高二、高三的成績文字，系統會自動「累加」勾選結果。</div>', unsafe_allow_html=True)

with st.expander("📝 點此展開文字貼上區", expanded=False):
    paste_txt = st.text_area("請在此貼上學校系統的成績文字：", height=200, placeholder="範例：登入系統後全選複製，貼於此處...")
    if st.button("🚀 執行累加解析"):
        if paste_txt:
            for idx, row in enumerate(st.session_state.courses):
                # 採用關鍵字解析，避免因為系統多了空格或括號而失敗
                if row[2][:2] in paste_txt:
                    for s in range(6):
                        if row[3+s] > 0:
                            st.session_state[f"k_{idx}_{s}"] = True
            st.success("✅ 解析完畢！學分已存入清單，您可以繼續貼上其他學年的資料。")

# 側邊欄控制與基本資訊
std_info = st.sidebar.text_input("學號/姓名", "01 王大明")
if st.sidebar.button("🧹 清空所有勾選"):
    for k in list(st.session_state.keys()):
        if k.startswith("k_"): st.session_state[k] = False
    st.rerun()

# --- 5. 主內容區：核對清單 ---
tabs = st.tabs(["一年級", "二年級", "三年級"])
sem_titles = ["一上", "一下", "二上", "二下", "三上", "三下"]

def render_year_tabs(tab_obj, s_indices):
    with tab_obj:
        for idx, row in enumerate(st.session_state.courses):
            c1, c2 = row[3+s_indices[0]], row[3+s_indices[1]]
            if c1 > 0 or c2 > 0:
                st.markdown(f'<div class="course-card">{row[2]}</div>', unsafe_allow_html=True)
                cols = st.columns(2)
                k1, k2 = f"k_{idx}_{s_indices[0]}", f"k_{idx}_{s_indices[1]}"
                
                # 初始化 state
                if k1 not in st.session_state: st.session_state[k1] = False
                if k2 not in st.session_state: st.session_state[k2] = False
                
                if c1 > 0: cols[0].checkbox(f"上學期 ({c1})", key=k1)
                if c2 > 0: cols[1].checkbox(f"下學期 ({c2})", key=k2)

render_year_tabs(tabs[0], [0, 1])
render_year_tabs(tabs[1], [2, 3])
render_year_tabs(tabs[2], [4, 5])

# --- 6. 畢業看板計算 ---
st.markdown("---")
st.subheader(f"📊 {std_info} 檢核看板")

final_stats = []
for idx, row in enumerate(st.session_state.courses):
    earned_val = 0
    for s in range(6):
        if st.session_state.get(f"k_{idx}_{s}", False):
            earned_val += row[3+s]
    final_stats.append({'cat': row[0], 'type': row[1], 'val': earned_val, 'pure': row[9]})

total_score = sum(i['val'] for i in final_stats)
dept_score = sum(i['val'] for i in final_stats if i['cat'] == '部定必修')
prof_score = sum(i['val'] for i in final_stats if i['type'] in ['專業', '實習'])
pure_score = sum(i['val'] for i in final_stats if i['pure'])

def bar(label, now, target):
    st.write(f"**{label}**")
    color = "#27ae60" if now >= target else "#e74c3c"
    st.markdown(f"<h3 style='color:{color}; margin:0;'>{now} / {target}</h3>", unsafe_allow_html=True)
    st.progress(min(now/target, 1.0))

c_l, c_r = st.columns(2)
with c_l:
    bar("1. 總學分 (門檻 160)", total_score, 160)
    bar("2. 部定必修 (門檻 106.3)", dept_score, 106.3)
with c_r:
    bar("3. 專業及實習 (門檻 60)", prof_score, 60)
    bar("4. 純實習 (門檻 30)", pure_score, 30)

if total_score >= 160 and dept_score >= 106.3 and prof_score >= 60 and pure_score >= 30:
    st.balloons(); st.success("🎓 畢業條件已完全達成！")
