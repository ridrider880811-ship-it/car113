import streamlit as st
import cv2
import numpy as np
import easyocr
from PIL import Image
import re

# --- 1. 頁面基礎配置 ---
st.set_page_config(page_title="汽車科學分檢核系統", layout="wide")

# --- 2. 高階 RWD 排版 CSS ---
st.markdown("""
    <style>
    /* 全域字體優化 */
    html, body, [class*="css"] { font-family: "Microsoft JhengHei", sans-serif; }
    
    /* 標題排版 */
    .main-title { font-size: 2.2rem; font-weight: 800; text-align: center; color: #2c3e50; margin-bottom: 0px; }
    .sub-title { font-size: 1.1rem; text-align: center; color: #7f8c8d; margin-bottom: 20px; }
    
    /* 進度條橘色美化 */
    .stProgress > div > div > div > div { background-color: #ff9f43; border-radius: 10px; }
    
    /* 手機版適應 (螢幕寬度小於 768px) */
    @media (max-width: 768px) {
        .main-title { font-size: 1.5rem; }
        .stCheckbox { font-size: 0.8rem; margin-bottom: 2px !important; }
        .block-container { padding: 0.5rem !important; }
        div[data-testid="column"] { width: 48% !important; flex: 1 1 45% !important; min-width: 45% !important; }
    }
    
    /* 卡片式外觀 */
    .course-card { background-color: #f8f9fa; padding: 10px; border-radius: 8px; border-left: 4px solid #3498db; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🚗 汽車科學分檢核系統</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">114 級汽車二甲專屬 (方案 B：雙軌校準版)</p>', unsafe_allow_html=True)
st.caption("製作人：羅章成老師")
st.write("---")

# --- 3. 核心資料庫 (48 門科目) ---
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
        ['部定必修', '一般', '藝術(音樂/美術)', 2, 2, 0, 0, 0, 0, False],
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

# --- 4. 側邊欄：雙軌功能區 ---
st.sidebar.header("📁 資料導入系統")

# A. 截圖 AI 辨識
up_img = st.sidebar.file_uploader("📸 方式1：上傳成績截圖", type=["png", "jpg", "jpeg"])
if up_img:
    if 'last_img' not in st.session_state or st.session_state.last_img != up_img.name:
        with st.spinner('AI 辨識中...'):
            reader = easyocr.Reader(['ch_tra', 'en'])
            result = reader.readtext(np.array(Image.open(up_img)))
            raw_txt = "".join([res[1] for res in result])
            for idx, row in enumerate(st.session_state.courses):
                if row[2][:2] in raw_txt:
                    for s in range(6): 
                        if row[3+s] > 0: st.session_state[f"k_{idx}_{s}"] = True
            st.session_state.last_img = up_img.name
            st.rerun()

# B. 文字複製貼上
st.sidebar.markdown("---")
paste_txt = st.sidebar.text_area("📋 方式2：全選貼上成績文字", height=150, placeholder="登入系統全選後在此貼上")
if st.sidebar.button("🚀 開始文字解析"):
    if paste_txt:
        for idx, row in enumerate(st.session_state.courses):
            if row[2][:2] in paste_txt:
                for s in range(6): 
                    if row[3+s] > 0: st.session_state[f"k_{idx}_{s}"] = True
        st.sidebar.success("解析完成！")
        st.rerun()

if st.sidebar.button("🧹 一鍵重置所有學分"):
    for k in list(st.session_state.keys()):
        if k.startswith("k_"): st.session_state[k] = False
    st.rerun()

seat_num = st.sidebar.text_input("座號", "01")
std_name = st.sidebar.text_input("姓名", "王大明")

# --- 5. 主內容區：勾選介面 ---
tabs = st.tabs(["一年級", "二年級", "三年級"])
sem_labels = ["一上", "一下", "二上", "二下", "三上", "三下"]

def render_courses(tab_obj, s_idx):
    with tab_obj:
        for idx, row in enumerate(st.session_state.courses):
            c1, c2 = row[3+s_idx[0]], row[3+s_idx[1]]
            if c1 > 0 or c2 > 0:
                st.markdown(f'<div class="course-card"><b>{row[2]}</b></div>', unsafe_allow_html=True)
                cols = st.columns(2)
                k1, k2 = f"k_{idx}_{s_idx[0]}", f"k_{idx}_{s_idx[1]}"
                if k1 not in st.session_state: st.session_state[k1] = False
                if k2 not in st.session_state: st.session_state[k2] = False
                if c1 > 0: cols[0].checkbox(f"上({c1}學分)", key=k1)
                if c2 > 0: cols[1].checkbox(f"下({c2}學分)", key=k2)

render_courses(tabs[0], [0, 1])
render_courses(tabs[1], [2, 3])
render_courses(tabs[2], [4, 5])

# --- 6. 計算與視覺化指標 ---
st.markdown("---")
st.subheader(f"📊 {seat_num}號 {std_name} 畢業戰報")

stats = []
for idx, row in enumerate(st.session_state.courses):
    earned = 0
    for s in range(6):
        if st.session_state.get(f"k_{idx}_{s}", False): earned += row[3+s]
    stats.append({'cat': row[0], 'type': row[1], 'val': earned, 'pure': row[9]})

t_all = sum(s['val'] for s in stats)
d_all = sum(s['val'] for s in stats if s['cat'] == '部定必修')
p_all = sum(s['val'] for s in stats if s['type'] in ['專業', '實習'])
s_all = sum(s['val'] for s in stats if s['pure'])

col1, col2 = st.columns([1, 1])

def draw_metric(col, label, now, goal):
    col.write(f"**{label}**")
    clr = "#27ae60" if now >= goal else "#e74c3c"
    col.markdown(f"<h3 style='color:{clr}; margin:0;'>{now} / {goal}</h3>", unsafe_allow_html=True)
    col.progress(min(now/goal, 1.0))

with col1:
    draw_metric(st, "1. 總學分 (>=160)", t_all, 160)
    draw_metric(st, "2. 部定必修 (>=106.3)", d_all, 106.3)

with col2:
    draw_metric(st, "3. 專業及實習 (>=60)", p_all, 60)
    draw_metric(st, "4. 純實習 (>=30)", s_all, 30)

# 最終判定
if t_all >= 160 and d_all >= 106.3 and p_all >= 60 and s_all >= 30:
    st.balloons()
    st.success("🎓 畢業條件已完全達成！恭喜！")
else:
    st.warning("⚠️ 目前條件尚未齊全，請繼續努力！")
