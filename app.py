import streamlit as st
import json
import re

# Load questions data from JSON file
def load_questions(filename='questions.json'):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

questions_data = load_questions()

def letter_to_index(letter):
    return ord(letter) - ord('A')

def clean_html_tags(text):
    """Remove <p> and </p> tags from the text."""
    text = re.sub(r'^<p>', '', text)
    text = re.sub(r'</p>$', '', text)
    return text

def main():
    st.title("Quiz Interface")

    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'selected_option' not in st.session_state:
        st.session_state.selected_option = None
    if 'answer_shown' not in st.session_state:
        st.session_state.answer_shown = False

    def display_question(question_index):
        question = questions_data[question_index]
        st.subheader(question['skill'])
        st.write(f"Question {question_index + 1}/{len(questions_data)}")

        # Render HTML content safely
        stimulus = clean_html_tags(question['question']['stimulus'])
        stem = clean_html_tags(question['question']['stem'])
        st.markdown(stimulus, unsafe_allow_html=True)
        st.write(stem)

        options = question['question']['answerOptions']
        option_labels = [clean_html_tags(option) for option in options]

        selected_option = st.radio(
            "Select an option:",
            option_labels,
            index=st.session_state.selected_option if st.session_state.selected_option is not None else 0
        )

        # Create columns for buttons
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            if st.button('Previous', key='previous_button'):
                st.session_state.current_question = (st.session_state.current_question - 1) % len(questions_data)
                st.session_state.answer_shown = False

        with col2:
            if st.button('Check', key=f'check_button_{question_index}'):
                st.session_state.selected_option = option_labels.index(selected_option)
                st.session_state.answer_shown = True

        with col3:
            if st.button('Next', key='next_button'):
                st.session_state.current_question = (st.session_state.current_question + 1) % len(questions_data)
                st.session_state.answer_shown = False

        if st.session_state.answer_shown:
            correct_index = letter_to_index(question['question']['correctAnswer'])
            for idx, option in enumerate(option_labels):
                color = 'green' if idx == correct_index else 'red' if idx == st.session_state.selected_option and idx != correct_index else 'black'
                st.markdown(f"<div style='color: {color};'>{option}</div>", unsafe_allow_html=True)
                if idx == st.session_state.selected_option or idx == correct_index:
                    rationale = clean_html_tags(question['question']['rationale'][idx])
                    st.markdown(rationale, unsafe_allow_html=True)

    display_question(st.session_state.current_question)

if __name__ == '__main__':
    main()
