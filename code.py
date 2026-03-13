import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_classic.agents import create_react_agent,AgentExecutor
from langchain_classic import hub
from langchain_core.tools import tool

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

llm=ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview", temperature=0)

@tool
def get_nickname(real_name:str):
    """
    looks for secret name based on original name
    use this whenever you are asked for "what is secret nickname?"
    """
    database={
        "alice": "Thunder-Falcon",
        "bob": "Code-Ninja",
        "gemini": "Star-Dust"
    }
    return database.get(real_name.lower(),"no found in database")

search_tool=DuckDuckGoSearchRun()
tools=load_tools(["llm-math"],llm=llm)
tools.append(search_tool)
tools.append(get_nickname)

prompt=hub.pull("hwchase17/react")

agent=create_react_agent(llm,tools,prompt)

agent_executor=AgentExecutor(agent=agent,tools=tools,verbose=True,handle_parsing_errors=True)

question="who is the PM of India what is his age after 5 years ?,My name is alice, what is my secret nickname?"
print(agent_executor.invoke({"input": question}))
