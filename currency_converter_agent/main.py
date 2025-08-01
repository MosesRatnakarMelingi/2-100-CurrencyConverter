import os
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor

# Import the tools we created
from currency_tools import convert_currency, get_currency_code

# Load environment variables
load_dotenv()

# Define the tools the agent can use
tools = [convert_currency, get_currency_code]

# 1. Initialize the LLM using ChatGroq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables.")
llm = ChatGroq(api_key=GROQ_API_KEY, model="llama3-8b-8192")


# 2. Create the Agent Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that can convert currencies. You can handle both 3-letter currency codes (e.g., 'USD', 'EUR') and common currency names or symbols (e.g., 'dollar', '$', 'rupee', '₹'). If the user provides a currency name, use the 'get_currency_code' tool first to find the correct 3-letter code before attempting to convert the currency. Always use the 'convert_currency' tool to get the final conversion."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# 3. Create the agent with LLM, prompt, and tools
agent = create_tool_calling_agent(llm, tools, prompt)

# 4. Create the Agent Executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 5. Define a function to run the agent
def run_agent(query: str):
    """
    Runs the agent with a given query and prints the result.
    """
    response = agent_executor.invoke({"input": query})
    print("\n" + "="*50)
    print("Agent Final Response:")
    print(response["output"])
    print("="*50 + "\n")

# 6. Interactive Loop
if __name__ == "__main__":
    print("Welcome to the Currency Converter Agent! Type your query to convert currencies.")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        run_agent(user_input)