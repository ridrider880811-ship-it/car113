import streamlit as st
import cv2
import numpy as np
import easyocr
from PIL import Image

# 1. 頁面配置
st.set_page_config(page_title="汽車科學分檢核系統", layout="centered")

# CSS 樣式：手機版優化 + 橘色可愛風進度條
st.markdown("""
    <style>
    .title-text { font-size: 24px !important; font-weight: bold; text-align: center; white-space: nowrap; }
    .sub-title-text { font-size: 16px !important; color: #555; text-align: center; margin-top: -5px; margin-bottom: 10px; }
    .stCheckbox { margin-bottom: 5px; }
    .main .block-container { padding-top: 1rem; padding-left: 0.5rem; padding-right: 0.5rem; }
    .stProgress > div > div > div > div { background-color: #ff9f43; }
    @media (max-width: 640px) { .title-text { font-size: 20px !important; } }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="title-text">🚗 汽車科學分檢核系統</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title-text">(加油，一定能順利畢業的！)</p>', unsafe_allow_html=True)
st.caption("製作人：羅章成老師")
st.write("---")

# 2. 原始科目資料庫 (精確 48 門科目)
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
        ['校訂選修', '實習', '汽車檢驗實習', 0, 0, 2, 2, 0, 0, True],
        ['校訂選修', '實習', '車輛儀器檢修實務', 0, 0, 0, 0, 3, 0, True],
        ['校訂選修', '實習', '車輛微電腦控制實習', 0, 0, 2, 2, 0, 0, True],
        ['校訂選修', '實習', '汽車美容實務', 0, 0, 0, 0, 0, 3, True],
        ['校訂選修', '實習', '汽車定期保養實習', 0, 0, 0, 0, 0, 4, True],
        ['校訂選修', '實習', '車輪定位檢修實習', 0, 0, 0, 0, 0, 4, True],
        ['校訂選修', '實習', '噴射引擎實習', 0, 0, 0, 0, 4, 0, True],
        ['校訂選修', '實習', '汽車塗裝實習', 0, 0, 0, 0, 4, 0, True],
        ['校訂選修', '實習', '柴油引擎實習', 0, 0, 0, 0, 4, 0, True],
        ['校訂選修', '實習', '汽車綜合實習', 0, 0, 0, 0, 4, 0, True],
    ]

# 3. 側邊欄 AI 辨識
st.sidebar.header("📸 AI 學分辨識")
uploaded_file = st.sidebar.file_uploader("上傳成績截圖", type=["png", "jpg", "jpeg"])

if uploaded_file:
    if 'processed_file' not in st.session_state or st.session_state.processed_file != uploaded_file.name:
        with st.spinner('辨識中...'):
            img = Image.open(uploaded_file)
            reader = easyocr.Reader(['ch_tra', 'en'])
            result = reader.readtext(np.array(img))
            raw_text = "".join([res[1] for res in result])
            
            # 精確比對邏輯
            for idx, row in enumerate(st.session_state.courses):
                subj = row[2]
                if subj in raw_text:
                    for s in range(6):
                        if row[3+s] > 0:
                            st.session_state[f"k_{idx}_{s}"] = True
            st.session_state.processed_file = uploaded_file.name
            st.rerun()

seat_num = st.sidebar.text_input("座號", "01")
student_name = st.sidebar.text_input("姓名", "學生姓名")
if st.sidebar.button("🧹 清空"):
    for k in list(st.session_state.keys()):
        if k.startswith("k_"): st.session_state[k] = False
    st.rerun()

# 4. 介面呈現
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
                
                if c1 > 0: cols[0].checkbox(f"上 ({c1})", key=k1)
                if c2 > 0: cols[1].checkbox(f"下 ({c2})", key=k2)
                st.write("---")

draw_tab(tabs[0], [0, 1])
draw_tab(tabs[1], [2, 3])
draw_tab(tabs[2], [4, 5])

# 5. 計算指標 (修正計算 Bug)
st.markdown("---")
st.subheader(f"📊 {seat_num}號 {student_name} 畢業檢核")

earned_list = []
missing_items = { "一": [], "二": [], "三": [] }

for idx, row in enumerate(st.session_state.courses):
    earned_val = 0
    for s in range(6):
        c_v = row[3+s]
        if c_v > 0:
            if st.session_state.get(f"k_{idx}_{s}", False):
                earned_val += c_v
            else:
                y = "一" if s < 2 else ("二" if s < 4 else "三")
                missing_items[y].append(f"{sem_names[s]} {row[2]} ({c_v})")
    earned_list.append({'cat': row[0], 'type': row[1], 'val': earned_val, 'is_pure': row[9]})

t_sum = sum(e['val'] for e in earned_list)
d_sum = sum(e['val'] for e in earned_list if e['cat'] == '部定必修')
p_sum = sum(e['val'] for e in earned_list if e['type'] in ['專業', '實習'])
s_sum = sum(e['val'] for e in earned_list if e['is_pure'])

def bar(title, now, target):
    st.write(f"**{title}**")
    color = "#27ae60" if now >= target else "#e74c3c"
    st.markdown(f"<h3 style='color:{color}; margin:0;'>{now} / {target}</h3>", unsafe_allow_html=True)
    st.progress(min(now/target, 1.0))

bar("1. 總學分數 (>=160)", t_sum, 160)
bar("2. 部定必修 (>=106.3)", d_sum, 106.3)
bar("3. 專業科目及實習科目 (>=60)", p_sum, 60)
bar("4. 純實習科目 (>=30)", s_sum, 30)

st.write("---")
st.write("### ❌ 待修明細")
for y, items in missing_items.items():
    with st.expander(f"{y}年級 (剩 {len(items)} 門)", expanded=False):
        if not items: st.success("全過！")
        else:
            for i in items: st.write(f"• {i}")

st.write("---")
st.write("本系統製作人：羅章成老師")

if t_sum >= 160 and d_sum >= 106.3 and p_sum >= 60 and s_sum >= 30:
    st.balloons(); st.success("🏁 准予畢業！")
