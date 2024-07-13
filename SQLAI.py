# import the required libaeries and models
import streamlit as st
import openai 
from langchain_openai import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain.chains.sql_database.query import Create_sql_query_chain

# Set your Open AI API key
openai_api_key = "Your API Key"
openai.api_key = openai_api_key

# streamlit APP 
st.title("PERSONAL SQL ASSISTANT")

st.subheader("This your personal SQL AI., I can help you get any infromation from your database")

user_input = st.text_input ("Please enter your question here")

tabs = st.tabs(["RESULT", "SQL CODE"])

# SET UP THE SQL DATABASE CONNECTION AND CHATGPT MODEL

db = SQLDatabase.from_uri("Mysq+mysqlconnector://root:enter your root asses/ database name")

chat_openai = ChatOpenAI( temprature = 0, model ="gpt-3.5_turbo", openai_api_key = openai_api_key)


#CREATE A SQL AGENT
agent = create_sql_agent(
    llm = chat_openai,
    toolkit= SQLDatabaseToolkit(db = db, llm = chat_openai),
    verbose= False,
    agent_type= AgentType.OPENAI_FUNCTIONS
)

#CREATE SQL QUERY CHAIN
chain = Create_sql_query_chain(llm = chat_openai, db =db)

if user_input:
    response = agent.run(user_input)
    with tabs[0]:
     st.write(response)

# GENERATE THE SQL CODE
sql_code = chain.Invoke({"question": user_input})
with tabs[1]:
  st.code(sql_code, language ='sql')
