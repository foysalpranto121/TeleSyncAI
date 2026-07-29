from aiogram import Bot, Dispatcher, executor, types

import openai
import sys
import os


from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))

class Reference:
   """  
   A class to store previous messages and their responses from the OpenAI API.
   
   
   """

   def __init__(self)->None:
      
      self.response = "" 

reference=Reference()


def _clear_past_messages():

    """
    clears the  past response from the reference object
    """
    global reference
    reference.response = ""