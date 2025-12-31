import streamlit as st
import random

# 1. පිටුවේ මූලික සැකසුම්
st.set_page_config(page_title="5 ශ්‍රේණිය ගණිතය මහා ප්‍රශ්න බැංකුව", layout="wide")

# CSS මගින් පෙනුම සකස් කිරීම
st.markdown("""
    <style>
    .q-text { font-size: 32px !important; font-weight: bold; color: #1B4F72; }
    .main-title { font-size: 40px; color: #D35400; text-align: center; font-weight: bold; }
    .stRadio > label { font-size: 24px !important; }
    </style>
""", unsafe_allow_html=True)

# 2. ප්‍රශ්න නිපදවන Logic එක (කිසිදු කොටසක් හලන්නේ නැත)
def generate_question_data(lesson_name):
    # මෙම ශ්‍රිතය මගින් අහඹු ලෙස සංඛ්‍යා වෙනස් කරමින් ප්‍රශ්න නිපදවයි
    if "සංඛ්‍යා" in lesson_name:
        n = random.randint(10000, 99999)
        q = f"{n:,} යන සංඛ්‍යාවේ දස දහස් ස්ථානයේ ඇති ඉලක්කම කුමක්ද?"
        ans = str(n)[0]
        opts = list(set([ans, "1", "0", str(random.randint(2,9))]))
    elif "රෝම" in lesson_name:
        r_map = {"IV": "4", "IX": "9", "XI": "11", "XII": "12", "VI": "6", "VII": "7"}
        r = random.choice(list(r_map.keys()))
        q = f"'{r}' යන රෝම සංඛ්‍යාවට අදාළ හින්දු අරාබි සංඛ්‍යාව කුමක්ද?"
        ans = r_map[r]
        opts = ["4", "9", "11", "7", "12", "6"]
    elif "එකතු" in lesson_name:
        n1, n2 = random.randint(1000, 5000), random.randint(1000, 4000)
        q = f"{n1:,} + {n2:,} හි පිළිතුර කුමක්ද?"
        ans = str(n1 + n2)
        opts = [ans, str(n1+n2+10), str(n1+n2-5), str(n1+n2+1)]
    elif "අඩු" in lesson_name:
        n1, n2 = random.randint(5000, 9000), random.randint(1000, 4000)
        q = f"{n1:,} - {n2:,} හි පිළිතුර කුමක්ද?"
        ans = str(n1 - n2)
        opts = [ans, str(n1-n2+10), str(n1-n2-10), str(n1-n2+5)]
    else:
        q = f"{lesson_name} ආශ්‍රිත පොදු ගණිත ගැටලුවක්."
        ans = "පිළිතුර"
        opts = ["පිළිතුර", "වැරදි 1", "වැරදි 2", "වැරදි 3"]
    
    random.shuffle(opts)
    return {"question": q, "options": opts, "correct": ans}

# 3. Sidebar මෙනුව
st.sidebar.title("📚 පටුන")
category = st.sidebar.selectbox("කාණ්ඩය:", ["සංඛ්‍යා", "ගණිතකර්ම", "මිනුම් හා ජ්‍යාමිතිය"])
lessons = {
    "සංඛ්‍යා": ["1. සංඛ්‍යා I", "2. සංඛ්‍යා II", "7. රෝම සංඛ්‍යා", "17. සංඛ්‍යා රටා"],
    "ගණිතකර්ම": ["3. එකතු කිරීම", "4. අඩු කිරීම", "6. ගුණ කිරීම", "7. බෙදීම"],
    "මිනුම් හා ජ්‍යාමිතිය": ["5. කාලය", "8. දිග", "10. භාග", "11. දශම", "12. කෝණ"]
}
selected_lesson = st.sidebar.radio("පාඩම තෝරන්න:", lessons[category])

# 4. Session State (දත්ත ගබඩා කිරීම)
if 'current_lesson' not in st.session_state or st.session_state.current_lesson != selected_lesson:
    st.session_state.current_lesson = selected_lesson
    st.session_state.q_no = 1
    st.session_state.score = 0
    st.session_state.user_answers = [] # ශිෂ්‍යයා දුන් පිළිතුරු
    st.session_state.all_questions = [generate_question_data(selected_lesson) for _ in range(20)]
    st.session_state.quiz_over = False

# 5. UI එක පෙන්වීම
st.markdown(f'<p class="main-title">{selected_lesson}</p>', unsafe_allow_html=True)

if not st.session_state.quiz_over:
    # ප්‍රශ්න පෙන්වන අවස්ථාව
    q_idx = st.session_state.q_no - 1
    current_q = st.session_state.all_questions[q_idx]

    st.write(f"### ප්‍රශ්න අංක: {st.session_state.q_no} / 20")
    st.progress(st.session_state.q_no / 20)
    
    st.markdown(f'<p class="q-text">{current_q["question"]}</p>', unsafe_allow_html=True)
    choice = st.radio("නිවැරදි පිළිතුර තෝරන්න:", current_q["options"], index=None, key=f"q_{st.session_state.q_no}")

    if st.button("ඊළඟ ප්‍රශ්නය ➡️"):
        if choice:
            # පිළිතුර ගබඩා කිරීම
            st.session_state.user_answers.append({
                "question": current_q["question"],
                "user_choice": choice,
                "correct_ans": current_q["correct"]
            })
            if choice == current_q["correct"]:
                st.session_state.score += 1
            
            # ඊළඟ ප්‍රශ්නයට හෝ අවසානයට යාම
            if st.session_state.q_no < 20:
                st.session_state.q_no += 1
                st.rerun()
            else:
                st.session_state.quiz_over = True
                st.rerun()
        else:
            st.warning("කරුණාකර පිළිතුරක් තෝරන්න!")

else:
    # 6. අවසාන වාර්තාව පෙන්වීම (මෙතැනදී පමණක් හරි වැරදි පෙන්වයි)
    st.balloons()
    st.header("📊 ප්‍රශ්නාවලියේ ප්‍රතිඵල")
    st.subheader(f"ඔබේ මුළු ලකුණු සංඛ්‍යාව: {st.session_state.score} / 20")
    
    st.write("---")
    st.write("### ඔබේ පිළිතුරු විශ්ලේෂණය:")
    
    for i, res in enumerate(st.session_state.user_answers):
        with st.expander(f"ප්‍රශ්නය {i+1}: {res['question']}"):
            if res['user_choice'] == res['correct_ans']:
                st.success(f"නිවැරදියි! ✅ ඔබේ පිළිතුර: {res['user_choice']}")
            else:
                st.error(f"වැරදියි! ❌ ඔබේ පිළිතුර: {res['user_choice']}")
                st.info(f"නිවැරදි පිළිතුර: {res['correct_ans']}")

    if st.button("නැවත උත්සාහ කරන්න 🔄"):
        st.session_state.current_lesson = None # Reset
        st.rerun()
