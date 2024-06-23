import streamlit as st
import pandas as pd
import sqlite3
from langchain.llms import GooglePalm
from langchain.chains import LLMChain
from langchain.prompts import FewShotPromptTemplate,PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

from few_shots import few_shots

# Function to create a database from Excel file
def create_db_from_excel(file_path):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path)

    # Create an SQLite database
    conn = sqlite3.connect('example.db')
    table_name = 'health_data'
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    return table_name

# Function to generate SQL query using LangChain and Google PaLM
def generate_sql_query(natural_query, table_name):
    llm = GooglePalm(google_api_key=os.getenv("GOOGLE_API_KEY"), temperature=0.1)
    
    # Define a simple prompt template to convert natural language to SQL
    example_prompt_template = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
        template="Question: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}\n"
    )

    prompt = FewShotPromptTemplate(
        examples=few_shots,
        example_prompt=example_prompt_template,
        prefix=("Translate the following natural language query into an SQL query for the table '{table}' "
                "which has columns Year, StateAbbr, LocationName, Category, Measure, Data_Value_Type, "
                "Data_Value, Low_Confidence_Limit, High_Confidence_Limit, "
                "TotalPopulation, LocationID, CategoryID, MeasureId, DataValueTypeID, Short_Question_Text, "
                "Counties. Use the exact column names and data values. Here are some examples:"),
        suffix=("Question: {query}\nSQLQuery:"),
        input_variables=["query", "table"]
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    sql_query = chain.run(query=natural_query, table=table_name)
    sql_query = sql_query.split('SQLResult:')[0].split('Answer:')[0].strip("```sql").strip("```").strip()
    return sql_query

# Function to execute the generated SQL query
def execute_sql_query(sql_query):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]  # Get column names
    conn.close()
    return results, columns

table_name = create_db_from_excel('database/health_data.xlsx')

# Streamlit app layout
st.title("Natural Language to SQL")

# Input from user
user_query = st.text_input("Enter your query:", "")

if st.button("Submit"):
    if user_query:
        try:
            # Generate and display SQL query
            sql_query = generate_sql_query(user_query, table_name)
            st.write(f"Generated SQL Query: `{sql_query}`")

            # Execute and display results
            results, columns = execute_sql_query(sql_query)
            st.write("Results:")
            st.write(pd.DataFrame(results, columns=columns))
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query.")
