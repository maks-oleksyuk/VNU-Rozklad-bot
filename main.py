import commands
import mes_text
from variables import bot


@bot.message_handler(commands=["start"])
def start(message):
    commands.start(message)


@bot.message_handler(commands=["change"])
def change(message):
    commands.change(message)


@bot.message_handler(commands=["about"])
def about(message):
    commands.about(message)


@bot.message_handler(commands=["help"])
def about(message):
    commands.help(message)


@bot.message_handler(commands=["cancel"])
def cancel(message):
    commands.cancel(message)


@bot.message_handler(content_types=["text"])
def text(message):
    mes_text.text(message)
    # bot.delete_message(message.chat.id, message.message_id)


bot.polling(non_stop=True)
