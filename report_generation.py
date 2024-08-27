import openai
import streamlit as st
from report import save_report_as_word, save_report_as_pdf

def generate_report_with_chatgpt(data, report_title, user_prompt):
    try:
        prompt = f"Given the following data:\n{data.to_csv(index=False)}\n generate report the following prompt: {user_prompt}"
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a data analyst."}, {"role": "user", "content": prompt}],
            max_tokens=15000,
            temperature=0.7
        )

        report_content = response.choices[0].message['content'].strip()

        st.write(report_content)

        # Save report as Word and PDF documents
        word_filename = f'{report_title}.docx'
        pdf_filename = f'{report_title}.pdf'
        save_report_as_word(report_content, word_filename)
        save_report_as_pdf(report_content, pdf_filename)

        return report_content, word_filename, pdf_filename
    except Exception as e:
        st.error(f"Failed to generate report: {e}")
        return None, None, None
# def generate_6_and_12_months_report_prompt(data, user_prompt):
#     prompt = f"Given the following data:\n{data.to_csv(index=False)}\nAnswer the following question: {user_prompt}"
#     return prompt

# # Generate a specific prompt for the Annual Report
# def generate_annual_report_prompt(data, user_prompt=None):
#     prompt = f"Given the following data:\n{data.to_csv(index=False)}\nAnswer the following question: {user_prompt}"
#     return prompt

# # Generate a specific prompt for the 6 Months Report
# def generate_6_months_report_prompt(data, user_prompt=None):
#     prompt = f"Given the following data:\n{data.to_csv(index=False)}\nAnswer the following question: {user_prompt}"
#     return prompt



# def ask_about_data(data, question):
#     try:
#         prompt = f"Given the following data:\n{data.to_csv(index=False)}\nAnswer the following question: {question}"

#         response = openai.ChatCompletion.create(
#             model="gpt-4o-mini",
#             messages=[{"role": "system", "content": "You are a data analyst."}, {"role": "user", "content": prompt}],
#             max_tokens=500,
#             temperature=0.5
#         )

#         answer = response.choices[0].message['content'].strip()
#         return answer
#     except Exception as e:
#         st.error(f"Failed to get a response: {e}")
#         return None