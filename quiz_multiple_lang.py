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
#from langchain.pydantic_v1 import BaseModel, Field

from pydantic import BaseModel, Field

# --------------------------------------------
# 1) IMPORT TRANSLATED TEMPLATES
# --------------------------------------------
from quiz_templates_miltiple_lang import *

# Helper function to detect language
def detect_language(text: str) -> str:
    """
    Uses langdetect to detect the language from the provided text.
    Returns a language code (e.g. 'en', 'fr', 'ar', etc.).
    """
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
    alternatives: List[List[str]] = Field(
        description="The quiz alternatives for each question as a list of lists"
    )
    answers: List[str] = Field(description="The quiz answers")


class QuizOpenEnded(BaseModel):
    questions: List[str] = Field(description="The quiz questions")
    answers: List[str] = Field(description="The quiz answers")


############################################
# HELPER FUNCTIONS
############################################

def extract_text_from_pdf(pdf_file) -> str:
    """Extracts text from an uploaded PDF file."""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "".join(page.get_text("text") for page in doc)
    return text


def create_quiz_chain(prompt_template, llm, pydantic_object_schema):
    """Creates the chain for the quiz app using the prompt template and the LLM."""
    return prompt_template | llm.with_structured_output(pydantic_object_schema)


def display_questions(quiz_type):
    """Display questions and store user answers in session state."""
    if quiz_type == "multiple-choice":
        for i, question in enumerate(st.session_state.questions):
            st.markdown(f"**Question {i + 1}:** {question}")
            options = st.session_state.alternatives[i]
            selected_option = st.radio(
                f"Select your answer for Q{i + 1}",
                options,
                key=f"question_{i}"
            )
            option_index = options.index(selected_option)
            option_identifier = chr(97 + option_index)  # 'a' for 0, 'b' for 1, etc.
            st.session_state.user_answers[i] = option_identifier

    elif quiz_type == "true-false":
        for i, question in enumerate(st.session_state.questions):
            st.markdown(f"**Question {i + 1}:** {question}")
            selected_option = st.radio(
                f"Select your answer for Q{i + 1}",
                ["True", "False"],
                key=f"question_{i}"
            )
            st.session_state.user_answers[i] = selected_option

    elif quiz_type == "open-ended":
        for i, question in enumerate(st.session_state.questions):
            st.markdown(f"**Question {i + 1}:** {question}")
            user_response = st.text_input(
                f"Your answer for Q{i + 1}",
                key=f"question_{i}"
            )
            st.session_state.user_answers[i] = user_response


def process_submission(quiz_type):
    """Process the user's submission and display score if applicable."""
    if 'user_answers' in st.session_state:
        # Check if any question is unanswered
        if any(ans is None or ans.strip() == "" for ans in st.session_state.user_answers):
            st.warning("Please answer all the questions before submitting.")
            return

        if quiz_type in ["multiple-choice", "true-false"]:
            # Transform user answers to match the format of the correct answers
            user_answers = [
                st.session_state.get(f"question_{i}") for i in range(len(st.session_state.questions))
            ]
            st.session_state.user_answers_news = user_answers
            # Calculate score
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
    """
    Detects the language from the given text_context and
    returns the appropriate ChatPromptTemplate function.
    """
    lang = detect_language(text_context)

    # For multiple-choice
    if quiz_type == "multiple-choice":
        if lang == "fr":
            return create_multiple_choice_template_fr()
        elif lang == "ar":
            return create_multiple_choice_template_ar()
        else:
            return create_multiple_choice_template_en()

    # For true-false
    elif quiz_type == "true-false":
        if lang == "fr":
            return create_true_false_template_fr()
        elif lang == "ar":
            return create_true_false_template_ar()
        else:
            return create_true_false_template_en()

    # For open-ended
    else:  # open-ended
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

    # Initialize session state
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    if 'alternatives' not in st.session_state:
        st.session_state.alternatives = []

    # Ask for OpenAI API key
    openai_api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key
    else:
        st.warning("Please enter your OpenAI API key to continue.")

    # PDF upload
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    pdf_text = ""
    if uploaded_file is not None:
        pdf_text = extract_text_from_pdf(uploaded_file)
        st.success("PDF text extracted! You can view/edit it below:")
    else:
        st.info("Please upload a PDF file.")

    # Display the extracted text in a text area for optional editing
    context = st.text_area("Context (extracted from PDF)", pdf_text, height=200)

    # Quiz controls
    num_questions = st.number_input(
        "Number of questions",
        min_value=1,
        max_value=10,
        value=3
    )
    quiz_type = st.selectbox(
        "Select quiz type",
        ["multiple-choice", "true-false", "open-ended"]
    )

    # Generate Quiz button
    if st.button("Generate Quiz"):
        if not openai_api_key:
            st.error("Please provide a valid OpenAI API key.")
            return
        if not context.strip():
            st.error("Please provide a non-empty context (or upload a valid PDF).")
            return

        # 1) Choose the right prompt template based on detected language
        prompt_template = choose_prompt_template(quiz_type, context)

        # 2) Initialize the LLM
        llm = ChatOpenAI(model="gpt-4o", temperature=0.0)

        # 3) Create the quiz chain
        chain = create_quiz_chain(prompt_template, llm,
                                  QuizMultipleChoice if quiz_type == "multiple-choice" else
                                  QuizTrueFalse if quiz_type == "true-false" else
                                  QuizOpenEnded
                                  )

        # 4) Invoke the chain
        quiz_response = chain.invoke({
            "num_questions": num_questions,
            "quiz_context": context
        })

        # Store quiz data in session state
        st.session_state.questions = quiz_response.questions
        st.session_state.answers = quiz_response.answers

        if quiz_type == "multiple-choice":
            st.session_state.alternatives = quiz_response.alternatives
        else:
            st.session_state.alternatives = []  # Clear alternatives if not multiple-choice

        # Initialize user answers
        st.session_state.user_answers = [None] * len(st.session_state.questions)

        st.success("Quiz generated below! Scroll down to answer.")

    # If we have questions, display them in a form
    if st.session_state.questions:
        with st.form("quiz_form"):
            display_questions(quiz_type)
            submitted = st.form_submit_button("Submit Answers")
            if submitted:
                process_submission(quiz_type)





if __name__ == "__main__":
    main()


