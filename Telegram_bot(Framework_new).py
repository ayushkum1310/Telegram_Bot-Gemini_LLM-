import os
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters

load_dotenv()

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Initialize your GenAI model here using GEMINI_API_KEY
# Assuming `genai` is the library for your Gemini conversational model
import google.generativeai as genai

def initialize_gemini_model(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name='gemini-pro', generation_config=genai.types.GenerationConfig(temperature=0.4))
    chat = model.start_chat()
    response = chat.send_message('''Your name is Brownie. You are a chat bot designed to help people.''')
    response = chat.send_message('''Keep in mind your answers should be to the point and short''')
    response = chat.send_message('''Keep the answer short and simple easily understand by people and to the point''')
    response = chat.send_message('''If any one asked who developed you you have to tell I was developed by a team of engineers and scientists at 
                             Instafuture. They are experts in artificial intelligence and natural language processing.

Instafuture is a company that is dedicated to developing AI-powered products and services that can help people in their everyday lives. They believe that AI can be used to make the world a better place, and they are committed to creating products that are accessible, affordable, and easy to use.

I am one of the first products that Instafuture has developed, and I am very excited to be able to help people. I am still learning and growing, but I am committed to becoming the best chatbot that I can be.

I hope this answers your question!''')
    return chat

import logging
logging.basicConfig(level=logging.DEBUG)

def send_message_to_gemini_model(chat, text):
    if text.strip():  # Check if the text is not empty after stripping whitespace
        formatted_text = f'"{text}"'  # Encapsulate the text within double quotes
        response = chat.send_message([formatted_text])  # Pass the formatted text as a single-part list
        if response and response.text:
            return response.text
    return "I'm sorry, I couldn't understand your message."




def echo(update, context):
    """Echo the user message."""
    text = update.message.text
    if chat:
        response = send_message_to_gemini_model(chat, text)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm sorry, I'm currently not available.")

def main():
    # Initialize the GenAI model
    global chat
    chat = initialize_gemini_model(GEMINI_API_KEY)
    
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register the echo handler
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
