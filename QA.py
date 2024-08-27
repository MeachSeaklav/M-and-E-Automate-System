import openai
import streamlit as st

def ask_about_data(data, question):
    try:
        prompt = f"Given the following data:\n{data.to_csv(index=False)}\nAnswer the following question: {question}"

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a data analyst."}, {"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.5
        )

        answer = response.choices[0].message['content'].strip()
        return answer
    except Exception as e:
        st.error(f"Failed to get a response: {e}")
        return None