import streamlit as st
import pandas as pd
import os
import openai
from dotenv import load_dotenv
from zip import create_zip_file
from email_utils import send_email_with_attachments
from telegram import send_to_telegram
from QA import ask_about_data
from report_generation import generate_report_with_chatgpt

# Set page configuration at the very beginning
st.set_page_config(
    page_title="DCx Co.,ltd",
    page_icon="https://dcxsea.com/asset/images/logo/LOGO_DCX.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key from environment variable
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Custom CSS for the buttons
st.markdown("""
    <style>
    div.stButton > button {
        width: auto;
        height: 40px;
        margin-top: 11px;
        background-color: green;
        color: white;
    }
    div.stButton > button:hover {
        background-color: darkgreen;
    }
    </style>
    """, unsafe_allow_html=True)

def dashboard():
    
    
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        .main {
            max-width: 1200px;
            margin: 0 auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="display: flex; align-items: center;">
            <img src="https://cdn3d.iconscout.com/3d/free/thumb/free-line-chart-growth-3814121-3187502.png" alt="logo" style="width: 90px; margin-right: 15px;">
            <h3 style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; margin-top: 0;">ការបន្សាំកសិកម្មជនជាតិដើមភាគតិច</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # File uploader to allow users to upload their data
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            # Store the dataframe in session state
            st.session_state['df'] = df
            # st.success("File uploaded successfully!")
        except Exception as e:
            st.error(f"Failed to read uploaded file: {e}")
    else:
        st.error("Please upload a dataset to proceed.")

    if 'df' in st.session_state:
        df = st.session_state['df']

        # Create tabs for the three sections
        tab1, tab2, tab3 = st.tabs(["Q&A", "Generate Report", "Send Email"])

        # Tab 1: Q&A Section
        with tab1:
            # st.subheader("Uploaded Data")
            st.dataframe(df)

            # st.markdown(
            #     """
            #     <div style="display: flex; align-items: center;">
            #         <label for="question_input" style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; font-size: 14px;">សូមបញ្ចូលសំណួរ:</label>
            #     </div>
            #     """,
            #     unsafe_allow_html=True
            # )

            # question = st.text_input(" ", key="question_input_key")
            # if st.button("Search"):
            #     if question.strip():
            #         st.session_state["search_result"] = ask_about_data(df, question)
            #     else:
            #         st.error("Please enter a question.")

            # if "search_result" in st.session_state:
            #     st.write(st.session_state["search_result"])
            st.markdown(
            """
            <div style="display: flex; align-items: center;">
                <label for="question_input" style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; font-size: 14px;">សូមបញ្ចូលសំណួរ:</label>
            </div>
            """,
            unsafe_allow_html=True
            )
            col1, col2 = st.columns([3, 1])
            with col1:
                # Text input field
                question = st.text_input(" ", key="question_input_key")

            with col2:
                st.markdown("""
                    <style>
                    div.stButton > button {
                        width: auto;
                        height: 40px;
                        margin-top: 11px;
                        background-color: #a9cce3 ;
                    }
                    div.stButton > button:hover {
                        background-color: #5d6d7e ;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                search = st.button("Search")

            # Display the answer if the button is clicked
            if search and question:
                st.session_state["search_result"] = ask_about_data(df, question)

            if "search_result" in st.session_state:
                st.write(st.session_state["search_result"])


        # Tab 2: Generate Report Section
        with tab2:
            # st.subheader("Uploaded Data")
            st.dataframe(df)

            st.markdown(
                """
                <div style="display: flex; align-items: center;">
                    <label for="prompt_input" style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; font-size: 14px;">សូមបញ្ចូល prompt ដើម្បីបង្កើតរបាយការណ៍:</label>
                </div>
                """,
                unsafe_allow_html=True
            )

            user_prompt = st.text_area(" ", key="prompt_input_key")

            if st.button('Generate Report'):
                if not user_prompt.strip():
                    st.error("Please enter a prompt to generate the report.")
                else:
                    df_cleaned = df.fillna('')
                    data = df_cleaned.to_dict(orient='records')

                    report_title = "Generated Report"
                    report_content, word_filename, pdf_filename = generate_report_with_chatgpt(df_cleaned, report_title, user_prompt)

                    if report_content:
                        zip_filename = f'{report_title}.zip'
                        create_zip_file(word_filename, pdf_filename, zip_filename)

                        st.session_state['report_generated'] = {
                            'zip_filename': zip_filename,
                            'word_filename': word_filename,
                            'pdf_filename': pdf_filename,
                            'report_title': report_title  # Store report title in session state
                        }

                        st.download_button(f'Download {report_title}', data=open(zip_filename, 'rb').read(), file_name=zip_filename, mime='application/zip')
                    else:
                        st.error("Failed to generate report.")

        # Tab 3: Send Email Section
        with tab3:
            if 'report_generated' in st.session_state:
                st.markdown(
                    """
                    <div style="display: flex; align-items: center;">
                        <label for="email_input" style="font-family: 'Khmer OS Muol Light', Arial, sans-serif; font-size: 14px;">សូមបញ្ចូលអ៊ីម៉ែលអ្នកទទួល</label>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                email_input = st.text_input(" ", key="email_input_key")

                if st.button('Send Email'):
                    if not email_input.strip():
                        st.error("Please enter an email address.")
                    else:
                        zip_filename = st.session_state['report_generated']['zip_filename']
                        word_filename = st.session_state['report_generated']['word_filename']
                        pdf_filename = st.session_state['report_generated']['pdf_filename']
                        report_title = st.session_state['report_generated']['report_title']

                        send_email_with_attachments(f"{report_title} Generated Report", "Please find the attached reports.", [zip_filename], to_email=[email_input])

                        # Send report to Telegram
                        send_to_telegram(word_filename, f"Here is your generated {report_title} (Word).")
                        send_to_telegram(pdf_filename, f"Here is your generated {report_title} (PDF).")
            else:
                st.error("Please generate a report first.")


