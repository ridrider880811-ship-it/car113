import streamlit as st
import pandas as pd

# 頁面配置 (可愛風設定)
st.set_page_config(page_title="114汽車二甲學分檢核", page_icon="🚗", layout="wide")

# 加入簡單的 CSS 讓介面更緊湊、更可愛
st.markdown("""
    <style>
    .stCheckbox { margin-bottom: -15px; }
    .main .block-container { padding-top: 2rem; }
    h1, h2, h3 { font-family: 'Comic Sans MS', cursive, sans-serif; }
    div[data-testid="stMetricValue"] > div { font-size: 2rem; color: #ff4b4b; }
    div[data-testid="stExpander"] { border: 2px solid #D9EAD3; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚗 Taitung East Auto - 114汽車二甲畢業檢核 App")
st.markdown("---")

# 1. 科目資料庫 (完全保留原始科目與學分)
# 格式：[類別, 性質, 科目名稱, 一上, 一下, 二上, 二下, 三上, 三下, 是否純實習]
if 'courses' not in st.session_state:
    st.session_state.courses = [
        # --- 🏫 部定必修 (一般科目) ---
        ['部定必修', '一般', '📚 國語文', 3, 3, 3, 3, 2, 2, False],
        ['部定必修', '一般', '🇬🇧 英語文', 2, 2, 2, 2, 2, 2, False],
        ['部定必修', '一般', '🔢 數學', 4, 4, 0, 0, 0, 0, False],
        ['部定必修', '一般', '📜 歷史', 2, 0, 0, 0, 0, 0, False],
        ['部定必修', '一般', '🗺️ 地理', 0, 0, 0, 2, 0, 0, False],
        ['部定必修', '一般', '⚖️ 公民與社會', 0, 0, 0, 0, 2, 0, False],
        ['部定必修', '一般', '💡 法律與生活', 0, 0, 0, 0, 0, 2, False],
        ['部定必修', '一般', '⚡ 物理', 2, 2, 0, 0, 0, 0, False],
        ['部定必修', '一般', '🧪 化學', 0, 2, 0, 0, 0, 0, False],
        ['部定必修', '一般', '🎵 音樂', 0, 0, 1, 1, 0, 0, False],
        ['部定必修', '一般', '🎨 美術', 2, 0, 0, 0, 0, 0, False],
        ['部定必修', '一般', '💻 資訊科技', 0, 2, 0, 0, 0, 0, False],
        ['部定必修', '一般', '🏥 健康與護理', 2, 0, 0, 0, 0, 0, False],
        ['部定必修', '一般', '🏃 體育', 2, 2, 2, 2, 2, 2, False],
        ['部定必修', '一般', '🛡️ 全民國防教育', 1, 1, 0, 0, 0, 0, False],
        ['部定必修', '一般', '🗣️ 本土語/台灣手語', 0, 0, 0, 2, 0, 0, False],
        # --- 🛠️ 部定必修 (專業/實習科目) ---
        ['部定必修', '專業', '💪 應用力學', 0, 0, 2, 0, 0, 0, False],
        ['部定必修', '專業', '⚙️ 機件原理', 0, 0, 2, 0, 0, 0, False],
        ['部定必修', '專業', '🔥 引擎原理', 3, 0, 0, 0, 0, 0, False],
        ['部定必修', '專業', '🔩 底盤原理', 0, 3, 0, 0, 0, 0, False],
        ['部定必修', '專業', '🔌 基本電學', 0, 0, 2, 0, 0, 0, False],
        ['部定必修', '實習', '🛠️ 機械工作法及實習', 0, 4, 0, 0, 0, 0, True],
        ['部定必修', '實習', '📐 機電製圖實習', 2, 2, 0, 0, 0, 0, True],
        ['部定必修', '實習', '🔧 引擎實習', 0, 0, 4, 0, 0, 0, True],
        ['部定必修', '實習', '🔩 底盤實習', 0, 0, 3, 0, 0, 0, True],
        ['部定必修', '實習', '電系實習', 0, 0, 0, 3, 0, 0, True],
        ['部定必修', '實習', '電工電子實習', 0, 0, 3, 0, 0, 0, True],
        ['部定必修', '實習', '車輛空調檢修實習', 0, 0, 0, 0, 3, 0, True],
        ['部定必修', '實習', '車輛底盤檢修實習', 0, 0, 0, 4, 0, 0, True],
        ['部定必修', '實習', '車身電器系統綜合檢修實習', 0, 0, 0, 0, 4, 0, True],
        ['部定必修', '實習', '機器腳踏車基礎實習', 3, 0, 0, 0, 0, 0, True],
        ['部定必修', '實習', '機器腳踏車檢修實習', 0, 3, 0, 0, 0, 0, True],
        # --- 🏫 校訂必修 ---
        ['校訂必修', '一般', '青少年身心健康管理', 0, 2, 0, 0, 0, 0, False],
        ['校訂必修', '一般', '🔢 數學', 0, 0, 4, 4, 0, 0, False],
        ['校訂必修', '一般', '📖 閱讀與寫作', 0, 0, 0, 0, 1, 1, False],
        ['校訂必修', '一般', '💻 計算機概論', 2, 0, 0, 0, 0, 0, False],
        ['校訂必修', '專業', '電動車概論', 0, 0, 0, 2, 0, 0, False],
        ['校訂必修', '專業', '汽車工業英文', 0, 0, 0, 0, 0, 2, False],
        ['校訂必修', '實習', '電動機車實習', 0, 0, 0, 0, 2, 0, True],
        ['校訂必修', '實習', '專題實作', 0, 0, 0, 0, 2, 2, True],
        ['校訂必修', '實習', '訊號量測與分析實習', 0, 0, 0, 0, 0, 2, True],
        # --- 🏫 校訂選修 ---
        ['校訂選修', '一般', '兵家的智慧', 0, 0, 1, 0, 0, 0, False],
        ['校訂選修', '一般', '野外求生', 0, 0, 0, 1, 0, 0, False],
        ['校訂選修', '一般', '數學演習', 0, 0, 0, 0, 2, 2, False],
        ['校訂選修', '專業', '交通安全與法規', 0, 0, 0, 0, 1, 0, False],
        ['校訂選修', '專業', '汽車新式裝備', 0, 0, 0, 0, 0, 1, False],
        ['校訂選修', '專業', '先進車輛電控概論', 0, 0, 0, 0, 0, 3, False],
        ['校訂選修', '實習', '車輛微電腦控制實習', 0, 0, 2, 2, 0, 0, True],
    ]

# 2. 側邊欄 (學生資訊與一鍵清除)
st.sidebar.header("👤 學生登入")
seat_num = st.sidebar.text_input("輸入座號", "01")
student_name = st.sidebar.text_input("輸入姓名", "學生測試A")

st.sidebar.markdown("---")
if st.sidebar.button("🧹 一鍵清空重來"):
    # 清空所有 checkbox 的狀態
    for key in st.session_state.keys():
        if key.startswith("c_"):
            st.session_state[key] = False
    st.experimental_rerun()

# 3. 佈局設計 (左邊勾選，右邊圓形圖表)
col_input, col_status = st.columns([2, 1])

with col_input:
    st.write("### 📖 學年學分勾選清單")
    tab1, tab2, tab3 = st.tabs(["🆕 高一", "🔥 高二", "🎓 高三"])
    
    # 用於儲存勾選狀態的字典
    checked = {}

    def draw_tab(tab, s_indices, label):
        with tab:
            h = st.columns([3, 1, 1])
            h[0].write("**科目名稱**")
            h[1].write(f"**{label}上**")
            h[2].write(f"**{label}下**")
            for idx, row in enumerate(st.session_state.courses):
                c1, c2 = row[3+s_indices[0]], row[3+s_indices[1]]
                if c1 > 0 or c2 > 0:
                    cols = st.columns([3, 1, 1])
                    cols[0].write(f"{row[2]}")
                    key1 = f"c_{idx}_{s_indices[0]}"
                    key2 = f"c_{idx}_{s_indices[1]}"
                    checked[f"{idx}_{s_indices[0]}"] = cols[1].checkbox(f"{c1}", key=key1) if c1 > 0 else False
                    checked[f"{idx}_{s_indices[1]}"] = cols[2].checkbox(f"{c2}", key=key2) if c2 > 0 else False

    draw_tab(tab1, [0, 1], "高一")
    draw_tab(tab2, [2, 3], "高二")
    draw_tab(tab3, [4, 5], "高三")

# 4. 計算與視覺化圓形圖表
with col_status:
    st.write(f"### 👋 哈囉，{seat_num} 號 {student_name}！")
    
    summary = []
    missing_list = []
    
    for idx, row in enumerate(st.session_state.courses):
        earned = 0
        missing = 0
        for s in range(6):
            c_val = row[3+s]
            if c_val > 0:
                if checked.get(f"{idx}_{s}", False):
                    earned += c_val
                else:
                    missing += c_val
        
        summary.append({'cat': row[0], 'type': row[1], 'val': earned, 'is_pure': row[9]})
        if missing > 0:
            missing_list.append(f"{row[2]} (欠 {missing})")

    # 指標計算
    t_now = sum(s['val'] for s in summary)
    d_now = sum(s['val'] for s in summary if s['cat'] == '部定必修')
    p_now = sum(s['val'] for s in summary if s['type'] in ['專業', '實習'])
    s_now = sum(s['val'] for s in summary if s['is_pure'])

    st.write("### 🎓 畢業檢核儀表板")
    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)

    def draw_circular_metric(col, label, now, target):
        percent = min(now/target, 1.0)
        col.write(f"**{label}**")
        color = "green" if now >= target else "red"
        # 這裡模擬圓形圖 (Streamlit 沒內建，用進度條和樣式模擬)
        col.progress(percent)
        col.markdown(f"<h3 style='color:{color}; margin:-10px 0 10px 0'>{now} / {target}</h3>", unsafe_allow_html=True)

    draw_circular_metric(c1, "總學分 (>=160)", t_now, 160)
    draw_circular_metric(c2, "部定必修 (>=106.3)", d_now, 106.3)
    draw_circular_metric(c3, "專業實習 (>=60)", p_now, 60)
    draw_circular_metric(c4, "純實習 (>=30)", s_now, 30)

    st.write("---")
    with st.expander("❌ 待修/未過科目明細", expanded=True):
        if not missing_list:
            st.success("全部科目皆已及格！")
        else:
            for m in missing_list:
                st.write(f"- {m}")

    if t_now >= 160 and d_now >= 106.3 and p_now >= 60 and s_now >= 30:
        st.balloons()
        st.success("🎓 准予畢業！")
