import streamlit as st

# --- 1. 頁面基礎配置 ---
st.set_page_config(page_title="汽車科學分檢核系統", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: "Microsoft JhengHei", sans-serif; }
    .main-title { font-size: 2.2rem; font-weight: 800; text-align: center; color: #2c3e50; margin-bottom: 5px; }
    .course-card { background-color: #f8f9fa; padding: 8px 12px; border-radius: 5px; border-left: 5px solid #3498db; margin-top: 10px; font-weight: bold; }
    .missing-card { color: #e74c3c; background-color: #fff5f5; padding: 5px 10px; border-radius: 4px; margin-bottom: 5px; border: 1px solid #ffc9c9; }
    .elective-info { font-size: 0.8rem; color: #666; font-weight: normal; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🚗 畢業學分清單</p>', unsafe_allow_html=True)
st.caption("製作人：羅章成老師")

# --- 2. 核心資料庫 (依 PDF 113 課綱人工精確校對順序) ---
# [類別, 屬性, 科目名稱, 一上, 一下, 二上, 二下, 三上, 三下, 是否純實習, 總學分]
if 'courses' not in st.session_state:
    st.session_state.courses = [
        # --- 部定必修 一般科目 (總計 74) ---
        ['部定必修', '一般', '國語文', 3, 3, 3, 3, 2, 2, False, 16],
        ['部定必修', '一般', '英語文', 2, 2, 2, 2, 2, 2, False, 12],
        ['部定必修', '一般', '數學', 4, 4, 0, 0, 0, 0, False, 8],
        ['部定必修', '一般', '歷史', 2, 0, 0, 0, 0, 0, False, 2],
        ['部定必修', '一般', '地理', 0, 2, 0, 0, 0, 0, False, 2],
        ['部定必修', '一般', '公民與社會', 0, 0, 2, 0, 0, 0, False, 2],
        ['部定必修', '一般', '物理', 0, 0, 2, 2, 0, 0, False, 4],
        ['部定必修', '一般', '化學', 2, 0, 0, 0, 0, 0, False, 2],
        ['部定必修', '一般', '音樂', 0, 0, 1, 0, 0, 0, False, 1],
        ['部定必修', '一般', '美術', 2, 0, 0, 0, 0, 0, False, 2],
        ['部定必修', '一般', '資訊科技', 0, 2, 0, 0, 0, 0, False, 2],
        ['部定必修', '一般', '健康與護理', 2, 0, 0, 0, 0, 0, False, 2],
        ['部定必修', '一般', '體育', 2, 2, 2, 2, 2, 2, False, 12],
        ['部定必修', '一般', '全民國防教育', 1, 1, 0, 0, 0, 0, False, 2],
        ['部定必修', '一般', '本土語/臺灣手語', 0, 0, 0, 2, 0, 0, False, 2],
        ['部定必修', '一般', '法律與生活', 0, 0, 0, 0, 2, 1, False, 3],

        # --- 部定必修 專業科目 ---
        ['部定必修', '專業', '應用力學', 0, 0, 2, 0, 0, 0, False, 2],
        ['部定必修', '專業', '機件原理', 0, 0, 3, 0, 0, 0, False, 3],
        ['部定必修', '專業', '引擎原理', 3, 0, 0, 0, 0, 0, False, 3],
        ['部定必修', '專業', '底盤原理', 0, 4, 0, 0, 0, 0, False, 4],

        # --- 部定必修 實習科目 (總計 39) ---
        ['部定必修', '實習', '機械工作法及實習', 0, 0, 0, 0, 3, 3, True, 6],
        ['部定必修', '實習', '機電製圖實習', 2, 2, 0, 0, 0, 0, True, 4],
        ['部定必修', '實習', '引擎實習', 4, 0, 0, 0, 0, 0, True, 4],
        ['部定必修', '實習', '底盤實習', 0, 4, 0, 0, 0, 0, True, 4],
        ['部定必修', '實習', '電工電子實習', 0, 0, 3, 0, 0, 0, True, 3],
        ['部定必修', '實習', '電系實習', 0, 0, 0, 3, 0, 0, True, 3],
        ['部定必修', '實習', '車輛空調檢修實習', 0, 0, 0, 0, 3, 0, True, 3],
        ['部定必修', '實習', '車輛底盤檢修實習', 0, 0, 0, 4, 0, 0, True, 4],
        ['部定必修', '實習', '車身電器系統綜合檢修實習', 0, 0, 0, 0, 4, 0, True, 4],
        ['部定必修', '實習', '機器腳踏車基礎實習', 0, 0, 3, 0, 0, 0, True, 3],
        ['部定必修', '實習', '機器腳踏車檢修實習', 0, 3, 0, 0, 0, 0, True, 3],

        # --- 校訂必修 (總計 28) ---
        ['校訂必修', '一般', '青少年身心健康管理', 0, 2, 0, 0, 0, 0, False, 2],
        ['校訂必修', '一般', '數學', 0, 0, 2, 2, 2, 2, False, 8],
        ['校訂必修', '一般', '計算機概論', 2, 0, 0, 0, 0, 0, False, 2],
        ['校訂必修', '一般', '閱讀與寫作', 0, 0, 0, 0, 1, 1, False, 2],
        ['校訂必修', '專業', '汽車工業英文', 0, 0, 0, 0, 2, 0, False, 2],
        ['校訂必修', '專業', '電動車概論', 0, 0, 0, 2, 0, 0, False, 2],
        ['校訂必修', '實習', '電動機車實習', 0, 0, 0, 0, 0, 2, True, 2],
        ['校訂必修', '實習', '專題實作', 0, 0, 0, 0, 2, 2, True, 4],
        ['校訂必修', '實習', '訊號量測與分析實習', 0, 0, 0, 0, 2, 2, True, 4],

        # --- 校訂選修 (選修區，含二選一) ---
        ['校訂選修', '一般', '兵家的智慧', 0, 0, 1, 0, 0, 0, False, 1],
        ['校訂選修', '一般', '野外求生', 0, 0, 0, 1, 0, 0, False, 1],
        ['校訂選修', '一般', '數學演習', 0, 0, 0, 0, 2, 2, False, 4],
        ['校訂選修', '專業', '交通安全與法規', 0, 0, 0, 0, 1, 0, False, 1],
        ['校訂選修', '專業', '汽車新式裝備', 0, 0, 0, 0, 0, 1, False, 1],
        ['校訂選修', '專業', '先進車輛電控概論', 0, 0, 0, 0, 3, 0, False, 3],
        ['校訂選修', '實習', '汽車檢驗實習', 0, 0, 0, 0, 4, 0, True, 4],
        ['校訂選修', '實習', '原住民族語課程', 0, 0, 2, 2, 2, 2, False, 8],
        ['校訂選修', '實習', '車輛儀器檢修實務 (2選1)', 0, 0, 0, 0, 0, 3, True, 3],
        ['校訂選修', '實習', '汽車定期保養實習 (2選1)', 0, 0, 0, 0, 4, 0, True, 4],
        ['校訂選修', '實習', '車輛微電腦控制實習', 0, 0, 2, 2, 0, 0, True, 4],
        ['校訂選修', '實習', '汽車美容實務 (2選1)', 0, 0, 0, 0, 0, 3, True, 3],
        ['校訂選修', '實習', '車輪定位檢修實習', 0, 0, 0, 0, 0, 4, True, 4],
        ['校訂選修', '實習', '噴射引擎實習', 0, 0, 0, 0, 0, 4, True, 4],
        ['校訂選修', '實習', '汽車塗裝實習', 0, 0, 0, 0, 4, 0, True, 4],
        ['校訂選修', '實習', '柴油引擎實習 (2選1)', 0, 0, 0, 0, 0, 4, True, 4],
        ['校訂選修', '實習', '汽車綜合實習 (2選1)', 0, 0, 0, 0, 4, 0, True, 4],
    ]

# --- 3. 側邊欄 ---
with st.sidebar:
    st.header("👤 學生資訊")
    student_id_name = st.text_input("座號 / 姓名", placeholder="例如：01 黃萬瑄")
    if st.button("🧹 清空所有勾選"):
        for k in list(st.session_state.keys()):
            if k.startswith("k_"): st.session_state[k] = False
        st.rerun()

# --- 4. 文字解析區 ---
with st.expander("📥 點此展開：貼上成績文字自動勾選"):
    paste_txt = st.text_area("請複製成績單文字貼於此：", height=100)
    if st.button("🚀 執行自動勾選"):
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
                            if row[2] in line:
                                if row[3+s_idx] > 0:
                                    st.session_state[f"k_{idx}_{s_idx}"] = True
            st.success("✅ 讀取完成！")

# --- 5. 學年分頁 ---
tabs = st.tabs(["高一階段", "高二階段", "高三階段"])

def render_year(tab_obj, s_idx):
    with tab_obj:
        for idx, row in enumerate(st.session_state.courses):
            c1, c2 = row[3+s_idx[0]], row[3+s_idx[1]]
            if c1 > 0 or c2 > 0:
                is_elective = "2選1" in row[2]
                elective_tag = '<span class="elective-info"> (二選一)</span>' if is_elective else ''
                st.markdown(f'<div class="course-card">{row[2]}{elective_tag}</div>', unsafe_allow_html=True)
                cols = st.columns(2)
                k1, k2 = f"k_{idx}_{s_idx[0]}", f"k_{idx}_{s_idx[1]}"
                if k1 not in st.session_state: st.session_state[k1] = False
                if k2 not in st.session_state: st.session_state[k2] = False
                if c1 > 0: cols[0].checkbox(f"上學期 ({c1})", key=k1)
                if c2 > 0: cols[1].checkbox(f"下學期 ({c2})", key=k2)

render_year(tabs[0], [0, 1])
render_year(tabs[1], [2, 3])
render_year(tabs[2], [4, 5])

# --- 6. 畢業檢核計算 ---
st.markdown("---")
stats_data = []
unpassed_list = []
sem_names = ["一上", "一下", "二上", "二下", "三上", "三下"]

for idx, row in enumerate(st.session_state.courses):
    earned = 0
    for s in range(6):
        if row[3+s] > 0:
            if st.session_state.get(f"k_{idx}_{s}", False):
                earned += row[3+s]
            else:
                unpassed_list.append(f"{row[2]} ({sem_names[s]} - {row[3+s]}學分)")
    stats_data.append({'cat': row[0], 'type': row[1], 'val': earned, 'pure': row[9]})

total_score = sum(x['val'] for x in stats_data)
dept_score = sum(x['val'] for x in stats_data if x['cat'] == '部定必修')
prof_score = sum(x['val'] for x in stats_data if x['type'] in ['專業', '實習'])
pure_score = sum(x['val'] for x in stats_data if x['pure'])

def bar(label, now, goal):
    st.write(f"**{label}**")
    color = "#27ae60" if now >= goal else "#e74c3c"
    st.markdown(f"<h3 style='color:{color}; margin:0;'>{now} / {goal}</h3>", unsafe_allow_html=True)
    st.progress(min(now/goal, 1.0) if goal > 0 else 0)

c_l, c_r = st.columns(2)
with c_l:
    bar("1. 總及格學分 (>=160)", total_score, 160)
    bar("2. 部定必修 (125之85% 門檻 106.3)", dept_score, 106.3)
with c_r:
    bar("3. 專業及實習科目 (>=60)", prof_score, 60)
    bar("4. 純實習科目 (>=30)", pure_score, 30)

# --- 7. 未修過清單 ---
st.markdown("### 🔍 未取得學分科目清單")
if unpassed_list:
    for item in unpassed_list:
        st.markdown(f'<div class="missing-card">❌ {item}</div>', unsafe_allow_html=True)
else:
    st.success("🎉 已達成目前所有勾選科目的及格要求！")

if total_score >= 160 and dept_score >= 106.3 and prof_score >= 60 and pure_score >= 30:
    st.balloons(); st.success(f"🎓 {student_id_name} 恭喜！已達成畢業門檻！")
