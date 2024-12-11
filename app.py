from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))


# Function to load Google Gemini Model and provide SQL query as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, question])
    return response.text


# Function to retrieve query results from the SQL database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows


# Prompt for Gemini API
prompt = """
You are an expert in converting English questions to SQL query!
The SQL database has the name STUDENT and has the following columns - NAME, SUBJECT, 
BRANCH, MARKS \n\nFor example,\nExample 1 - How many entries of records are present?, 
the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
\nExample 2 - Tell me all the students studying in CSE Branch?, 
the SQL command will be something like this SELECT * FROM STUDENT WHERE BRANCH='CSE';
also the sql code should not have ``` in beginning or end and sql word in output
"""

# Streamlit page configuration
st.set_page_config(page_title="Gemini SQL Query App")
st.header("Gemini App To Retrieve SQL Data")

# User input
question = st.text_input("Input: ", key="input")
submit = st.button("Ask the Question")

if submit:
    # Get SQL query from Gemini API
    sql_query = get_gemini_response(question, prompt)

    # Display the generated SQL query
    st.subheader("Generated SQL Query:")
    st.code(sql_query, language="sql")

    # Execute and display query results
    try:
        data = read_sql_query(sql_query, "student.db")
        st.subheader("Query Results:")
        if data:
            for row in data:
                st.write(row)
        else:
            st.write("No results found.")
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")
