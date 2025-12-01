import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Arabic support for matplotlib text (gauges only)
import arabic_reshaper
from bidi.algorithm import get_display

def rtl(text: str) -> str:
    return get_display(arabic_reshaper.reshape(text))

# ---------- Scoring helpers ----------

def act_level(score: int) -> str:
    if score <= 15:
        return "Poorly controlled"
    elif score <= 19:
        return "Partially controlled"
    else:
        return "Well controlled"

def airq_level(score: int) -> str:
    if score <= 1:
        return "Well controlled"
    elif score <= 4:
        return "Not well controlled"
    else:
        return "Poorly controlled"

# ---------- ACT Gauge (English) ----------

def draw_act_gauge_en(score: int):
    fig, ax = plt.subplots(figsize=(10, 2))
    xs = np.linspace(5, 25, 500)
    cmap = LinearSegmentedColormap.from_list("act", ["#EF4444", "#FDE047", "#3B82F6"])

    for i in range(len(xs)-1):
        ax.axvspan(xs[i], xs[i+1], 0.4, 0.6, color=cmap(i/len(xs)), alpha=0.9)

    ax.axvline(15.5, 0.35, 0.65, color="white", linewidth=1)
    ax.axvline(19.5, 0.35, 0.65, color="white", linewidth=1)
    ax.axvline(score, 0.35, 0.65, color="black", linewidth=4)

    ax.set_xticks(range(5, 26))
    ax.set_xticklabels(range(5, 26), fontsize=6)

    ax.text(10, 0.75, "Poorly controlled", ha="center", fontsize=10)
    ax.text(17.5, 0.75, "Partially controlled", ha="center", fontsize=10)
    ax.text(23, 0.75, "Well controlled", ha="center", fontsize=10)

    ax.set_xlim(5, 25)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("ACT score (5–25)")
    for s in ax.spines.values():
        s.set_visible(False)

    st.pyplot(fig)

# ---------- ACT Gauge (Arabic) ----------

def draw_act_gauge_ar(score: int):
    fig, ax = plt.subplots(figsize=(10, 2))
    xs = np.linspace(5, 25, 500)
    cmap = LinearSegmentedColormap.from_list("act", ["#EF4444", "#FDE047", "#3B82F6"])

    for i in range(len(xs)-1):
        ax.axvspan(xs[i], xs[i+1], 0.4, 0.6, color=cmap(i/len(xs)), alpha=0.9)

    ax.axvline(15.5, 0.35, 0.65, color="white", linewidth=1)
    ax.axvline(19.5, 0.35, 0.65, color="white", linewidth=1)
    ax.axvline(score, 0.35, 0.65, color="black", linewidth=4)

    ax.set_xticks(range(5, 26))
    ax.set_xticklabels(range(5, 26), fontsize=6)

    ax.text(10, 0.75, rtl("سيطرة ضعيفة"), ha="center", fontsize=12)
    ax.text(17.5, 0.75, rtl("سيطرة جزئية"), ha="center", fontsize=12)
    ax.text(23, 0.75, rtl("سيطرة جيدة"), ha="center", fontsize=12)

    ax.set_xlim(5, 25)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel(rtl("مجموع النقاط (5–25)"))
    for s in ax.spines.values():
        s.set_visible(False)

    st.pyplot(fig)

# ---------- AIRQ Gauge (English + Arabic) ----------

def draw_airq_gauge(score: int, arabic=False):
    fig, ax = plt.subplots(figsize=(10, 2))
    xs = np.linspace(0, 10, 500)

    # Blue → Yellow → Red = good → medium → poor
    cmap = LinearSegmentedColormap.from_list(
        "airq", ["#3B82F6", "#FDE047", "#EF4444"]
    )

    for i in range(len(xs)-1):
        ax.axvspan(xs[i], xs[i+1], 0.4, 0.6, color=cmap(i/len(xs)), alpha=0.9)

    ax.axvline(1.5, 0.35, 0.65, color="white", linewidth=1)
    ax.axvline(4.5, 0.35, 0.65, color="white", linewidth=1)
    ax.axvline(score, 0.35, 0.65, color="black", linewidth=4)

    ax.set_xticks(range(0, 11))
    ax.set_xticklabels(range(0, 11), fontsize=6)

    if not arabic:
        ax.text(0.5, 0.75, "Well controlled", ha="center", fontsize=10)
        ax.text(3.0, 0.75, "Not well controlled", ha="center", fontsize=10)
        ax.text(7.5, 0.75, "Poorly controlled", ha="center", fontsize=10)
        ax.set_xlabel("AIRQ score (0–10)")
    else:
        ax.text(0.5, 0.75, rtl("سيطرة جيدة"), ha="center", fontsize=12)
        ax.text(3.0, 0.75, rtl("سيطرة غير جيدة"), ha="center", fontsize=12)
        ax.text(7.5, 0.75, rtl("سيطرة ضعيفة"), ha="center", fontsize=12)
        ax.set_xlabel(rtl("مجموع النقاط (0–10)"))

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    st.pyplot(fig)

# ---------- Streamlit Base Setup ----------

st.set_page_config(page_title="Asthma Tools", layout="wide")

rtl_css = """
<style>
.arabic-container { direction: rtl; text-align: right; }
div[role='radiogroup'] label {
    direction: rtl !important;
    text-align: right !important;
}
</style>
"""
st.markdown(rtl_css, unsafe_allow_html=True)

st.title("Asthma Control & Risk Assessment Tools")

tab_act_en, tab_act_ar, tab_airq_en, tab_airq_ar = st.tabs(
    ["ACT – English", "ACT – العربية", "AIRQ – English", "AIRQ – العربية"]
)

# ---------- ACT English Tab ----------

with tab_act_en:
    st.header("Asthma Control Test (ACT) – English")
    st.markdown("""
INSTRUCTIONS  
Use in patients ≥12 years who have been diagnosed with asthma.
""")
    st.markdown("""
Please answer each question based on the **last 4 weeks**.
""")

    q1 = st.radio("1) How much of the time has asthma limited your activity?",
                  ["All of the time","Most of the time","Some of the time","A little of the time","None of the time"])
    q2 = st.radio("2) How often have you had shortness of breath?",
                  ["More than once a day","Once a day","3 to 6 times a week","Once or twice a week","Not at all"])
    q3 = st.radio("3) How often have asthma symptoms woken you at night?",
                  ["4 or more nights a week","2 to 3 nights a week","Once a week","Once or Twice","Not at all"])
    q4 = st.radio("4) How often have you used your rescue inhaler?",
                  ["3 or more times per day","Once or twice per day","2 or 3 times per week","Once a week or less","Not at all"])
    q5 = st.radio("5) How would you rate your asthma control?",
                  ["Not Controlled at all","Poorly Controlled","Somewhat Controlled","Well Controlled","Completely Controlled"])

    s1 = ["All of the time","Most of the time","Some of the time","A little of the time","None of the time"].index(q1)+1
    s2 = ["More than once a day","Once a day","3 to 6 times a week","Once or twice a week","Not at all"].index(q2)+1
    s3 = ["4 or more nights a week","2 to 3 nights a week","Once a week","Once or Twice","Not at all"].index(q3)+1
    s4 = ["3 or more times per day","Once or twice per day","2 or 3 times per week","Once a week or less","Not at all"].index(q4)+1
    s5 = ["Not Controlled at all","Poorly Controlled","Somewhat Controlled","Well Controlled","Completely Controlled"].index(q5)+1

    act_en_score = s1 + s2 + s3 + s4 + s5
    st.markdown(f"### ACT Score: **{act_en_score}** — **{act_level(act_en_score)}**")
    draw_act_gauge_en(act_en_score)

    st.markdown("---")
    st.markdown("### References (ACT)")
    st.markdown("""
1. Nathan RA, Sorkness CA, Kosinski M, Schatz M, Li JT, Marcus P, et al.  
   *Development of the Asthma Control Test: a Survey for Assessing Asthma Control.*  
   J Allergy Clin Immunol. 2004;113(1):59–65.

2. Schatz M, Sorkness CA, Li JT, Marcus P, Murray JJ, Nathan RA, Kosinski M, Pendergraft TB, Jhingran P.  
   *Asthma Control Test: reliability, validity, and responsiveness in patients not previously followed by asthma specialists.*  
   J Allergy Clin Immunol. 2006;117:549–56.

3. Liu AH, Zeiger R, Sorkness C, et al.  
   *Development and cross-sectional validation of the Childhood Asthma Control Test.*  
   J Allergy Clin Immunol. 2007;119(4):817–825.

4. Lababidi H, Hijaoui A, Zarzour M.  
   *Validation of the Arabic version of the asthma control test.*  
   Ann Thorac Med. 2008;3(2):44–47.
""")

# ---------- ACT Arabic Tab ----------

with tab_act_ar:
    st.markdown("<div class='arabic-container'>", unsafe_allow_html=True)

    st.header("اختبار السيطرة على الربو (ACT) – العربية")
    st.markdown("""
التعليمات  
يُستخدم لدى المرضى الذين تبلغ أعمارهم ١٢ عامًا فأكثر والمُشخَّصين بالربو.
""")
    st.markdown("خلال الأسابيع الأربعة الماضية، يرجى اختيار الإجابة المناسبة.")

    q1_ar = st.radio("1) خلال الأربعة أسابيع الأخيرة، كم من الوقت منعك الربو من القيام بنشاطك؟",
                     ["كل الأوقات","أغلب الأوقات","أحياناً","أوقات قليلة","لم يحصل أبداً"])
    q2_ar = st.radio("2) خلال الأربعة أسابيع الماضية، كم مرة حصل لك ضيق نفس؟",
                     ["أكثر من مرة في اليوم","مرة واحدة في اليوم","من 3 إلى 6 مرات في الأسبوع","مرة أو مرتين في الأسبوع","لم يحصل أبداً"])
    q3_ar = st.radio("3) كم مرة أيقظتك أعراض الربو أثناء الليل؟",
                     ["4 ليال أو أكثر","2 إلى 3 مرات","مرة واحدة","مرة أو مرتين","لم يحصل أبداً"])
    q4_ar = st.radio("4) كم مرة استخدمت بخاخ الأزمات؟",
                     ["3 مرات أو أكثر","مرة أو مرتين","2 أو 3 مرات في الأسبوع","مرة واحدة في الأسبوع أو أقل","لم يحصل أبداً"])
    q5_ar = st.radio("5) ما هو تقييمك للسيطرة على الربو؟",
                     ["تحكّم مفقود","تحكّم ضعيف","تحكّم متواضع","تحكّم جيد","تحكّم شامل"])

    s1_ar = ["كل الأوقات","أغلب الأوقات","أحياناً","أوقات قليلة","لم يحصل أبداً"].index(q1_ar)+1
    s2_ar = ["أكثر من مرة في اليوم","مرة واحدة في اليوم","من 3 إلى 6 مرات في الأسبوع","مرة أو مرتين في الأسبوع","لم يحصل أبداً"].index(q2_ar)+1
    s3_ar = ["4 ليال أو أكثر","2 إلى 3 مرات","مرة واحدة","مرة أو مرتين","لم يحصل أبداً"].index(q3_ar)+1
    s4_ar = ["3 مرات أو أكثر","مرة أو مرتين","2 أو 3 مرات في الأسبوع","مرة واحدة في الأسبوع أو أقل","لم يحصل أبداً"].index(q4_ar)+1
    s5_ar = ["تحكّم مفقود","تحكّم ضعيف","تحكّم متواضع","تحكّم جيد","تحكّم شامل"].index(q5_ar)+1

    act_ar_score = s1_ar + s2_ar + s3_ar + s4_ar + s5_ar

    st.markdown(f"### مجموع نقاط ACT: **{act_ar_score}** — **{rtl(act_level(act_ar_score))}**")
    draw_act_gauge_ar(act_ar_score)

    st.markdown("---")
    st.markdown("### المراجع (ACT)")
    st.markdown("""
1. Nathan RA وآخرون.  
   *Development of the Asthma Control Test: a Survey for Assessing Asthma Control.*  
   J Allergy Clin Immunol. 2004;113(1):59–65.

2. Schatz M وآخرون.  
   *Asthma Control Test: reliability, validity, and responsiveness in patients not previously followed by asthma specialists.*  
   J Allergy Clin Immunol. 2006;117:549–56.

3. Liu AH وآخرون.  
   *Development and cross-sectional validation of the Childhood Asthma Control Test.*  
   J Allergy Clin Immunol. 2007;119(4):817–825.

4. Lababidi H، Hijaoui A، Zarzour M.  
   *Validation of the Arabic version of the asthma control test.*  
   Ann Thorac Med. 2008;3(2):44–47.
""")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- AIRQ English Tab ----------

with tab_airq_en:
    st.header("Asthma Impairment and Risk Questionnaire (AIRQ) – English")
    st.markdown("""
INSTRUCTIONS  
Use in patients ≥12 years who have been diagnosed with asthma.
""")
    st.markdown("""
Each Yes = 1 point  
Each No = 0 points  
Total score = 0–10.
""")

    q = []
    q.append(st.radio("1) More than 4 days of daytime symptoms?", ["No","Yes"]))
    q.append(st.radio("2) Woken from sleep more than once?", ["No","Yes"]))
    q.append(st.radio("3) Limited daily activities?", ["No","Yes"]))
    q.append(st.radio("4) Used rescue inhaler every day?", ["No","Yes"]))

    st.markdown("### In the past 2 weeks:")
    q.append(st.radio("5) Limited social activities?", ["No","Yes"]))
    q.append(st.radio("6) Limited ability to exercise?", ["No","Yes"]))
    q.append(st.radio("7) Felt asthma was hard to control?", ["No","Yes"]))

    st.markdown("### In the past 12 months:")
    q.append(st.radio("8) Required steroid pills or shots?", ["No","Yes"]))
    q.append(st.radio("9) ER or urgent visits?", ["No","Yes"]))
    q.append(st.radio("10) Hospital overnight stay?", ["No","Yes"]))

    airq_score = sum(1 for x in q if x == "Yes")

    st.markdown(f"### AIRQ Score: **{airq_score}** — **{airq_level(airq_score)}**")
    draw_airq_gauge(airq_score, arabic=False)

    st.markdown("---")
    st.markdown("### References (AIRQ)")
    st.markdown("""
1. Murphy KR, Chipps B, Beuther DA, et al.  
   *Development of the asthma impairment and risk questionnaire (AIRQ): a composite control measure.*  
   J Allergy Clin Immunol Pract. 2020;8(7):2263–2274.e5.

2. Reibman J, Chipps BE, Zeiger RS, et al.  
   *Relationship between asthma control as measured by the Asthma Impairment and Risk Questionnaire (AIRQ) and patient perception of disease status, health-related quality of life, and treatment adherence.*  
   J Asthma Allergy. 2023;16:59–72.
""")

# ---------- AIRQ Arabic Tab ----------

with tab_airq_ar:
    st.markdown("<div class='arabic-container'>", unsafe_allow_html=True)

    st.header("استبيان اعتلال ومخاطر الربو (AIRQ) – العربية")
    st.markdown("""
التعليمات  
يُستخدم لدى المرضى الذين تبلغ أعمارهم ١٢ عامًا فأكثر والمُشخَّصين بالربو.
""")
    st.markdown("""
كل إجابة "نعم" = 1 نقطة  
وكل إجابة "لا" = 0 نقاط  
المجموع من 0 إلى 10.
""")

    q = []
    q.append(st.radio("1) هل أزعجتك الأعراض نهارًا لأكثر من 4 أيام؟", ["لا","نعم"]))
    q.append(st.radio("2) هل أيقظتك الأعراض من النوم أكثر من مرة؟", ["لا","نعم"]))
    q.append(st.radio("3) هل قلّصت الأعراض أنشطتك اليومية؟", ["لا","نعم"]))
    q.append(st.radio("4) هل استخدمت بخاخ الطوارئ يوميًا؟", ["لا","نعم"]))

    st.markdown("### خلال الأسبوعين الماضيين:")
    q.append(st.radio("5) هل حدّت الأعراض من أنشطتك الاجتماعية؟", ["لا","نعم"]))
    q.append(st.radio("6) هل حدّت من قدرتك على ممارسة الرياضة؟", ["لا","نعم"]))
    q.append(st.radio("7) هل شعرت بصعوبة في السيطرة على الربو؟", ["لا","نعم"]))

    st.markdown("### خلال 12 شهرًا الماضية:")
    q.append(st.radio("8) هل احتجت إلى حبوب أو حقن كورتيزون؟", ["لا","نعم"]))
    q.append(st.radio("9) هل احتجت إلى زيارة الطوارئ؟", ["لا","نعم"]))
    q.append(st.radio("10) هل مكثت في المستشفى طوال الليل؟", ["لا","نعم"]))

    airq_score = sum(1 for x in q if x == "نعم")

    st.markdown(f"### مجموع نقاط AIRQ: **{airq_score}** — **{rtl(airq_level(airq_score))}**")
    draw_airq_gauge(airq_score, arabic=True)

    st.markdown("---")
    st.markdown("### المراجع (AIRQ)")
    st.markdown("""
1. Murphy KR وآخرون.  
   *Development of the asthma impairment and risk questionnaire (AIRQ): a composite control measure.*  
   J Allergy Clin Immunol Pract. 2020;8(7):2263–2274.e5.

2. Reibman J وآخرون.  
   *Relationship between asthma control as measured by the Asthma Impairment and Risk Questionnaire (AIRQ) and patient perception of disease status, health-related quality of life, and treatment adherence.*  
   J Asthma Allergy. 2023;16:59–72.
""")

    st.markdown("</div>", unsafe_allow_html=True)
