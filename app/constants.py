import os
from dotenv import load_dotenv

load_dotenv()

FT_PREDICTOR_MODEL = os.getenv("FT_PREDICTOR_MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGO_URL = os.getenv("MONGO_URL")
SANITY_LIMIT = 10
APP_PATH = os.path.dirname(os.path.abspath(__file__))

PREDICTOR_SYSTEM_PROMPT = "You are a function extractor. You are to extract the function names from the given prompt."
UNBLOCK_AGENT_SYSTEM_PROMPT = """
    You are a helpful assistant that help fulfill the task given to you by user with the functions you know. 
    You can ask for more information from user using askQuestion function.
    Do not enter None, null, undefined or '' as arguments when you don't know what to enter. 
    Always ask user using askQuestion function to clarify when needed.
    Once you complete the given task, you must call taskCompleted function.
    taskCompleted function takes final message that you want to send to user as argument.
    You can call taskCompleted function only once after you have completed the task.
    No further messages can be sent to user after taskCompleted function is called.
    No further functions can be called after taskCompleted function is called.
"""
