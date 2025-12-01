import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Arabic support for matplotlib text
import arabic_reshaper
from bidi.algorithm import get_display

def rtl(text: str) -> str:
    """Return correctly shaped RTL Arabic text for matplotlib."""
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

# ---------- ACT Gauges (English & Arabic) ----------

def draw_act_gauge_en(score: int):
    fig, ax = plt.subplots(figsize=(10, 2))
    xmin, xmax = 5, 25
    xs = np.linspace(xmin, xmax, 500)

    cmap = LinearSegmentedColormap.from_list(
        "act_gradient",
        ["#EF4444", "#FDE047", "#3B82F6"]   # Red → Yellow → Blue
    )

    for i in range(len(xs)-1):
        ax.axvspan(xs[i], xs[i+1], 0.4, 0.6, color=cmap(i/len(xs)), alpha=0.9)

    ax.axvline(15.5, 0.35, 0.65, color="white", linewidth=1)
    ax.axvline(19.5, 0.35, 0.65, color="white", linewidth=1)
    ax.axvline(score, 0.35, 0.65, color="white", linewidth=4)

    ax.set_xticks(range(5, 26))
    ax.set_xticklabels(range(5, 26), fontsize=6)

    ax.text(10, 0.75, "Poorly controlled", ha="center", fontsize=10)
    ax.text(17.5, 0.75, "Partially controlled", ha="center", fontsize=10)
    ax.text(23, 0.75, "Well controlled", ha="center", fontsize=10)

    ax.set_xlim(xmin, xmax)
    ax.set_yticks([])
    ax.set_xlabel("ACT score (5–25)")

    for spine in ax.spines.values():
        spine.set_visible(False)

    st.pyplot(fig)

def draw_act_gauge_ar(score: int):
    fig, ax = plt.subplots(figsize=(10, 2))
    xmin, xmax = 5, 25
    xs = np.linspace(xmin, xmax, 500)

    cmap = LinearSegmentedColormap.from_list(
        "act_gradient",
        ["#EF4444", "#FDE047", "#3B82F6"]
    )

    for i in range(len(xs)-1):
        ax.axvspan(xs[i], xs[i+1], 0.4, 0.6, color=cmap(i/len(xs)), alpha=0.9)

    ax.axvline(15.5, 0.35, 0.65, color="white", linewidth=1)
    ax.axvline(19.5, 0.35, 0.65, color="white", linewidth=1)
    ax.axvline(score, 0.35, 0.65, color="white", linewidth=4)

    ax.set_xticks(range(5, 26))
    ax.set_xticklabels(range(5, 26), fontsize=6)

    ax.text(10, 0.75, rtl("سيطرة ضعيفة"), ha="center", fontsize=12)
    ax.text(17.5, 0.75, rtl("سيطرة جزئية"), ha="center", fontsize=12)
    ax.text(23, 0.75, rtl("سيطرة جيدة"), ha="center", fontsize=12)

    ax.set_xlim(xmin, xmax)
    ax.set_yticks([])
    ax.set_xlabel(rtl("مجموع نقاط ACT (5–25)"))

    for spine in ax.spines.values():
        spine.set_visible(False)

    st.pyplot(fig)

# ---------- AIRQ Gauge (English & Arabic) ----------

def draw_airq_gauge(score: int, arabic: bool=False):
    fig, ax = plt.subplots(figsize=(10, 2))
    xmin, xmax = 0, 10
    xs = np.linspace(xmin, xmax, 500)

    # RED → YELLOW → BLUE (match ACT)
    cmap = LinearSegmentedColormap.from_list(
        "airq_gradient",
        ["#EF4444", "#FDE047", "#3B82F6"]
    )

    for i in range(len(xs)-1):
        ax.axvspan(xs[i], xs[i+1], 0.4, 0.6, color=cmap(i/len(xs)), alpha=0.9)

    ax.axvline(1.5, 0.35, 0.65, color="white", linewidth=1)
    ax.axvline(4.5, 0.35, 0.65, color="white", linewidth=1)
    ax.axvline(score, 0.35, 0.65, color="white", linewidth=4)

    ax.set_xticks(range(0, 11))
    ax.set_xticklabels(range(0, 11), fontsize=6)

    if arabic:
        ax.text(0.5, 0.75, rtl("سيطرة ضعيفة جداً"), ha="center", fontsize=12)
        ax.text(3.0, 0.75, rtl("سيطرة غير جيدة"), ha="center", fontsize=12)
        ax.text(7.5, 0.75, rtl("سيطرة جيدة"), ha="center", fontsize=12)
        ax.set_xlabel(rtl("مجموع نقاط AIRQ (0–10)"))
    else:
        ax.text(0.5, 0.75, "Poorly controlled", ha="center", fontsize=10)
        ax.text(3.0, 0.75, "Not well controlled", ha="center", fontsize=10)
        ax.text(7.5, 0.75, "Well controlled", ha="center", fontsize=10)
        ax.set_xlabel("AIRQ score (0–10)")

    ax.set_xlim(xmin, xmax)
    ax.set_yticks([])

    for spine in ax.spines.values():
        spine.set_visible(False)

    st.pyplot(fig)

# ---------- Streamlit Setup ----------

st.set_page_config(page_title="Asthma Tools", layout="wide")

# Add RTL CSS for Arabic tabs
rtl_css = """
<style>
.arabic-container {
    direction: rtl;
    text-align: right;
}
div[role='radiogroup'] label {
    direction: rtl !important;
    text-align: right !important;
}
</style>
"""
st.markdown(rtl_css, unsafe_allow_html=True)

st.title("Asthma Control & Risk Tools")

tab_act_en, tab_act_ar, tab_airq_en, tab_airq_ar = st.tabs(
    ["ACT – English", "ACT – العربية", "AIRQ – English", "AIRQ – العربية"]
)

# ---------- ACT English Tab ----------
with tab_act_en:
    st.header("Asthma Control Test (ACT) – English")
    st.markdown("""
Please answer each question based on your symptoms during the **last 4 weeks**.
Each answer is scored from 1 to 5; higher total scores indicate better asthma control.
""")

    q1 = st.radio("1) During the last 4 weeks, how much of the time has your asthma kept you from getting as much done at work, school or home?",
        ["All of the time","Most of the time","Some of the time","A little of the time","None of the time"])
    q2 = st.radio("2) During the last 4 weeks, how often have you had shortness of breath?",
        ["More than once a day","Once a day","3 to 6 times a week","Once or twice a week","Not at all"])
    q3 = st.radio("3) During the last 4 weeks, how often have your asthma symptoms woken you up at night or earlier than usual in the morning?",
        ["4 or more nights a week","2 to 3 nights a week","Once a week","Once or Twice","Not at all"])
    q4 = st.radio("4) During the last 4 weeks, how often have you used your rescue inhaler or nebuliser medication?",
        ["3 or more times per day","Once or twice per day","2 or 3 times per week","Once a week or less","Not at all"])
    q5 = st.radio("5) How would you rate your asthma control during the last 4 weeks?",
        ["Not Controlled at all","Poorly Controlled","Somewhat Controlled","Well Controlled","Completely Controlled"])

    score = [1,2,3,4,5][ ["All of the time","Most of the time","Some of the time","A little of the time","None of the time"].index(q1) ] + \
             [1,2,3,4,5][ ["More than once a day","Once a day","3 to 6 times a week","Once or twice a week","Not at all"].index(q2) ] + \
             [1,2,3,4,5][ ["4 or more nights a week","2 to 3 nights a week","Once a week","Once or Twice","Not at all"].index(q3) ] + \
             [1,2,3,4,5][ ["3 or more times per day","Once or twice per day","2 or 3 times per week","Once a week or less","Not at all"].index(q4) ] + \
             [1,2,3,4,5][ ["Not Controlled at all","Poorly Controlled","Somewhat Controlled","Well Controlled","Completely Controlled"].index(q5) ]

    st.markdown(f"### ACT Score: **{score}** — **{act_level(score)}**")
    draw_act_gauge_en(score)

# ---------- ACT Arabic Tab ----------
with tab_act_ar:
    st.markdown("<div class='arabic-container'>", unsafe_allow_html=True)

    st.header("اختبار السيطرة على الربو (ACT) – العربية")

    st.markdown(
"""
اختبار السيطرة على الربو (من عمر 12 سنة فأكثر).  
خلال الأسابيع الأربعة الماضية، يرجى اختيار الإجابة التي تصف حالتك.
"""
    )

    q1 = st.radio("1) خلال الأربعة أسابيع الأخيرة، كم من الوقت منعك مرض الربو من القيام بنشاطك؟",
        ["كل الأوقات","أغلب الأوقات","أحياناً","أوقات قليلة","لم يحصل أبداً"])
    q2 = st.radio("2) خلال الأربعة أسابيع الماضية، كم مرة حصل لك ضيق نفس؟",
        ["أكثر من مرة في اليوم","مرة واحدة في اليوم","من 3 إلى 6 مرات في الأسبوع","مرة أو مرتين في الأسبوع","لم يحصل أبداً"])
    q3 = st.radio("3) خلال الأربعة أسابيع الماضية، كم مرة أيقظتك أعراض الربو أثناء الليل؟",
        ["4 ليال أو أكثر في الأسبوع","2 إلى 3 مرات في الأسبوع","مرة واحدة في الأسبوع","مرة أو مرتين","لم يحصل أبداً"])
    q4 = st.radio("4) خلال الأربعة أسابيع الماضية، كم مرة استخدمت بخاخة الأزمات؟",
        ["3 مرات أو أكثر في اليوم","مرة أو مرتين في اليوم","2 أو 3 مرات في الأسبوع","مرة واحدة في الأسبوع أو أقل","لم يحصل أبداً"])
    q5 = st.radio("5) خلال الأربعة أسابيع الماضية، ما هو تقييمك للسيطرة على الربو؟",
        ["تحكّم مفقود","تحكّم ضعيف","تحكّم متواضع","تحكّم جيد","تحكّم شامل"])

    score = [1,2,3,4,5][ ["كل الأوقات","أغلب الأوقات","أحياناً","أوقات قليلة","لم يحصل أبداً"].index(q1) ] + \
             [1,2,3,4,5][ ["أكثر من مرة في اليوم","مرة واحدة في اليوم","من 3 إلى 6 مرات في الأسبوع","مرة أو مرتين في الأسبوع","لم يحصل أبداً"].index(q2) ] + \
             [1,2,3,4,5][ ["4 ليال أو أكثر في الأسبوع","2 إلى 3 مرات في الأسبوع","مرة واحدة في الأسبوع","مرة أو مرتين","لم يحصل أبداً"].index(q3) ] + \
             [1,2,3,4,5][ ["3 مرات أو أكثر في اليوم","مرة أو مرتين في اليوم","2 أو 3 مرات في الأسبوع","مرة واحدة في الأسبوع أو أقل","لم يحصل أبداً"].index(q4) ] + \
             [1,2,3,4,5][ ["تحكّم مفقود","تحكّم ضعيف","تحكّم متواضع","تحكّم جيد","تحكّم شامل"].index(q5) ]

    st.markdown(f"### مجموع نقاط ACT: **{score}** — **{rtl(act_level(score))}**")
    draw_act_gauge_ar(score)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- AIRQ English Tab ----------
with tab_airq_en:
    st.header("AIRQ – English")
    st.markdown("""
Each Yes = 1 point.  
Each No = 0 points.  
Total score = 0–10.
""")

    q = []
    q.append(st.radio("1) Bothered you during the day on more than 4 days?", ["No","Yes"]))
    q.append(st.radio("2) Woken you up from sleep more than 1 time?", ["No","Yes"]))
    q.append(st.radio("3) Limited the activities you want to do?", ["No","Yes"]))
    q.append(st.radio("4) Required your rescue inhaler every day?", ["No","Yes"]))

    st.markdown("### In the past 2 weeks:")
    q.append(st.radio("5) Limited your social activities?", ["No","Yes"]))
    q.append(st.radio("6) Limited your ability to exercise?", ["No","Yes"]))
    q.append(st.radio("7) Difficult to control your asthma?", ["No","Yes"]))

    st.markdown("### In the past 12 months:")
    q.append(st.radio("8) Required steroid pills or shots?", ["No","Yes"]))
    q.append(st.radio("9) Required ER or urgent care?", ["No","Yes"]))
    q.append(st.radio("10) Required hospital overnight stay?", ["No","Yes"]))

    score = sum([1 if ans=="Yes" else 0 for ans in q])
    st.markdown(f"### AIRQ Score: **{score}** — **{airq_level(score)}**")

    draw_airq_gauge(score, arabic=False)

# ---------- AIRQ Arabic Tab ----------
with tab_airq_ar:
    st.markdown("<div class='arabic-container'>", unsafe_allow_html=True)

    st.header("استبيان اعتلال ومخاطر الربو (AIRQ) – العربية")

    st.markdown("""
كل إجابة "نعم" = 1 نقطة  
وكل إجابة "لا" = 0.  
المجموع من 0 إلى 10.
""")

    q = []
    q.append(st.radio("1) هل أزعجتك خلال اليوم لأكثر من 4 أيام؟", ["لا","نعم"], horizontal=True))
    q.append(st.radio("2) هل أيقظك من النوم أكثر من مرة؟", ["لا","نعم"], horizontal=True))
    q.append(st.radio("3) هل قلّصت الأنشطة اليومية التي تريد القيام بها؟", ["لا","نعم"], horizontal=True))
    q.append(st.radio("4) هل استخدمت بخاخ الأزمات، أو جهاز الاستنشاق يوميًا؟", ["لا","نعم"], horizontal=True))

    st.markdown("### خلال الأسبوعين الماضيين:")
    q.append(st.radio("5) هل اضطررت للحد من أنشطتك الاجتماعية بسبب الربو؟", ["لا","نعم"], horizontal=True))
    q.append(st.radio("6) هل حدّ السعال أو الأزيز أو ضيق التنفس من قدرتك على ممارسة الرياضة؟", ["لا","نعم"], horizontal=True))
    q.append(st.radio("7) هل شعرت بصعوبة في السيطرة على الربو؟", ["لا","نعم"], horizontal=True))

    st.markdown("### خلال 12 شهرًا الماضية:")
    q.append(st.radio("8) هل تناولت حبوب كورتيزون أو حقن؟", ["لا","نعم"], horizontal=True))
    q.append(st.radio("9) هل اضطررت إلى زيارة الطوارئ؟", ["لا","نعم"], horizontal=True))
    q.append(st.radio("10) هل مكثت في المستشفى طوال الليل؟", ["لا","نعم"], horizontal=True))

    score = sum([1 if ans=="نعم" else 0 for ans in q])

    st.markdown(f"### مجموع نقاط AIRQ: **{score}** — **{rtl(airq_level(score))}**")

    draw_airq_gauge(score, arabic=True)
