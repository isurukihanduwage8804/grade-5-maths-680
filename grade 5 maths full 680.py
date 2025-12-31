import streamlit as st
import random
import streamlit.components.v1 as components

# 1. පිටුවේ මූලික සැකසුම් (Page Config)
st.set_page_config(page_title="5 ශ්‍රේණිය ගණිතය මහා ප්‍රශ්න බැංකුව", layout="wide")

# CSS මගින් අකුරු ලොකු කිරීම සහ පෙනුම සැකසීම
st.markdown("""
    <style>
    .main-title { font-size: 45px; color: #D35400; text-align: center; font-weight: bold; }
    .q-text { font-size: 32px !important; font-weight: bold; color: #1B4F72; line-height: 1.5; }
    .stRadio > label { font-size: 24px !important; color: #2C3E50; }
    div.stButton > button { width: 100%; height: 60px; font-size: 22px; background-color: #28B463; color: white; }
    .result-box { padding: 20px; border-radius: 10px; font-size: 24px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 2. ප්‍රශ්න නිපදවන මහා තර්කනය (Question Generator Logic)
def get_math_data(lesson_name):
    options = []
    correct = ""
    question = ""

    # පාඩම: සංඛ්‍යා I, II, III (ස්ථානීය අගය, විශාලම/කුඩාම සංඛ්‍යා)
    if "සංඛ්‍යා" in lesson_name:
        case = random.randint(1, 3)
        if case == 1:
            digits = random.sample(range(1, 9), 4)
            correct = "".join(map(str, sorted(digits, reverse=True)))
            question = f"{digits[0]}, {digits[1]}, {digits[2]}, {digits[3]} යන ඉලක්කම් හතරම භාවිතා කර ලිවිය හැකි විශාලම සංඛ්‍යාව කුමක්ද?"
            options = [correct, str(int(correct)-100), str(int(correct)-10), str(int(correct)+9)]
        elif case == 2:
            n = random.randint(10000, 99999)
            question = f"{n:,} යන සංඛ්‍යාවේ දස දහස් ස්ථානයේ ඇති ඉලක්කම කුමක්ද?"
            correct = str(n)[0]
            options = ["1", "0", "5", correct]
        else:
            n = random.randint(50000, 99998)
            question = f"{n:,} ට වඩා 1ක් වැඩි වූ විට ලැබෙන සංඛ්‍යාව කුමක්ද?"
            correct = str(n + 1)
            options = [correct, str(n), str(n+2), str(n+10)]

    # පාඩම: රෝම සංඛ්‍යා
    elif "රෝම" in lesson_name:
        r_map = {"IV": "4", "IX": "9", "XI": "11", "VII": "7", "XII": "12", "VI": "6"}
        r = random.choice(list(r_map.keys()))
        question = f"'{r}' යන රෝම සංඛ්‍යාවට අදාළ හින්දු අරාබි සංඛ්‍යාව (සාමාන්‍ය අංකය) කුමක්ද?"
        correct = r_map[r]
        options = ["4", "9", "11", "7", "12", "6"]

    # පාඩම: ගණිතකර්ම (එකතු, අඩු, ගුණ, බෙදීම)
    elif any(x in lesson_name for x in ["එකතු", "අඩු", "ගුණ", "බෙදීම"]):
        n1 = random.randint(100, 1000)
        n2 = random.randint(10, 100)
        if "එකතු" in lesson_name:
            question = f"{n1} + {n2} හි පිළිතුර කුමක්ද?"
            correct = str(n1 + n2)
        elif "අඩු" in lesson_name:
            question = f"{n1} - {n2} හි පිළිතුර කුමක්ද?"
            correct = str(n1 - n2)
        elif "ගුණ" in lesson_name:
            n2 = random.randint(2, 9)
            question = f"{n1} x {n2} හි පිළිතුර කුමක්ද?"
            correct = str(n1 * n2)
        else: # බෙදීම
            n1 = random.randint(20, 100)
            n2 = random.randint(2, 5)
            question = f"{n1 * n2} බෙදීම {n2} හි පිළිතුර කුමක්ද?"
            correct = str(n1)
        options = [correct, str(int(correct)+random.randint(1,5)), str(int(correct)-random.randint(1,5)), str(int(correct)+10)]

    # වෙනත් පාඩම් සඳහා (Default)
    else:
        question = f"{lesson_name} පාඩමට අදාළ මූලධර්මයක් තෝරන්න."
        correct = "නිවැරදි පිළිතුර"
        options = ["නිවැරදි පිළිතුර", "වැරදි පිළිතුර 1", "වැරදි පිළිතුර 2", "වැරදි පිළිතුර 3"]

    random.shuffle(options)
    return question, options, correct

# 3. Sidebar - පටුන (පාඩම් 34 ම මෙහි ලැයිස්තුගත කළ හැක)
st.sidebar.title("📚 ගණිතය මෙනුව")
category = st.sidebar.selectbox("කාණ්ඩය:", ["සංඛ්‍යා හා රටා", "ගණිතකර්ම", "මිනුම් හා ජ්‍යාමිතිය"])

lesson_list = {
    "සංඛ්‍යා හා රටා": ["1. සංඛ්‍යා I", "2. සංඛ්‍යා II", "7. රෝම සංඛ්‍යා", "17. සංඛ්‍යා රටා", "20. සංඛ්‍යා III"],
    "ගණිතකර්ම": ["3. එකතු කිරීම", "4. අඩු කිරීම", "6. ගුණ කිරීම", "7. බෙදීම"],
    "මිනුම් හා ජ්‍යාමිතිය": ["5. කාලය", "8. දිග", "10. භාග", "11. දශම", "12. කෝණ", "13. පරිමිතිය"]
}

selected_lesson = st.sidebar.radio("පාඩම තෝරන්න:", lesson_list[category])

# 4. Session State පාලනය
if 'q_idx' not in st.session_state or st.session_state.current_lesson != selected_lesson:
    st.session_state.current_lesson = selected_lesson
    st.session_state.q_idx = 1
    st.session_state.score = 0
    st.session_state.ans_status = None
    st.session_state.q_data = get_math_data(selected_lesson)

# 5. UI සහ ප්‍රශ්න පෙන්වීම
st.markdown(f'<p class="main-title">{selected_lesson}</p>', unsafe_allow_html=True)
st.write(f"### ප්‍රශ්නය: {st.session_state.q_idx} / 20 | ලකුණු: {st.session_state.score}")
st.progress(st.session_state.q_idx / 20)

q_txt, opts, correct_ans = st.session_state.q_data

st.markdown(f'<div style="background:#f9f9f9; padding:25px; border-left:10px solid #D35400;"><p class="q-text">{q_txt}</p></div>', unsafe_allow_html=True)

choice = st.radio("නිවැරදි පිළිතුර තෝරන්න:", opts, index=None, key=f"radio_{st.session_state.q_idx}")

# හරි වැරදි පෙන්වන Logic එක
if st.button("ඊළඟ ප්‍රශ්නය ➡️"):
    if choice:
        if choice == correct_ans:
            st.session_state.score += 1
            st.success("නිවැරදියි! 🎉")
        else:
            st.error(f"වැරදියි! නිවැරදි පිළිතුර: {correct_ans}")
        
        # ප්‍රශ්න 20ක් දක්වා ඉදිරියට යාම
        if st.session_state.q_idx < 20:
            st.session_state.q_idx += 1
            st.session_state.q_data = get_math_data(selected_lesson)
            st.rerun()
        else:
            st.balloons()
            st.markdown(f'<div class="result-box" style="background:#D4EFDF;">සියලු ප්‍රශ්න අවසන්! ඔබේ මුළු ලකුණු: {st.session_state.score} / 20</div>', unsafe_allow_html=True)
    else:
        st.warning("කරුණාකර පිළිතුරක් තෝරන්න!")
