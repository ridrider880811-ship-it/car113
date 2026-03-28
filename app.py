import streamlit as st

# --- 1. 頁面配置 ---
st.set_page_config(page_title="汽車科畢業學分檢核", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"] { font-family: "Microsoft JhengHei", sans-serif; }
    .main-title { font-size: 2.2rem; font-weight: 800; text-align: center; color: #2c3e50; }
    .stProgress > div > div > div > div { background-color: #ff9f43; }
    .course-card { background-color: #f8f9fa; padding: 8px 12px; border-radius: 5px; border-left: 5px solid #3498db; margin-top: 10px; font-weight: bold; }
    .missing-card { color: #e74c3c; background-color: #fff5f5; padding: 5px; border-radius: 4px; margin-bottom: 3px; border-left: 3px solid #e74c3c; font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🚗 畢業學分清單</p>', unsafe_allow_html=True)
st.caption("製作人：羅章成老師")

# --- 2. 核心資料庫 (嚴格對照 113課綱新.pdf 逐行輸入) ---
if 'courses' not in st.session_state:
    st.session_state.courses = [
        # [類別, 屬性, 科目名稱, 一上, 一下, 二上, 二下, 三上, 三下, 是否純實習]
        # 部定必修 一般科目 (74學分)
        ['部定必修', '一般', '國語文', 3, 3, 3, 3, 2, 2, False],
        ['部定必修', '一般', '英語文', 2, 2, 2, 2, 2, 2, False],
        ['部定必修', '一般', '數學', 4, 4, 0, 0, 0, 0, False],
        ['部定必修', '一般', '歷史', 2, 0, 0, 0, 0, 0, False],
        ['部定必修', '一般', '地理', 0, 2, 0, 0, 0, 0, False],
        ['部定必修', '一般', '公民與社會', 0, 0, 2, 0, 0, 0, False],
        ['部定必修', '一般', '物理', 0, 0, 2, 2, 0, 0, False],
        ['部定必修', '一般', '化學', 2, 0, 0, 0, 0, 0, False],
        ['部定必修', '一般', '音樂', 0, 0, 1, 0, 0, 0, False],
        ['部定必修', '一般', '美術', 2, 0, 0, 0, 0, 0, False],
        ['部定必修', '一般', '法律與生活', 0, 0, 0, 0, 2, 1, False],
        ['部定必修', '一般', '資訊科技', 0, 2, 0, 0, 0, 0, False],
        ['部定必修', '一般', '健康與護理', 2, 0, 0, 0, 0, 0, False],
        ['部定必修', '一般', '體育', 2, 2, 2, 2, 2, 2, False],
        ['部定必修', '一般', '全民國防教育', 1, 1, 0, 0, 0, 0, False],
        ['部定必修', '一般', '本土語/臺灣手語', 0, 0, 0, 2, 0, 0, False],
        
        # 部定必修 專業及實習科目 (51學分)
        ['部定必修', '專業', '應用力學', 0, 0, 2, 0, 0, 0, False],
        ['部定必修', '專業', '機件原理', 0, 0, 3, 0, 0, 0, False],
        ['部定必修', '專業', '引擎原理', 3, 0, 0, 0, 0, 0, False],
        ['部定必修', '專業', '底盤原理', 0, 4, 0, 0, 0, 0, False],
        ['部定必修', '實習', '機電製圖實習', 2, 2, 0, 0, 0, 0, True],
        ['部定必修', '實習', '引擎實習', 4, 0, 0, 0, 0, 0, True],
        ['部定必修', '實習', '底盤實習', 0, 4, 0, 0, 0, 0, True],
        ['部定必修', '實習', '電工電子實習', 0, 0, 3, 0, 0, 0, True],
        ['部定必修', '實習', '機器腳踏車基礎實習', 0, 0, 3, 0, 0, 0, True],
        ['部定必修', '實習', '機器腳踏車檢修實習', 0, 3, 0, 0, 0, 0, True],
        ['部定必修', '實習', '電系實習', 0, 0, 0, 3, 0, 0, True],
        ['部定必修', '實習', '車輛底盤檢修實習', 0, 0, 0, 4, 0, 0, True],
        ['部定必修', '實習', '機械工作法及實習', 0, 0, 0, 0, 3, 3, True],
        ['部定必修', '實習', '車輛空調檢修實習', 0, 0, 0, 0, 3, 0, True],
        ['部定必修', '實習', '車身電器系統綜合檢修實習', 0, 0, 0, 0, 4, 0, True],

        # 校訂必修 (26學分)
        ['校訂必修', '一般', '青少年身心健康管理', 0, 2, 0, 0, 0, 0, False],
        ['校訂必修', '一般', '數學(校訂)', 0, 0, 2, 2, 2, 2, False], # 這是關鍵的校訂必修數學
        ['校訂必修', '一般', '計算機概論', 2, 0, 0, 0, 0, 0, False],
        ['校訂必修', '一般', '閱讀與寫作', 0, 0, 0, 0, 1, 1, False],
        ['校訂必修', '專業', '汽車工業英文', 0, 0, 0, 0, 2, 0, False],
        ['校訂必修', '專業', '電動車概論', 0, 0, 0, 2, 0, 0, False],
        ['校訂必修', '實習', '電動機車實習', 0, 0, 0, 0, 0, 2, True],
        ['校訂必修', '實習', '專題實作', 0, 0, 0, 0, 2, 2, True],
        ['校訂必修', '實習', '訊號量測與分析實習', 0, 0, 0, 0, 2, 2, True],

        # 校訂選修
        ['校訂選修', '一般', '兵家的智慧', 0, 0, 1, 0, 0, 0, False],
        ['校訂選修', '一般', '野外求生', 0, 0, 0, 1, 0, 0, False],
        ['校訂選修', '一般', '數學演習', 0, 0, 0, 0, 2, 2, False],
        ['校訂選修', '專業', '交通安全與法規', 0, 0, 0, 0, 1, 0, False],
        ['校訂選修', '專業', '汽車新式裝備', 0, 0, 0, 0, 0, 1, False],
        ['校訂選修', '專業', '先進車輛電控概論', 0, 0, 0, 0, 3, 0, False],
        ['校訂選修', '實習', '汽車檢驗實習', 0, 0, 0, 0, 4, 0, True],
        ['校訂選修', '實習', '汽車綜合實習', 0, 0, 0, 0, 4, 0, True],
        ['校訂選修', '實習', '汽車定期保養實習', 0, 0, 0, 0, 4, 0, True],
        ['校訂選修', '實習', '汽車塗裝實習', 0, 0, 0, 0, 4, 0, True],
        ['校訂選修', '實習', '車輛儀器檢修實務', 0, 0, 0, 0, 0, 3, True],
        ['校訂選修', '實習', '汽車美容實務', 0, 0, 0, 0, 0, 3, True],
        ['校訂選修', '實習', '車輪定位檢修實習', 0, 0, 0, 0, 0, 4, True],
        ['校訂選修', '實習', '噴射引擎實習', 0, 0, 0, 0, 0, 4, True],
        ['校訂選修', '實習', '柴油引擎實習', 0, 0, 0, 0, 0, 4, True],
        ['校訂選修', '實習', '車輛微電腦控制實習', 0, 0, 2, 2, 0, 0, True],
        ['校訂選修', '一般', '原住民族語課程', 0, 0, 2, 2, 2, 2, False],
    ]

# --- 3. 側邊欄與資訊 ---
with st.sidebar:
    st.header("👤 學生資訊")
    st_info = st.text_input("座號 / 姓名", placeholder="例如：32 王茂鈞")
    if st.button("🧹 清空所有勾選"):
        for k in list(st.session_state.keys()):
            if k.startswith("k_"): st.session_state[k] = False
        st.rerun()

# --- 4. 解析功能 (下拉式) ---
with st.expander("📥 點此展開：貼上成績文字自動勾選"):
    paste_txt = st.text_area("請貼上歷年成績文字：", height=150)
    if st.button("🚀 執行自動勾選"):
        if paste_txt:
            is_y1 = "一年級" in paste_txt
            is_y2 = "二年級" in paste_txt
            is_y3 = "三年級" in paste_txt
            for line in paste_txt.split('\n'):
                for idx, row in enumerate(st.session_state.courses):
                    if row[2][:2] in line: # 模糊比對前兩字
                        if is_y1:
                            if row[3]>0: st.session_state[f"k_{idx}_0"] = True
                            if row[4]>0: st.session_state[f"k_{idx}_1"] = True
                        if is_y2:
                            if row[5]>0: st.session_state[f"k_{idx}_2"] = True
                            if row[6]>0: st.session_state[f"k_{idx}_3"] = True
                        if is_y3:
                            if row[7]>0: st.session_state[f"k_{idx}_4"] = True
                            if row[8]>0: st.session_state[f"k_{idx}_5"] = True
            st.success("✅ 解析完成！")

# --- 5. 學分勾選分頁 ---
tabs = st.tabs(["高一階段", "高二階段", "高三階段"])
sem_names = ["一上", "一下", "二上", "二下", "三上", "三下"]

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

# --- 6. 統計看板 ---
st.markdown("---")
stats = []
unpassed = []
for idx, row in enumerate(st.session_state.courses):
    e_val = 0
    for s in range(6):
        if row[3+s] > 0:
            if st.session_state.get(f"k_{idx}_{s}", False): e_val += row[3+s]
            else: unpassed.append(f"❌ {row[2]} ({sem_names[s]})")
    stats.append({'cat': row[0], 'type': row[1], 'val': e_val, 'pure': row[9]})

t_s = sum(x['val'] for x in stats)
d_s = sum(x['val'] for x in stats if x['cat'] == '部定必修')
p_s = sum(x['val'] for x in stats if x['type'] in ['專業', '實習'])
s_s = sum(x['val'] for x in stats if x['pure'])

def bar(label, now, goal):
    st.write(f"**{label}**")
    color = "#27ae60" if now >= goal else "#e74c3c"
    st.markdown(f"<h3 style='color:{color}; margin:0;'>{now} / {goal}</h3>", unsafe_allow_html=True)
    st.progress(min(now/goal, 1.0) if goal > 0 else 0)

c_l, c_r = st.columns(2)
with c_l:
    bar("1. 總學分 (>=160)", t_s, 160)
    bar("2. 部定必修 (>=106.3)", d_s, 106.3)
with c_r:
    bar("3. 專業及實習科目 (>=60)", p_s, 60)
    bar("4. 純實習科目 (>=30)", s_s, 30)

# --- 7. 未取得學分清單 (下拉式) ---
with st.expander("🔍 點此展開：未取得學分科目清單"):
    if unpassed:
        for item in unpassed: st.markdown(f'<div class="missing-card">{item}</div>', unsafe_allow_html=True)
    else: st.success("🎉 恭喜！所有科目皆已及格。")

if t_s >= 160 and d_s >= 106.3 and p_s >= 60 and s_s >= 30:
    st.balloons(); st.success(f"🎓 {st_info} 恭喜！符合畢業標準。")
