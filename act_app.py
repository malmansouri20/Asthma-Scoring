import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# ---------- ACT scoring helper ----------
def act_level(score: int) -> str:
    if score <= 15:
        return "Poorly controlled"
    elif score <= 19:
        return "Partially controlled"
    else:
        return "Well controlled"

# ---------- AIRQ scoring helper ----------
def airq_level(score: int) -> str:
    if score <= 1:
        return "Well controlled"
    elif score <= 4:
        return "Not well controlled"
    else:
        return "Very poorly controlled"

# ---------- ACT gauge (5–25) ----------
def draw_act_gauge(score: int):
    fig, ax = plt.subplots(figsize=(10, 2))

    xmin, xmax = 5, 25
    xs = np.linspace(xmin, xmax, 500)

    # RED → YELLOW → BLUE gradient
    cmap = LinearSegmentedColormap.from_list(
        "act_gradient",
        ["#EF4444", "#FDE047", "#3B82F6"]  # Red → Yellow → Blue
    )

    for i in range(len(xs) - 1):
        x_start = xs[i]
        x_end = xs[i + 1]
        color = cmap(i / len(xs))
        ax.axvspan(x_start, x_end, 0.4, 0.6, color=color, alpha=0.9)

    # Vertical boundaries between categories
    ax.axvline(15.5, 0.35, 0.65, color="black", linewidth=1)
    ax.axvline(19.5, 0.35, 0.65, color="black", linewidth=1)

    # Score marker
    ax.axvline(score, 0.35, 0.65, color="black", linewidth=4)

    # Ticks 5–25
    ax.set_xticks(range(5, 26))
    ax.set_xticklabels(range(5, 26), fontsize=6)

    # Category labels
    ax.text(10,   0.75, "Poorly controlled",    ha="center", fontsize=10)
    ax.text(17.5, 0.75, "Partially controlled", ha="center", fontsize=10)
    ax.text(23,   0.75, "Well controlled",      ha="center", fontsize=10)

    ax.set_xlim(xmin, xmax)
    ax.set_yticks([])
    ax.set_xlabel("ACT score (5–25)")

    for spine in ax.spines.values():
        spine.set_visible(False)

    st.pyplot(fig)

# ---------- AIRQ gauge (0–10) ----------
def draw_airq_gauge(score: int, arabic: bool = False):
    fig, ax = plt.subplots(figsize=(10, 2))

    xmin, xmax = 0, 10
    xs = np.linspace(xmin, xmax, 500)

    # BLUE → YELLOW → RED gradient (low=good, high=bad)
    cmap = LinearSegmentedColormap.from_list(
        "airq_gradient",
        ["#3B82F6", "#FDE047", "#EF4444"]  # Blue → Yellow → Red
    )

    for i in range(len(xs) - 1):
        x_start = xs[i]
        x_end = xs[i + 1]
        color = cmap(i / len(xs))
        ax.axvspan(x_start, x_end, 0.4, 0.6, color=color, alpha=0.9)

    # Boundaries for 0–1 (well), 2–4 (not well), 5–10 (very poorly)
    ax.axvline(1.5, 0.35, 0.65, color="black", linewidth=1)
    ax.axvline(4.5, 0.35, 0.65, color="black", linewidth=1)

    # Score marker
    ax.axvline(score, 0.35, 0.65, color="black", linewidth=4)

    # Ticks 0–10
    ax.set_xticks(range(0, 11))
    ax.set_xticklabels(range(0, 11), fontsize=6)

    # Category labels
    if not arabic:
        ax.text(0.5,  0.75, "Well controlled",        ha="center", fontsize=10)
        ax.text(3.0,  0.75, "Not well controlled",    ha="center", fontsize=10)
        ax.text(7.5,  0.75, "Very poorly controlled", ha="center", fontsize=10)
    else:
        ax.text(0.5,  0.75, "سيطرة جيدة",         ha="center", fontsize=10)
        ax.text(3.0,  0.75, "سيطرة غير جيدة",      ha="center", fontsize=10)
        ax.text(7.5,  0.75, "سيطرة ضعيفة جدًا",    ha="center", fontsize=10)

    ax.set_xlim(xmin, xmax)
    ax.set_yticks([])
    ax.set_xlabel("AIRQ score (0–10)" if not arabic else "مجموع نقاط AIRQ (0–10)")

    for spine in ax.spines.values():
        spine.set_visible(False)

    st.pyplot(fig)

# ---------- Streamlit config ----------
st.set_page_config(page_title="Asthma Tools", layout="wide")
st.title("Asthma Control & Risk Tools")

tab_act_en, tab_act_ar, tab_airq_en, tab_airq_ar = st.tabs(
    ["ACT – English", "ACT – العربية", "AIRQ – English", "AIRQ – العربية"]
)

# ===================== ACT – ENGLISH =====================
with tab_act_en:
    st.header("Asthma Control Test (ACT) – English")

    st.markdown("""
Please answer each question based on your symptoms during the **last 4 weeks**.
Each answer is scored from 1 to 5; higher total scores indicate better asthma control.
""")

    # --- ACT EN questions ---
    q1_en = st.radio(
        "1) During the last 4 weeks, how much of the time has your asthma kept you from getting as much done at work, school or home?",
        options=[
            ("All of the time", 1),
            ("Most of the time", 2),
            ("Some of the time", 3),
            ("A little of the time", 4),
            ("None of the time", 5),
        ],
        format_func=lambda x: x[0]
    )[1]

    q2_en = st.radio(
        "2) During the last 4 weeks, how often have you had shortness of breath?",
        options=[
            ("More than once a day", 1),
            ("Once a day", 2),
            ("3 to 6 times a week", 3),
            ("Once or twice a week", 4),
            ("Not at all", 5),
        ],
        format_func=lambda x: x[0]
    )[1]

    q3_en = st.radio(
        "3) During the last 4 weeks, how often have your asthma symptoms (wheezing, coughing, shortness of breath, chest tightness or pain) woken you up at night or earlier than usual in the morning?",
        options=[
            ("4 or more nights a week", 1),
            ("2 to 3 nights a week", 2),
            ("Once a week", 3),
            ("Once or Twice", 4),
            ("Not at all", 5),
        ],
        format_func=lambda x: x[0]
    )[1]

    q4_en = st.radio(
        "4) During the last 4 weeks, how often have you used your rescue inhaler or nebuliser medication (such as salbutamol)?",
        options=[
            ("3 or more times per day", 1),
            ("Once or twice per day", 2),
            ("2 or 3 times per week", 3),
            ("Once a week or less", 4),
            ("Not at all", 5),
        ],
        format_func=lambda x: x[0]
    )[1]

    q5_en = st.radio(
        "5) How would you rate your asthma control during the last 4 weeks?",
        options=[
            ("Not Controlled at all", 1),
            ("Poorly Controlled", 2),
            ("Somewhat Controlled", 3),
            ("Well Controlled", 4),
            ("Completely Controlled", 5),
        ],
        format_func=lambda x: x[0]
    )[1]

    act_en_score = q1_en + q2_en + q3_en + q4_en + q5_en
    act_en_level = act_level(act_en_score)

    st.markdown(f"### ACT Score: **{act_en_score}** — **{act_en_level}**")
    st.caption("Possible score range: 5–25. Higher scores indicate better asthma control.")

    draw_act_gauge(act_en_score)

    st.markdown("---")
    st.markdown("### References (ACT)")
    st.markdown("""
1. **Nathan RA**, Sorkness CA, Kosinski M, Schatz M, Li JT, Marcus P, et al.  
   *Development of the Asthma Control Test: a Survey for Assessing Asthma Control.*  
   J Allergy Clin Immunol. 2004;113(1):59–65.

2. **Schatz M**, Sorkness CA, Li JT, Marcus P, Murray JJ, Nathan RA, Kosinski M, Pendergraft TB, Jhingran P.  
   *Asthma Control Test: reliability, validity, and responsiveness in patients not previously followed by asthma specialists.*  
   J Allergy Clin Immunol. 2006;117:549–56.

3. **Liu AH**, Zeiger R, Sorkness C, et al.  
   *Development and cross-sectional validation of the Childhood Asthma Control Test.*  
   J Allergy Clin Immunol. 2007;119(4):817–825. doi:10.1016/j.jaci.2006.12.662.

4. **Lababidi H**, Hijaoui A, Zarzour M.  
   *Validation of the Arabic version of the asthma control test.*  
   Ann Thorac Med. 2008;3(2):44–47. doi:10.4103/1817-1737.39635.
""")

# ===================== ACT – ARABIC =====================
with tab_act_ar:
    st.header("اختبار السيطرة على الربو (ACT) – العربية")

    st.markdown("""
إختبار السيطرة على الربو (من عُمْر 12 سنة فأكثر).  
خلال الأسابيع الأربعة الماضية، يرجى اختيار الإجابة التي تصف حالتك.
""")

    # Q1 Arabic
    q1_ar = st.radio(
        "1) خلال الأربعة أسابيع الأخيرة، كم من الوقت منعك مرض الربو من القیام بنشاطك في العمل أو المدرسة أو المنزل؟",
        options=[
            ("كل الأوقات", 1),
            ("أغلب الأوقات", 2),
            ("أحياناً", 3),
            ("أوقات قليلة", 4),
            ("لم يحصل أبداً", 5),
        ],
        format_func=lambda x: x[0]
    )[1]

    # Q2 Arabic
    q2_ar = st.radio(
        "2) خلال الأربعة أسابيع الماضية، كم مرة حصل لك ضيق نفس؟",
        options=[
            ("أكثر من مرة في اليوم", 1),
            ("مرة واحدة في اليوم", 2),
            ("من 3 إلى 6 مرات في الأسبوع", 3),
            ("مرة أو مرتين في الأسبوع", 4),
            ("لم يحصل أبداً", 5),
        ],
        format_func=lambda x: x[0]
    )[1]

    # Q3 Arabic
    q3_ar = st.radio(
        "3) خلال الأربعة أسابيع الماضية، كم مرة أيقظتك أعراض الربو (الصفير، السعال، ضيق تنفس، ضيق صدر أو ألم في الصدر) أثناء الليل أو في الصباح الباكر؟",
        options=[
            ("4 ليال أو أكثر في الأسبوع", 1),
            ("2 إلى 3 مرات في الأسبوع", 2),
            ("مرة واحدة في الأسبوع", 3),
            ("مرة أو مرتين", 4),
            ("لم يحصل أبداً", 5),
        ],
        format_func=lambda x: x[0]
    )[1]

    # Q4 Arabic
    q4_ar = st.radio(
        "4) خلال الأربعة أسابيع الماضية، كم مرة استخدمت بخاخة الأزمات (موسعات الشعب الهوائية)؟",
        options=[
            ("3 مرات أو أكثر في اليوم", 1),
            ("مرة واحدة أو مرتين في اليوم", 2),
            ("2 أو 3 مرات في الأسبوع", 3),
            ("مرة واحدة في الأسبوع أو أقل", 4),
            ("لم يحصل أبداً", 5),
        ],
        format_func=lambda x: x[0]
    )[1]

    # Q5 Arabic (note: scored from worst to best)
    q5_ar = st.radio(
        "5) خلال الأربعة أسابيع الماضية، ما هو تقييمك للسيطرة على الربو عندك؟",
        options=[
            ("تحكّم مفقود", 1),
            ("تحكّم ضعيف", 2),
            ("تحكّم متواضع", 3),
            ("تحكّم جيد", 4),
            ("تحكّم شامل", 5),
        ],
        format_func=lambda x: x[0]
    )[1]

    act_ar_score = q1_ar + q2_ar + q3_ar + q4_ar + q5_ar
    act_ar_level = act_level(act_ar_score)

    st.markdown(f"### مجموع نقاط ACT: **{act_ar_score}** — **{act_ar_level}**")
    st.caption("النطاق الممكن لمجموع النقاط: 5–25. كلما زادت النقاط دلّ ذلك على سيطرة أفضل على الربو.")

    draw_act_gauge(act_ar_score)

    st.markdown("---")
    st.markdown("### المراجع (ACT)")
    st.markdown("""
1. **Nathan RA** وآخرون.  
   *Development of the Asthma Control Test: a Survey for Assessing Asthma Control.*  
   J Allergy Clin Immunol. 2004;113(1):59–65.

2. **Schatz M** وآخرون.  
   *Asthma Control Test: reliability, validity, and responsiveness in patients not previously followed by asthma specialists.*  
   J Allergy Clin Immunol. 2006;117:549–56.

3. **Liu AH** وآخرون.  
   *Development and cross-sectional validation of the Childhood Asthma Control Test.*  
   J Allergy Clin Immunol. 2007;119(4):817–825.

4. **Lababidi H**, **Hijaoui A**, **Zarzour M**.  
   *Validation of the Arabic version of the asthma control test.*  
   Ann Thorac Med. 2008;3(2):44–47.
""")

# ===================== AIRQ – ENGLISH =====================
with tab_airq_en:
    st.header("Asthma Impairment and Risk Questionnaire (AIRQ™) – English")

    st.markdown("""
For each question, please select **Yes** or **No**.  
Each **Yes = 1 point**, **No = 0 points**.  
Total AIRQ score = 0–10.
""")

    st.markdown("#### In the past 2 weeks, has coughing, wheezing, shortness of breath, or chest tightness:")

    q1_airq_en = st.radio(
        "1) Bothered you during the day on more than 4 days?",
        options=[("No", 0), ("Yes", 1)], horizontal=True,
        format_func=lambda x: x[0]
    )[1]

    q2_airq_en = st.radio(
        "2) Woken you up from sleep more than 1 time?",
        options=[("No", 0), ("Yes", 1)], horizontal=True,
        format_func=lambda x: x[0]
    )[1]

    q3_airq_en = st.radio(
        "3) Limited the activities you want to do every day?",
        options=[("No", 0), ("Yes", 1)], horizontal=True,
        format_func=lambda x: x[0]
    )[1]

    q4_airq_en = st.radio(
        "4) Caused you to use your rescue inhaler or nebulizer every day?",
        options=[("No", 0), ("Yes", 1)], horizontal=True,
        format_func=lambda x: x[0]
    )[1]

    st.markdown("#### In the past 2 weeks:")

    q5_airq_en = st.radio(
        "5) Did you have to limit your social activities (such as visiting with friends/relatives or playing with pets/children) because of your asthma?",
        options=[("No", 0), ("Yes", 1)], horizontal=True,
        format_func=lambda x: x[0]
    )[1]

    q6_airq_en = st.radio(
        "6) Did coughing, wheezing, shortness of breath, or chest tightness limit your ability to exercise?",
        options=[("No", 0), ("Yes", 1)], horizontal=True,
        format_func=lambda x: x[0]
    )[1]

    q7_airq_en = st.radio(
        "7) Did you feel that it was difficult to control your asthma?",
        options=[("No", 0), ("Yes", 1)], horizontal=True,
        format_func=lambda x: x[0]
    )[1]

    st.markdown("#### In the past 12 months, has coughing, wheezing, shortness of breath, or chest tightness:")

    q8_airq_en = st.radio(
        "8) Caused you to take steroid pills or shots, such as prednisone or methylprednisolone?",
        options=[("No", 0), ("Yes", 1)], horizontal=True,
        format_func=lambda x: x[0]
    )[1]

    q9_airq_en = st.radio(
        "9) Caused you to go to the emergency room or have unplanned visits to a health care provider?",
        options=[("No", 0), ("Yes", 1)], horizontal=True,
        format_func=lambda x: x[0]
    )[1]

    q10_airq_en = st.radio(
        "10) Caused you to stay in the hospital overnight?",
        options=[("No", 0), ("Yes", 1)], horizontal=True,
        format_func=lambda x: x[0]
    )[1]

    airq_en_score = (
        q1_airq_en + q2_airq_en + q3_airq_en + q4_airq_en +
        q5_airq_en + q6_airq_en + q7_airq_en +
        q8_airq_en + q9_airq_en + q10_airq_en
    )
    airq_en_cat = airq_level(airq_en_score)

    st.markdown(f"### AIRQ Score: **{airq_en_score}** — **{airq_en_cat}**")
    st.caption("Interpretation: 0–1 = Well controlled, 2–4 = Not well controlled, 5–10 = Very poorly controlled.")

    draw_airq_gauge(airq_en_score, arabic=False)

    st.markdown("---")
    st.markdown("### References (AIRQ)")
    st.markdown("""
1. **Murphy KR**, Chipps B, Beuther DA, et al.  
   *Development of the asthma impairment and risk questionnaire (AIRQ): a composite control measure.*  
   J Allergy Clin Immunol Pract. 2020;8(7):2263–2274.e5.

2. **Reibman J**, Chipps BE, Zeiger RS, et al.  
   *Relationship between asthma control as measured by the Asthma Impairment and Risk Questionnaire (AIRQ) and patient perception of disease status, health-related quality of life, and treatment adherence.*  
   J Asthma Allergy. 2023;16:59–72.
""")

# ===================== AIRQ – ARABIC =====================
with tab_airq_ar:
    st.header("استبيان اعتلال ومخاطر الربو (AIRQ) – العربية")

    st.markdown("""
للاستخدام من قبل مقدمي الرعاية الصحية لمرضاهم الذين تبلغ أعمارهم ١٢ عامًا فأكثر والذين شُخِّصوا بالربو.  
يُستخدم استبيان اعتلال ومخاطر الربو (AIRQ) كجزء من زيارة عيادة الربو.  
يُرجى الإجابة على كافة الأسئلة أدناه (نعم / لا).  
كل إجابة **نعم = 1 نقطة**، و **لا = 0**. المجموع من 0 إلى 10.
""")

    st.markdown("#### في خلال الأسبوعين الماضيين، هل كان السعال، أو صوت الصفير عند التنفس، أو ضيق التنفس، أو الضيق في الصدر:")

    q1_airq_ar = st.radio(
        "1) هل أزعجتك خلال اليوم لأكثر من 4 أيام؟",
        options=[("لا", 0), ("نعم", 1)], horizontal=True,
        format_func=lambda x: x[0]
    )[1]

    q2_airq_ar = st.radio(
        "2) هل أيقظك من النوم أكثر من مرة؟",
        options=[("لا", 0), ("نعم", 1)], horizontal=True,
        format_func=lambda x: x[0]
    )[1]

    q3_airq_ar = st.radio(
        "3) هل قلّصت الأنشطة التي تريد القيام بها كل يوم؟",
        options=[("لا", 0), ("نعم", 1)], horizontal=True,
        format_func=lambda x: x[0]
    )[1]

    q4_airq_ar = st.radio(
        "4) هل تسبّب في استخدامك لجهاز الاستنشاق أو البخاخة كل يوم؟",
        options=[("لا", 0), ("نعم", 1)], horizontal=True,
        format_func=lambda x: x[0]
    )[1]

    st.markdown("#### في آخر أسبوعين:")

    q5_airq_ar = st.radio(
        "5) هل اضطررت للحد من أنشطتك الاجتماعية (مثل زيارة الأصدقاء/الأقارب أو اللعب مع الحيوانات الأليفة/الأطفال) بسبب الربو؟",
        options=[("لا", 0), ("نعم", 1)], horizontal=True,
        format_func=lambda x: x[0]
    )[1]

    q6_airq_ar = st.radio(
        "6) هل حدّ السعال أو الأزيز أو ضيق التنفس أو ضيق الصدر من قدرتك على ممارسة الرياضة؟",
        options=[("لا", 0), ("نعم", 1)], horizontal=True,
        format_func=lambda x: x[0]
    )[1]

    q7_airq_ar = st.radio(
        "7) هل شعرتَ بصعوبة في السيطرة على الربو؟",
        options=[("لا", 0), ("نعم", 1)], horizontal=True,
        format_func=lambda x: x[0]
    )[1]

    st.markdown("#### في الأشهر الاثني عشر (12) الماضية، هل كان السعال أو الأزيز أو ضيق التنفس أو ضيق الصدر:")

    q8_airq_ar = st.radio(
        "8) هل تسبب في تناولك حبوبًا أو حقنًا كورتيزون؟",
        options=[("لا", 0), ("نعم", 1)], horizontal=True,
        format_func=lambda x: x[0]
    )[1]

    q9_airq_ar = st.radio(
        "9) هل تسبب في ذهابك إلى قسم الطوارئ أو زيارات غير مخطط لها لمقدم الرعاية الصحية؟",
        options=[("لا", 0), ("نعم", 1)], horizontal=True,
        format_func=lambda x: x[0]
    )[1]

    q10_airq_ar = st.radio(
        "10) هل تسبب في مكوثك في المستشفى طوال الليل؟",
        options=[("لا", 0), ("نعم", 1)], horizontal=True,
        format_func=lambda x: x[0]
    )[1]

    airq_ar_score = (
        q1_airq_ar + q2_airq_ar + q3_airq_ar + q4_airq_ar +
        q5_airq_ar + q6_airq_ar + q7_airq_ar +
        q8_airq_ar + q9_airq_ar + q10_airq_ar
    )
    airq_ar_cat = airq_level(airq_ar_score)

    st.markdown(f"### مجموع نقاط AIRQ: **{airq_ar_score}** — **{airq_ar_cat}**")
    st.caption("التفسير: 0–1 = سيطرة جيدة، 2–4 = سيطرة غير جيدة، 5–10 = سيطرة ضعيفة جدًا.")

    draw_airq_gauge(airq_ar_score, arabic=True)

    st.markdown("---")
    st.markdown("### المراجع (AIRQ)")
    st.markdown("""
1. **Murphy KR**، Chipps B، Beuther DA، وآخرون.  
   *Development of the asthma impairment and risk questionnaire (AIRQ): a composite control measure.*  
   J Allergy Clin Immunol Pract. 2020;8(7):2263–2274.e5.

2. **Reibman J**، Chipps BE، Zeiger RS، وآخرون.  
   *Relationship between asthma control as measured by the Asthma Impairment and Risk Questionnaire (AIRQ) and patient perception of disease status, health-related quality of life, and treatment adherence.*  
   J Asthma Allergy. 2023;16:59–72.
""")
