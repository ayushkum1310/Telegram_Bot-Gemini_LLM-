import telegram.ext
from telegram.ext import CommandHandler, MessageHandler,filters
import google.generativeai as genai
from dotenv import load_dotenv
from queue import Queue
update_queue = Queue()

load_dotenv()
import os

api_key = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=api_key)
Token = os.environ.get('TELEGRAM_TOKEN')

updater = telegram.ext.Updater(Token,use_context=True)
dispatcher = updater.dispatcher

model = genai.GenerativeModel(model_name='gemini-pro', generation_config=genai.types.GenerationConfig(max_output_tokens=250, temperature=0.4))
chat = model.start_chat()

#Customizing the chat bot accouring to our need
response = chat.send_message('''Your name is Brownie. You are a chat bot designed to help people.''')
response = chat.send_message('''Keep in mind your answers should be to the point and short''')
response = chat.send_message('''Keep the answer short and simple easily understand by people and to the point''')
response = chat.send_message('''If any one asked who developed you you have to tell I was developed by a team of engineers and scientists at 
                             Instafuture. They are experts in artificial intelligence and natural language processing.

Instafuture is a company that is dedicated to developing AI-powered products and services that can help people in their everyday lives. They believe that AI can be used to make the world a better place, and they are committed to creating products that are accessible, affordable, and easy to use.

I am one of the first products that Instafuture has developed, and I am very excited to be able to help people. I am still learning and growing, but I am committed to becoming the best chatbot that I can be.

I hope this answers your question!''')

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hello! My name is Brownie your personal chat bot. Ask me anything.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def help(update,context):
    context.bot.send_message(chat_id=update.message.chat_id,text='''/start -> To start\n/Ask or simple text -> To ask\n/help -> For this message''')
                             

help_handelar=CommandHandler('help',help)
dispatcher.add_handler(help_handelar)

def Ask(update, context):
    try:
        user_input = update.message.text
        response = chat.send_message(user_input)
        context.bot.send_message(chat_id=update.message.chat_id, text=response.text)
    except Exception as e:
            context.bot.send_message(chat_id=update.message.chat_id, text="Sorry,Due to Security issues i can't answer you,Try something else.(Note:Don't ask about other Ai)")

message_handler = MessageHandler(filters.Filters.text & ~filters.Filters.command, Ask)
dispatcher.add_handler(message_handler)

updater.start_polling()
updater.idle()

