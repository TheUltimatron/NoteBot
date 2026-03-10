import telebot
import json
import os

note_file = 'notes.json'

if not os.path.exists(note_file):
    with open(note_file, 'w') as file:
        json.dump({}, file)

TOKEN = '8754215918:AAEqwTiMXyEBozmFFsBnhcNPLbQ7Y85mqC8'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я NoteBot. Я могу помочь тебе сохранять заметки. Просто отправь мне текст, и я сохраню его для тебя.")
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("Показать заметки")
    markup.add(item1)
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)
    
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "Показать заметки":
        with open(note_file, 'r') as file:
            notes = json.load(file)
        user_notes = notes.get(str(message.chat.id), [])
        if user_notes:
            bot.send_message(message.chat.id, "Твои заметки:\n" + "\n".join(user_notes))
        else:
            bot.send_message(message.chat.id, "У тебя нет заметок.")
    else:
        with open(note_file, 'r') as file:
            notes = json.load(file)
        user_notes = notes.get(str(message.chat.id), [])
        user_notes.append(message.text)
        notes[str(message.chat.id)] = user_notes
        with open(note_file, 'w') as file:
            json.dump(notes, file)
        bot.send_message(message.chat.id, "Заметка сохранена!")
        

bot.polling()
