#llx-bYcdRMr0i9Wca2MfWFigTh952x9EfgrkQcKOh9fMpeO0s9CW
import streamlit as st
import os
from typing import List

# For PDF extraction
import pymupdf as fitz

# For language detection
from langdetect import detect

# LLM
from langchain_openai import ChatOpenAI

# Pydantic models for structured output
from pydantic import BaseModel, Field

# Parsing
from llama_parse import LlamaParse

# --------------------------------------------
# 1) IMPORT TRANSLATED TEMPLATES
# --------------------------------------------
from quiz_templates_miltiple_lang import *

# Helper function to detect language
def detect_language(text: str) -> str:
    return detect(text)


############################################
# QUIZ SCHEMA CLASSES
############################################

class QuizTrueFalse(BaseModel):
    quiz_text: str = Field(description="The quiz text")
    questions: List[str] = Field(description="The quiz questions")
    answers: List[str] = Field(description="The quiz answers for each question as True or False only.")


class QuizMultipleChoice(BaseModel):
    quiz_text: str = Field(description="The quiz text")
    questions: List[str] = Field(description="The quiz questions")
    alternatives: List[List[str]] = Field(description="The quiz alternatives for each question as a list of lists")
    answers: List[str] = Field(description="The quiz answers")


class QuizOpenEnded(BaseModel):
    questions: List[str] = Field(description="The quiz questions")
    answers: List[str] = Field(description="The quiz answers")


############################################
# HELPER FUNCTIONS
############################################

def extract_text_from_pdf(pdf_file) -> str:
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "".join(page.get_text("text") for page in doc)
    return text


def extract_text_llamaparse(pdf_file, api_key) -> str:
    with open("temp_uploaded.pdf", "wb") as f:
        f.write(pdf_file.read())

    parser = LlamaParse(api_key=api_key, result_type="text", verbose=True)
    docs = parser.load_data("temp_uploaded.pdf")
    
    if not docs:
        return "Aucun contenu extrait du PDF."
    
    return "\n".join([doc.text for doc in docs])


def create_quiz_chain(prompt_template, llm, pydantic_object_schema):
    return prompt_template | llm.with_structured_output(pydantic_object_schema)


def display_questions(quiz_type):
    if quiz_type == "multiple-choice":
        for i, question in enumerate(st.session_state.questions):
            st.markdown(f"**Question {i + 1}:** {question}")
            options = st.session_state.alternatives[i]
            selected_option = st.radio(
                f"Select your answer for Q{i + 1}",
                options,
                key=f"question_{i}"
            )
            st.session_state.user_answers[i] = selected_option

            # ✅ Affiche la bonne réponse
            answer = st.session_state.answers[i]
            if answer in options:
                st.markdown(f"<span style='color: green'>Bonne réponse : **{answer}**</span>", unsafe_allow_html=True)
            else:
                try:
                    correct_index = ord(answer.strip().lower()) - 97
                    if 0 <= correct_index < len(options):
                        st.markdown(f"<span style='color: green'>Bonne réponse : **{options[correct_index]}**</span>", unsafe_allow_html=True)
                except:
                    st.warning(f"Impossible d'afficher la bonne réponse pour la question {i+1}.")

    elif quiz_type == "true-false":
        for i, question in enumerate(st.session_state.questions):
            st.markdown(f"**Question {i + 1}:** {question}")
            selected_option = st.radio(
                f"Select your answer for Q{i + 1}",
                ["True", "False"],
                key=f"question_{i}"
            )
            st.session_state.user_answers[i] = selected_option

            st.markdown(f"<span style='color: green'>Bonne réponse : **{st.session_state.answers[i]}**</span>", unsafe_allow_html=True)

    elif quiz_type == "open-ended":
        for i, question in enumerate(st.session_state.questions):
            st.markdown(f"**Question {i + 1}:** {question}")
            user_response = st.text_input(
                f"Your answer for Q{i + 1}",
                key=f"question_{i}"
            )
            st.session_state.user_answers[i] = user_response

            st.markdown(f"<span style='color: green'>Réponse attendue : **{st.session_state.answers[i]}**</span>", unsafe_allow_html=True)


def process_submission(quiz_type):
    if 'user_answers' in st.session_state:
        if any(ans is None or ans.strip() == "" for ans in st.session_state.user_answers):
            st.warning("Please answer all the questions before submitting.")
            return

        if quiz_type in ["multiple-choice", "true-false"]:
            user_answers = [
                st.session_state.get(f"question_{i}") for i in range(len(st.session_state.questions))
            ]
            st.session_state.user_answers_news = user_answers
            score = sum(
                user_answer == correct_answer
                for user_answer, correct_answer
                in zip(st.session_state.user_answers_news, st.session_state.answers)
            )
            st.write(f"Your score is **{score}/{len(st.session_state.questions)}**")
        else:
            st.write("Open-ended questions have been submitted.")
            st.write("Answers:", st.session_state.answers)


############################################
# PROMPT-SELECTION LOGIC
############################################

def choose_prompt_template(quiz_type: str, text_context: str):
    lang = detect_language(text_context)

    if quiz_type == "multiple-choice":
        if lang == "fr":
            return create_multiple_choice_template_fr()
        elif lang == "ar":
            return create_multiple_choice_template_ar()
        else:
            return create_multiple_choice_template_en()

    elif quiz_type == "true-false":
        if lang == "fr":
            return create_true_false_template_fr()
        elif lang == "ar":
            return create_true_false_template_ar()
        else:
            return create_true_false_template_en()

    else:
        if lang == "fr":
            return create_open_ended_template_fr()
        elif lang == "ar":
            return create_open_ended_template_ar()
        else:
            return create_open_ended_template_en()


############################################
# MAIN STREAMLIT APP
############################################

def main():
    st.title("MindBridge Quiz Generator")
    st.write("Upload a PDF, extract its text, then generate a quiz based on that text!")

    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    if 'alternatives' not in st.session_state:
        st.session_state.alternatives = []

    openai_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    llamaparse_api_key = st.sidebar.text_input("Enter your LlamaParse API key", type="password")

    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key
    else:
        st.warning("Please enter your OpenAI API key to continue.")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    parse_method = st.radio("Méthode d'extraction du texte PDF", ["Standard (PyMuPDF)", "LlamaParse (qualité supérieure)"])

    pdf_text = ""
    if uploaded_file is not None:
        if parse_method == "LlamaParse (qualité supérieure)":
            if not llamaparse_api_key:
                st.error("Veuillez saisir votre clé API LlamaParse.")
                return
            pdf_text = extract_text_llamaparse(uploaded_file, llamaparse_api_key)
        else:
            pdf_text = extract_text_from_pdf(uploaded_file)

        st.success("Texte extrait du PDF ! Vous pouvez le voir ou le modifier ci-dessous :")
    else:
        st.info("Please upload a PDF file.")

    context = st.text_area("Context (extracted from PDF)", pdf_text, height=200)

    num_questions = st.number_input("Number of questions", min_value=1, max_value=10, value=3)
    quiz_type = st.selectbox("Select quiz type", ["multiple-choice", "true-false", "open-ended"])
    temperature = st.slider("Créativité du quiz (température)", min_value=0.0, max_value=4.0, value=0.0, step=0.2)

    if st.button("Generate Quiz"):
        if not openai_api_key:
            st.error("Please provide a valid OpenAI API key.")
            return
        if not context.strip():
            st.error("Please provide a non-empty context (or upload a valid PDF).")
            return

        prompt_template = choose_prompt_template(quiz_type, context)
        llm = ChatOpenAI(model="gpt-4o", temperature=temperature)

        chain = create_quiz_chain(prompt_template, llm,
                                  QuizMultipleChoice if quiz_type == "multiple-choice" else
                                  QuizTrueFalse if quiz_type == "true-false" else
                                  QuizOpenEnded)

        quiz_response = chain.invoke({
            "num_questions": num_questions,
            "quiz_context": context
        })

        st.session_state.questions = quiz_response.questions
        st.session_state.answers = quiz_response.answers
        st.session_state.alternatives = quiz_response.alternatives if quiz_type == "multiple-choice" else []
        st.session_state.user_answers = [None] * len(st.session_state.questions)

        st.success("Quiz generated below! Scroll down to answer.")

    if st.session_state.questions:
        with st.form("quiz_form"):
            display_questions(quiz_type)
            submitted = st.form_submit_button("Submit Answers")
            if submitted:
                process_submission(quiz_type)


    if st.session_state.questions:
        with st.form("quiz_form"):
            display_questions(quiz_type)
            submitted = st.form_submit_button("Submit Answers")
            if submitted:
                process_submission(quiz_type)

if __name__ == "__main__":
    main()
