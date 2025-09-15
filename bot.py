from telebot import types, TeleBot
from fipi import load_subjects

bot = TeleBot('8438991402:AAH2kNsDOpM5xCN1lNYDS3MoHbeJEGZQQJ0')

zadanie1 = [['текст1', 1], ['текст2', 2], ['текст3', 3], ['текст4', 4], ['текст5', 5]]
question_number = -1

def add_button(title, data, buttons):
    buttons.add(types.InlineKeyboardButton(title, callback_data=data))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    buttons = types.InlineKeyboardMarkup()
    subjects = load_subjects()
    print(type(subjects))
    for subject in subjects:
        add_button(subject["title"], subject["data"], buttons)

    bot.send_message(message.chat.id, f"{message.chat.first_name}, добро пожаловать в телеграм бот Rocinante!", reply_markup=buttons)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    buttons = types.InlineKeyboardMarkup()
    buttons.add(types.InlineKeyboardButton('Тема 1', parse_mode='html', reply_markup=buttons, callback_data='theme1'))
    bot.send_message(message.chat.id, "Выбери тему".format(message.from_user), reply_markup=buttons)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    buttons = types.InlineKeyboardMarkup()
    global question_number
    if callback.data == 'theme1':
        question_number += 1
        buttons.add(types.InlineKeyboardButton('Ответ', parse_mode='html', reply_markup=buttons, callback_data=f'ans{question_number}'))
        bot.send_message(callback.message.chat.id, f'Задание 1: {zadanie1[0][0]}'.format(callback.message.from_user), reply_markup=buttons)
        # bot.delete_message(callback.message.chat.id, callback.message.message_id)
    if callback.data == f'ans{question_number}':
        if question_number < 4:
            buttons.add(types.InlineKeyboardButton('Далее', parse_mode='html', reply_markup=buttons, callback_data=f'next{question_number}'))
            bot.send_message(callback.message.chat.id, f'Ответ: {zadanie1[question_number][1]}'.format(callback.message.from_user), reply_markup=buttons)
        if question_number == 4:
            buttons.add(types.InlineKeyboardButton('Назад к выбору темы', parse_mode='html', reply_markup=buttons, callback_data='back'))
            bot.send_message(callback.message.chat.id, f'Ответ: {zadanie1[question_number][1]}'.format(callback.message.from_user), reply_markup=buttons)
        # bot.delete_message(callback.message.chat.id, callback.message.message_id)
    if callback.data == f'next{question_number}':
        question_number += 1
        buttons.add(types.InlineKeyboardButton('Ответ', parse_mode='html', reply_markup=buttons, callback_data=f'ans{question_number}'))
        bot.send_message(callback.message.chat.id, f'Задание {question_number+1}: {zadanie1[question_number][0]}'.format(callback.message.from_user), reply_markup=buttons)
        # bot.delete_message(callback.message.chat.id, callback.message.message_id)
    if callback.data == 'back':
        question_number = -1
        buttons = types.InlineKeyboardMarkup()
        buttons.add(types.InlineKeyboardButton('Тема 1', parse_mode='html', reply_markup=buttons, callback_data='theme1'))
        bot.send_message(callback.message.chat.id, "Выбери тему".format(callback.message.from_user), reply_markup=buttons)

bot.polling(none_stop=True, interval=0)
