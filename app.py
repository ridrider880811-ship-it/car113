import streamlit as st
import cv2
import numpy as np
import easyocr
from PIL import Image

# 1. 頁面配置
st.set_page_config(page_title="汽車科學分檢核系統", layout="centered")

# CSS 樣式修正：解決手機跳行與進度條顏色
st.markdown("""
    <style>
    .title-text { font-size: 24px !important; font-weight: bold; text-align: center; white-space: nowrap; }
    .sub-title-text { font-size: 16px !important; color: #555; text-align: center; margin-top: -5px; margin-bottom: 10px; }
    .stCheckbox { margin-top: -10px; margin-bottom: 5px; }
    .main .block-container { padding-top: 1rem; padding-left: 0.5rem; padding-right: 0.5rem; }
    .stProgress > div > div > div > div {
        background-color: #ff9f43; 
        background-image: linear-gradient(45deg, rgba(255, 255, 255, .2) 25%, transparent 25%, transparent 50%, rgba(255, 255, 255, .2) 50%, rgba(255, 255, 255, .2) 75%, transparent 75%, transparent);
        background-size: 1rem 1rem;
    }
    @media (max-width: 640px) { .title-text { font-size: 20px !important; } }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="title-text">🚗 汽車科學分檢核系統</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title-text">(加油，一定能順利畢業的！)</p>', unsafe_allow_html=True)
st.caption("製作人：羅章成老師")
st.write("---")

# 2. 原始科目資料庫
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

# 3. 側邊欄：AI 辨識功能 (強化邏輯)
st.sidebar.header("📸 AI 成績單辨識")
uploaded_file = st.sidebar.file_uploader("上傳成績截圖", type=["png", "jpg", "jpeg"])

if uploaded_file:
    if 'last_file' not in st.session_state or st.session_state.last_file != uploaded_file.name:
        with st.spinner('AI 正在讀取...'):
            img = Image.open(uploaded_file)
            reader = easyocr.Reader(['ch_tra', 'en'])
            result = reader.readtext(np.array(img))
            raw_text = "".join([res[1] for res in result])
            
            for idx, row in enumerate(st.session_state.courses):
                name = row[2]
                # 模糊比對：只要科目名稱的前兩個字出現在圖中，就當作及格
                if name[:2] in raw_text:
                    for s in range(6):
                        if row[3+s] > 0:
                            st.session_state[f"k_{idx}_{s}"] = True
            st.session_state.last_file = uploaded_file.name
            st.rerun()

seat_num = st.sidebar.text_input("座號", "01")
student_name = st.sidebar.text_input("姓名", "學生姓名")
if st.sidebar.button("🧹 一鍵清空"):
    for k in list(st.session_state.keys()):
        if k.startswith("k_"): st.session_state[k] = False
    st.rerun()

# 4. 學分勾選區 (Tabs)
st.write("### 📖 學分勾選區")
tabs = st.tabs(["高一", "高二", "高三"])

def draw_tab(tab_obj, s_indices):
    with tab_obj:
        for idx, row in enumerate(st.session_state.courses):
            c1, c2 = row[3+s_indices[0]], row[3+s_indices[1]]
            if c1 > 0 or c2 > 0:
                st.markdown(f"**{row[2]}**")
                cols = st.columns(2)
                k1, k2 = f"k_{idx}_{s_indices[0]}", f"k_{idx}_{s_indices[1]}"
                if k1 not in st.session_state: st.session_state[k1] = False
                if k2 not in st.session_state: st.session_state[k2] = False
                
                # 強制連動 Session State
                cols[0].checkbox(f"上 ({c1})", key=k1) if c1 > 0 else None
                cols[1].checkbox(f"下 ({c2})", key=k2) if c2 > 0 else None
                st.write("---")

draw_tab(tabs[0], [0, 1])
draw_tab(tabs[1], [2, 3])
draw_tab(tabs[2], [4, 5])

# 5. 計算畢業看板 (確保 100% 同步)
st.markdown("---")
st.subheader(f"📊 {seat_num} 號 {student_name} 檢核結果")

res_list = []
missing = { "一": [], "二": [], "三": [] }

for idx, row in enumerate(st.session_state.courses):
    e_row = 0
    for s in range(6):
        val = row[3+s]
        if val > 0:
            if st.session_state.get(f"k_{idx}_{s}", False):
                e_row += val
            else:
                y = "一" if s < 2 else ("二" if s < 4 else "三")
                missing[y].append(f"{sem_names[s]} {row[2]} ({val})")
    res_list.append({'cat': row[0], 'type': row[1], 'val': e_row, 'is_pure': row[9]})

t_s = sum(x['val'] for x in res_list)
d_s = sum(x['val'] for x in res_list if x['cat'] == '部定必修')
p_s = sum(x['val'] for x in res_list if x['type'] in ['專業', '實習'])
s_s = sum(x['val'] for x in res_list if x['is_pure'])

def bar(t, n, g):
    st.write(f"**{t}**")
    c = "#27ae60" if n >= g else "#e74c3c"
    st.markdown(f"<h3 style='color:{c}; margin:0;'>{n} / {g}</h3>", unsafe_allow_html=True)
    st.progress(min(n/g, 1.0))

bar("1. 總學分 (>=160)", t_s, 160)
bar("2. 部定必修 (>=106.3)", d_s, 106.3)
bar("3. 專業及實習 (>=60)", p_s, 60)
bar("4. 純實習 (>=30)", s_s, 30)

st.write("---")
st.write("### ❌ 待修明細")
for y, items in missing.items():
    with st.expander(f"{y}年級 (剩 {len(items)} 門)", expanded=False):
        if not items: st.success("全過！")
        else:
            for i in items: st.write(f"• {i}")

st.write("---")
st.write("製作人：羅章成老師")

if t_s >= 160 and d_s >= 106.3 and p_s >= 60 and s_s >= 30:
    st.balloons(); st.success("🎓 准予畢業！")
