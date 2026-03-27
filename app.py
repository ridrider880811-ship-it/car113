import streamlit as st
import cv2
import numpy as np
import easyocr
from PIL import Image

# 1. 頁面配置
st.set_page_config(page_title="汽車科學分檢核系統", layout="centered")

# CSS 樣式優化 (手機與電腦兼顧)
st.markdown("""
    <style>
    .title-text { font-size: 24px !important; font-weight: bold; text-align: center; white-space: nowrap; }
    .sub-title-text { font-size: 16px !important; color: #555; text-align: center; margin-top: -5px; }
    .stProgress > div > div > div > div { background-color: #ff9f43; }
    @media (max-width: 640px) { .title-text { font-size: 20px !important; } }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="title-text">🚗 汽車科學分檢核系統</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title-text">(加油，一定能順利畢業的！)</p>', unsafe_allow_html=True)
st.caption("製作人：羅章成老師")

# 2. 原始科目資料庫 (48 門)
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

# 3. AI 辨識邏輯 (核心新增)
st.sidebar.header("📸 AI 成績單辨識")
uploaded_file = st.sidebar.file_uploader("上傳成績截圖", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    with st.spinner('AI 正在讀取成績中...'):
        image = Image.open(uploaded_file)
        img_np = np.array(image)
        reader = easyocr.Reader(['ch_tra', 'en']) # 繁體中文與英文
        result = reader.readtext(img_np)
        
        recognized_text = " ".join([res[1] for res in result])
        st.sidebar.success("辨識完成！請核對下方勾選。")
        
        # 自動勾選邏輯
        for idx, row in enumerate(st.session_state.courses):
            subject = row[2]
            if subject in recognized_text:
                # 簡單判定：只要科目出現在圖中，且這學期有學分，就暫時幫他勾選
                # 精確版需要判斷分數欄位，此為快速雛形
                for s in range(6):
                    if row[3+s] > 0:
                        st.session_state[f"k_{idx}_{s}"] = True

# 側邊欄其他資訊
seat_num = st.sidebar.text_input("座號", "01")
student_name = st.sidebar.text_input("姓名", "學生姓名")
if st.sidebar.button("🧹 一鍵清空勾選"):
    for key in list(st.session_state.keys()):
        if key.startswith("k_"): st.session_state[key] = False
    st.rerun()

# 4. 介面呈現與計算 (同前版本)
checked = {}
st.write("### 📖 學分勾選區")
tabs = st.tabs(["高一", "高二", "高三"])

def draw_mobile_course(tab_obj, s_indices):
    with tab_obj:
        for idx, row in enumerate(st.session_state.courses):
            st.markdown(f"**{row[2]}**")
            cols = st.columns(2)
            k1, k2 = f"k_{idx}_{s_indices[0]}", f"k_{idx}_{s_indices[1]}"
            c1, c2 = row[3+s_indices[0]], row[3+s_indices[1]]
            
            # 使用 session_state 來同步 AI 辨識的結果
            checked[f"{idx}_{s_indices[0]}"] = cols[0].checkbox(f"上 ({c1})", value=st.session_state.get(k1, False), key=k1) if c1 > 0 else False
            checked[f"{idx}_{s_indices[1]}"] = cols[1].checkbox(f"下 ({c2})", value=st.session_state.get(k2, False), key=k2) if c2 > 0 else False
            st.write("---")

draw_mobile_course(tabs[0], [0, 1])
draw_mobile_course(tabs[1], [2, 3])
draw_mobile_course(tabs[2], [4, 5])

# 5. 計算結果 (略，同前版本)
# ... (此處保留原有的計算與進度條邏輯)
