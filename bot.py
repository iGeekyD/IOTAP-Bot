import telebot



#main variables
TOKEN = "1270963540:AAEuQ7n9g6TWi5jaMwCGE36dAMRzYiR_PkA"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['go'])
def start_handler(message):
    bot.send_message(message.chat.id, 'Привет, когда я вырасту, я буду парсить заголовки с Хабра')

bot.polling()