# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 09:00:13 2024

@author: Francesco
"""
import random
import streamlit as st
import docx

# Function to read questions from docx file
def read_questions_from_docx(file_path):
    doc = docx.Document(file_path)
    questions = []
    current_question = None
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            if text.startswith("- A."):
                if current_question:
                    questions.append(current_question)
                current_question = {"question": current_question_text, "answers": [text], "correct": "A"}
            elif text.startswith("-"):
                current_question["answers"].append(text)
            else:
                current_question_text = text
    if current_question:
        questions.append(current_question)
    return questions

# Function to shuffle the answers
def shuffle_answers(questions):
    for question in questions:
        correct_answer = question["answers"][0]
        random.shuffle(question["answers"])
        question["correct"] = question["answers"].index(correct_answer)
    return questions

# Percorso del file con le domande
file_path = 'questions.docx'
questions = read_questions_from_docx(file_path)
shuffled_questions = shuffle_answers(questions)

# Streamlit app
def main():
    st.title("Quiz Game")

    if 'score' not in st.session_state:
        st.session_state.score = 0
        st.session_state.current_question_index = 0
        st.session_state.answers = [None] * len(shuffled_questions)

    if st.session_state.current_question_index < len(shuffled_questions):
        question = shuffled_questions[st.session_state.current_question_index]
        st.write(f"Q{st.session_state.current_question_index + 1}: {question['question']}")

        for i, answer in enumerate(question['answers']):
            if st.radio(f"Question {st.session_state.current_question_index + 1}", [f"{i}. {answer[3:]}"]) == f"{i}. {answer[3:]}":
                st.session_state.answers[st.session_state.current_question_index] = i

        if st.button("Next"):
            correct_answer = question['correct']
            if st.session_state.answers[st.session_state.current_question_index] == correct_answer:
                st.session_state.score += 1
            st.session_state.current_question_index += 1
            st.experimental_rerun()
    else:
        st.write(f"Your final score is {st.session_state.score} out of {len(shuffled_questions)}")
        if st.button("Restart"):
            st.session_state.score = 0
            st.session_state.current_question_index = 0
            st.session_state.answers = [None] * len(shuffled_questions)
            st.experimental_rerun()

if __name__ == "__main__":
    main()
