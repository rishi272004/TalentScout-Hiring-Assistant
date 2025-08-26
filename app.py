# app.py
import streamlit as st
from core.chatbot import HiringChatbot
from core.utils import ensure_key, save_candidate_record
from core.i18n import supported_langs, translate_text
from core.sentiment import analyze_sentiment
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="TalentScout — Universal Hiring Assistant",
    page_icon="🧭",
    layout="wide"
)

KEY = ensure_key()

with st.sidebar:
    st.image("logo.png", use_container_width=True)
    st.title("TalentScout")
    st.write("Universal Hiring Assistant — works for ALL job roles.")

    lang = st.selectbox(
        "Language / भाषा / Idioma:",
        options=list(supported_langs.keys()),
        index=0,
        format_func=lambda k: f"{supported_langs[k]} ({k})"
    )

_ = lambda s: translate_text(s, target_lang=lang)

st.title(_("Welcome to TalentScout — Universal Hiring Assistant"))
st.write(_("This assistant works for ALL roles, collects candidate details, and generates customized interview questions."))

with st.expander(_("Candidate Information Form"), expanded=True):
    with st.form(key="candidate_form"):
        full_name = st.text_input(_("Full Name"))
        email = st.text_input(_("Email Address"))
        phone = st.text_input(_("Phone Number"))
        years_exp = st.number_input(_("Years of Experience"), min_value=0, max_value=50, value=1)
        role = st.text_input(_("Job Role (e.g., Marketing Manager, HR, Data Scientist)"))
        skills = st.text_area(_("Key Skills (comma-separated, e.g., SEO, Leadership, Python, Negotiation)"))
        location = st.text_input(_("Current Location"))

        personalize = st.checkbox(_("Personalize based on prior records (if any)"), value=True)
        do_sentiment = st.checkbox(_("Run sentiment analysis on responses (bonus)"), value=True)

        submit = st.form_submit_button(_("Start Screening"))

    if submit:
        if not full_name or not email or not role:
            st.error(_("Please provide at least Full Name, Email, and Job Role to proceed."))
        else:
            candidate = {
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "years_exp": years_exp,
                "role": role,
                "skills": [s.strip() for s in skills.split(",") if s.strip()],
                "location": location,
            }
            saved_id = save_candidate_record(candidate)
            st.success(_("Candidate saved (anonymized) with id") + f": {saved_id}")

            # Use Ollama local model (Mistral)
            chatbot = HiringChatbot(model="mistral:latest", language=lang)

            if personalize:
                st.info(_("Searching for prior interactions..."))
                prior = chatbot.match_prior(candidate["email"])
                if prior:
                    st.success(_("Found prior interactions for this candidate — responses will be personalized."))
                    st.json(prior)

            st.header(_("Generated Interview Questions"))
            with st.spinner(_("Generating role-specific questions...")):
                questions = chatbot.generate_questions(candidate)

            for i, q in enumerate(questions, 1):
                st.markdown(f"**Q{i}.** {q}")

            st.markdown("---")
            st.header(_("Interactive Screening Chat"))

            if "conversation" not in st.session_state:
                st.session_state["conversation"] = []

            user_input = st.text_input(_("Ask a follow-up question (or type 'exit' to finish)"))
            if st.button(_("Send")) or user_input:
                if user_input.strip().lower() in ["exit", "quit", "bye", "end"]:
                    st.balloons()
                    st.success(_("Conversation ended. Thank you — the recruiter will reach out shortly."))
                    st.session_state.pop("conversation", None)
                else:
                    st.session_state["conversation"].append({"role": "user", "content": user_input})
                    reply = chatbot.chat_reply(st.session_state["conversation"])
                    st.session_state["conversation"].append({"role": "assistant", "content": reply})

                    if do_sentiment:
                        sentiment = analyze_sentiment(user_input)
                        st.write(_("Sentiment analysis"), sentiment)

                    st.info(reply)
