from bot import bot 
from telebot import types
from StepsController import StepsController
from steps import CalculatorSteps;

@bot.message_handler(commands=['start'])
def start_message(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  start_calc_button = types.KeyboardButton("🚀 Начать расчет")
  markup.add(start_calc_button)
  StepsController.go_to_step(CalculatorSteps.start)
  message_text = f'''Привет, {message.from_user.first_name} 👋\nНу что, начнем расчет?'''
  bot.send_message(message.chat.id, message_text, reply_markup=markup)

@bot.message_handler(commands=['terms'])
def write_terms(message):
  message_text = f'''Термины и понятия
*Тайм тревел(ТТ)* - механизм получения изумрудов путём заполнения шахт героями и перемотки времени.
*Шахта* - место, куда отправляются герои для майнинга изумрудов. Для заполнени яодной шахты требуется 4 героя.
*Изумруды* - игровой ресурс, необходимый для открытия новых героев.
*Бутылки* - игровой ресурс, необходимый для выполнения тайм тревела.
*Большой круг* - большой цикл шахт равный 192 часам, за который отработают все 192-часовые шахты.
*Малый круг* - малый цикл шахт равный 64 часам, за который отработают все 60-часовые шахты.
'''
  bot.send_message(message.chat.id, message_text,parse_mode='markdown')