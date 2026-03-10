from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
import pandas as pd

def ask_supply_chain_agent(df: pd.DataFrame, question: str, api_key: str, model_choice: str) -> str:
    """
    Takes a natural language question and a dataframe, and uses the selected LLM to return an answer.
    """
    if not api_key:
        return f"Please provide a valid {model_choice} API Key in the sidebar."
        
    try:
        # Initializing the correct LLM based on user selection
        if model_choice == "OpenAI":
            # OpenAI gpt-5.4
            llm = ChatOpenAI(temperature=0, openai_api_key=api_key, model="gpt-5.4")
        elif model_choice == "Gemini":
            # Google gemini 2.5 flash
            llm = ChatGoogleGenerativeAI(temperature=0, google_api_key=api_key, model="gemini-2.5-flash")
        elif model_choice == "Claude":
            # Anthropic claude haiku 4.5
            llm = ChatAnthropic(temperature=0, anthropic_api_key=api_key, model_name="claude-haiku-4-5")
        else:
            return "Invalid model selection."
        
        # Create the Pandas DataFrame Agent
        agent = create_pandas_dataframe_agent(
            llm, 
            df, 
            verbose=True, # Set to True to watch it think in the terminal
            allow_dangerous_code=True,
            handle_parsing_errors=True,
            max_iterations=3 # Prevents infinite loops if the model gets stuck
        )
        
        # Prompt and Invoke
        prompt = f"""
        You are a Supply Chain AI Assistant. Answer the following question based on the provided dataframe.
        Explain your reasoning briefly. 
        Question: {question}
        """
        
        response = agent.invoke(prompt)
        return response.get("output", "I could not formulate an answer.")
        
    except Exception as e:
        return f"**Agent Error:** I couldn't process that question with {model_choice}. \n\n*(Technical detail: {str(e)})*"