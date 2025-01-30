from g4f.client import Client
import telebot
from telebot import TeleBot
from telebot import types

API_TOKEN = '7638889053:AAEImpNVav_UvU7xfPg1JrLkli5LYJcN2f0'
bot = telebot.TeleBot(API_TOKEN)

client = Client()

# print("Добро пожаловать в GPT-4o Mini Chat!")
# print("Введите 'exit', чтобы выйти из чата.")

conversation_history = {}

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("/start")
markup.add(btn1)
def trim_history(history, max_length=4096):
    current_length = sum(len(message["content"]) for message in history)
    while history and current_length > max_length:
        removed_message = history.pop(0)
        current_length -= len(removed_message["content"])
    return history


@bot.message_handler(commands=['start'])
def process_start_command(message):
    bot.reply_to(message, "Hi, I am an AGS bot made by spectacular KeepInTouch (StudentGov) team. Go ahead and chat with this bot. \nTo find other commands, enter /help")

@bot.message_handler(commands=['help'])
def process_help_command(message):
    bot.reply_to(message, "/start - start dialogue \n/clear - clear diaogue history \n/stats - shows the number of messages in dialogue history \n/anon - sends an anonymous message to the teacher or a student. Specify the name")

@bot.message_handler(commands=['clear'])
def process_clear_command(message):
    user_id = message.from_user.id
    conversation_history[user_id] = []
    bot.reply_to(message, "history cleaned")

@bot.message_handler(commands=['stats'])
def process_stats_command(message):
    number_mes = len(conversation_history)
    bot.reply_to(message, str(number_mes)+" messages in the dialogue history")

@bot.message_handler(commands=['anon'])
def process_anon_command(message):
    user_message = message.text
    user_id = message.from_user.id
    username = message.from_user.username  # Get the username (if available)

    # Prepare the message to forward
    if username:
        sender_info = f"Sender: @{username} (ID: {user_id})"
    else:
        sender_info = f"Sender: (ID: {user_id})"

    forwarded_message = f"Anonymous Message:\n{user_message}\n\n{sender_info}"

    # Forward the message to your account
    bot.send_message(chat_id=1249376888, text=forwarded_message)

    # Notify the user
    bot.reply_to(message, "Your message has been sent anonymously")



@bot.message_handler(content_types=['text'])
def gptresponse(message):
    user_id = message.from_user.id
    user_input = message.text






    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append({"role": "user", "content": user_input})
    conversation_history[user_id] = trim_history(conversation_history[user_id])

    if len(user_input) > 500:
            bot.send_message(message.from_user.id, 'The message is exceeding the limit (500 characters). Shorten your message')
            user_id = message.from_user.id
            user_input = message.text


    if len(user_input) <= 500:
        try:

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=conversation_history[user_id]
            )
            gptresponse = response.choices[0].message.content
            conversation_history[user_id].append({"role": "assistant", "content": gptresponse})

            bot.reply_to(message, gptresponse)
        except Exception as e:
            print(f"Error while processing GPT request: {e}")
            bot.reply_to(message, "Sorry, try again")



if __name__ == "__main__":
    bot.polling(none_stop=True)
