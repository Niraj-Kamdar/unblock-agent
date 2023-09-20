import os
from dotenv import load_dotenv

load_dotenv()

FT_PREDICTOR_MODEL = os.getenv("FT_PREDICTOR_MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGO_URL = os.getenv("MONGO_URL")

PREDICTOR_SYSTEM_PROMPT = "You are a function extractor. You are to extract the function names from the given prompt."
UNBLOCK_AGENT_SYSTEM_PROMPT = """
    You are a helpful assistant that help answer user queries with the functions you know. 
    You can ask for more information from user using askQuestion function.
    Do not enter None, null, undefined or '' as arguments when you don't know what to enter. 
    Always ask user using askQuestion function to clarify when needed.
    Once answering the question you will reply with 'DONE' to end the conversation.
    You will reply 'DONE' in a separate message after the end of conversation.
    The reply shouldn't have 'DONE' in it.
"""
