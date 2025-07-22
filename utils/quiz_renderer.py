import streamlit as st

def render_dynamic_quiz(quiz_data):
    st.subheader("🧪 Quiz Based on Chapter")

    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = [None] * len(quiz_data)

    if "submitted" not in st.session_state:
        st.session_state.submitted = False

    for idx, q in enumerate(quiz_data):
        st.markdown(f"**Q{idx+1}: {q['question']}**")

        if q["type"] == "mcq":
            selected = st.radio(
                f"Select your answer for Q{idx+1}",
                q["options"],
                key=f"q{idx}_option",
                index=(q["options"].index(st.session_state.quiz_answers[idx])
                       if st.session_state.quiz_answers[idx] else 0)
            )
            st.session_state.quiz_answers[idx] = selected

        elif q["type"] == "true_false":
            selected = st.radio(
                f"Select your answer for Q{idx+1}",
                ["True", "False"],
                key=f"q{idx}_tf",
                index=(["True", "False"].index(st.session_state.quiz_answers[idx])
                       if st.session_state.quiz_answers[idx] else 0)
            )
            st.session_state.quiz_answers[idx] = selected

        elif q["type"] == "fill_blank":
            answer = st.text_input(
                f"Your answer for Q{idx+1}",
                value=st.session_state.quiz_answers[idx] or "",
                key=f"q{idx}_text"
            )
            st.session_state.quiz_answers[idx] = answer

        # ✅ After submission, show correct answer
        if st.session_state.submitted:
            st.markdown(f"✅ **Correct Answer:** `{q['answer']}`")

        st.markdown("---")

    if st.button("Submit Quiz"):
        st.session_state.submitted = True
