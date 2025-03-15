import streamlit as st
import pymupdf as fitz
import os
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from quiz_templates import create_multiple_choice_template, create_true_false_template, create_open_ended_template
from typing import List


# Define Quiz Models
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


# Function to Extract Text from PDF
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "".join(page.get_text("text") for page in doc)
    return text


# Function to Create Quiz Chain
def create_quiz_chain(prompt_template, llm, pydantic_object_schema):
    return prompt_template | llm.with_structured_output(pydantic_object_schema)


def main():
    st.title("📄 AI Quiz Generator from PDFs")
    st.write("Upload a PDF, and AI will generate quizzes based on the extracted content.")

    openai_api_key = st.sidebar.text_input("🔑 Enter your OpenAI API key", type="password")
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key
    else:
        st.error("Please enter your OpenAI API key")
        return

    # File uploader
    uploaded_file = st.file_uploader("📤 Upload a PDF document", type=["pdf"])
    if uploaded_file:
        pdf_text = extract_text_from_pdf(uploaded_file)
        st.session_state["pdf_text"] = pdf_text
        st.success("✅ PDF uploaded and text extracted!")
    else:
        return

    llm = ChatOpenAI(model="gpt-4o", temperature=0.0)

    quiz_type = st.selectbox("🎯 Select Quiz Type", ["Multiple Choice", "True/False", "Open-Ended"])
    num_questions = st.number_input("🔢 Number of Questions", min_value=1, max_value=10, value=5)

    if quiz_type == "Multiple Choice":
        prompt_template = create_multiple_choice_template()
        pydantic_object_schema = QuizMultipleChoice
    elif quiz_type == "True/False":
        prompt_template = create_true_false_template()
        pydantic_object_schema = QuizTrueFalse
    else:
        prompt_template = create_open_ended_template()
        pydantic_object_schema = QuizOpenEnded

    if st.button("🚀 Generate Quiz"):
        st.write("⏳ Generating quiz... please wait!")
        chain = create_quiz_chain(prompt_template, llm, pydantic_object_schema)
        quiz_response = chain.invoke({"num_questions": num_questions, "quiz_context": st.session_state["pdf_text"]})

        st.session_state.questions = quiz_response.questions
        st.session_state.answers = quiz_response.answers
        if quiz_type == "Multiple Choice":
            st.session_state.alternatives = quiz_response.alternatives
        st.session_state.user_answers = [None] * len(quiz_response.questions)
        st.success("✅ Quiz Generated Successfully!")

    if "questions" in st.session_state:
        display_questions(quiz_type)
        if st.button("✅ Submit Answers"):
            process_submission(quiz_type)


# Function to Display Questions
def display_questions(quiz_type):
    for i, question in enumerate(st.session_state.questions):
        st.markdown(f"**{i + 1}. {question}**")
        if quiz_type == "Multiple Choice":
            options = st.session_state.alternatives[i]
            selected_option = st.radio("Select your answer", options, key=f"question_{i}")
            option_index = options.index(selected_option)
            option_identifier = chr(97 + option_index)
            st.session_state.user_answers[i] = option_identifier
        elif quiz_type == "True/False":
            selected_option = st.radio("Select your answer", ["True", "False"], key=f"question_{i}")
            st.session_state.user_answers[i] = selected_option
        elif quiz_type == "Open-Ended":
            user_response = st.text_input("Your answer", key=f"question_{i}")
            st.session_state.user_answers[i] = user_response


# Function to Process Answers
def process_submission(quiz_type):
    if None in st.session_state.user_answers:
        st.warning("⚠️ Please answer all the questions before submitting.")
        return
    score = sum(1 for user, correct in zip(st.session_state.user_answers, st.session_state.answers) if user == correct)
    st.success(f"🎯 Your score: {score}/{len(st.session_state.questions)}")


if __name__ == "__main__":
    main()