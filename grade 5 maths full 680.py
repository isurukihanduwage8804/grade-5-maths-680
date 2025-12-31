import streamlit as st
import random

st.set_page_config(page_title="ගණිතය මහා ප්‍රශ්න බැංකුව", layout="wide")

# CSS මගින් පෙනුම ලස්සන කිරීම
st.markdown("""
    <style>
    .q-text { font-size: 30px !important; font-weight: bold; color: #1E3A5F; }
    .stRadio > label { font-size: 22px !important; }
    .main-header { font-size: 45px; text-align: center; color: #D35400; }
    </style>
""", unsafe_allow_html=True)

# 1. සියලුම පාඩම් ලැයිස්තුව
lesson_map = {
    "සංඛ්‍යා": ["1. සංඛ්‍යා I", "2. සංඛ්‍යා II", "7. රෝම සංඛ්‍යා", "17. සංඛ්‍යා රටා", "20. සංඛ්‍යා III"],
    "ගණිතකර්ම": ["3. එකතු කිරීම", "4. අඩු කිරීම", "6. ගුණ කිරීම", "7. බෙදීම"],
    "මිනුම්": ["5. කාලය", "8. දිග", "9. බර", "15. ධාරිතාව", "21. මුදල්"],
    "ජ්‍යාමිතිය": ["10. භාග", "11. දශම", "12. කෝණ", "13. පරිමිතිය", "18. වෘත්තය"]
}

# 2. Sidebar මෙනුව
st.sidebar.title("📚 පටුන")
category = st.sidebar.selectbox("කාණ්ඩය:", list(lesson_map.keys()))
selected_lesson = st.sidebar.radio("පාඩම තෝරන්න:", lesson_map[category])

# 3. ප්‍රශ්න නිපදවන 'Smart' Function එක
def generate_dynamic_question(lesson):
    if "සංඛ්‍යා" in lesson:
        n = random.randint(10000, 99999)
        q = f"{n:,} හි දස දහස් ස්ථානයේ ඇති ඉලක්කම කුමක්ද?"
        ans = str(n)[0]
        opts = list(set([ans, str(random.randint(0,9)), str(random.randint(0,9)), str(random.randint(0,9))]))
    elif "එකතු කිරීම" in lesson:
        n1, n2 = random.randint(1000, 5000), random.randint(1000, 5000)
        q = f"{n1:,} + {n2:,} හි පිළිතුර කුමක්ද?"
        ans = str(n1 + n2)
        opts = [ans, str(n1+n2+10), str(n1+n2-10), str(n1+n2+1)]
    elif "රෝම සංඛ්‍යා" in lesson:
        r_map = {"IV": "4", "IX": "9", "XI": "11", "VII": "7", "XII": "12"}
        r = random.choice(list(r_map.keys()))
        q = f"'{r}' රෝම සංඛ්‍යාවට අදාළ සාමාන්‍ය අංකය කුමක්ද?"
        ans = r_map[r]
        opts = ["4", "9", "11", "7", "12"]
    elif "ගුණ කිරීම" in lesson:
        n1, n2 = random.randint(10, 99), random.randint(2, 9)
        q = f"{n1} x {n2} හි අගය කීයද?"
        ans = str(n1 * n2)
        opts = [ans, str(n1*n2+2), str(n1*n2-2), str(n1*n2+10)]
    else:
        q, opts, ans = "මෙම පාඩම සඳහා ප්‍රශ්න සැකසෙමින් පවතී...", ["A", "B", "C", "D"], "A"
    
    random.shuffle(opts)
    return q, opts, ans

# 4. Session State පාලනය (ප්‍රශ්න 20ක් පවත්වා ගැනීම)
if 'active_lesson' not in st.session_state or st.session_state.active_lesson != selected_lesson:
    st.session_state.active_lesson = selected_lesson
    st.session_state.q_no = 1
    st.session_state.score = 0
    st.session_state.current_q_data = generate_dynamic_question(selected_lesson)

# 5. UI එක පෙන්වීම
st.markdown(f'<p class="main-header">{selected_lesson}</p>', unsafe_allow_html=True)
st.write(f"### ප්‍රශ්න අංක: {st.session_state.q_no} / 20  |  ලකුණු: {st.session_state.score}")
st.progress(st.session_state.q_no / 20)

q_text, options, correct_ans = st.session_state.current_q_data

st.markdown(f'<div style="background:#f0f2f6;padding:20px;border-radius:10px;"><p class="q-text">{q_text}</p></div>', unsafe_allow_html=True)
choice = st.radio("පිළිතුර තෝරන්න:", options, index=None, key=f"q_{st.session_state.q_no}")

if st.button("ඊළඟ ප්‍රශ්නය ➡️"):
    if choice:
        if choice == correct_ans:
            st.session_state.score += 1
        
        if st.session_state.q_no < 20:
            st.session_state.q_no += 1
            st.session_state.current_q_data = generate_dynamic_question(selected_lesson)
            st.rerun()
        else:
            st.balloons()
            st.success(f"නිමයි! ඔබේ මුළු ලකුණු: {st.session_state.score} / 20")
    else:
        st.warning("කරුණාකර පිළිතුරක් තෝරන්න!")
