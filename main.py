from config import TOKEN
from data import STOP_WORDS
from stop_words_logic import stop_logic
import telebot

bot=telebot.TeleBot(token=TOKEN)

@bot.message_handler(content_types=["text"])
def print_parrot(message):
    if stop_logic(message.text):
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, 'Не пишите такие слова')
    else:
        bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)