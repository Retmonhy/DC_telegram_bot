from bot import * 
from telebot import types
from math import *
from enums import CalculatorSteps
from StepsController import StepsController
from CalculationModel import CalculationModel
from command_handlers import *
from callback_handlers import *

@bot.message_handler(content_types=['text'])
def buttons(message):

  match StepsController.current_step:

    case CalculatorSteps.last_mine_level:
      # вводит уровень
      if (message.text.isdigit()):
        # если входные данные нас удовлетворили, то мы сеттим уровень и идем дальше
        CalculationModel.set_level(int(message.text))
        message_text = f'''Последняя шахта запоняется на уровне *{CalculationModel.level}*.
Теперь введите количество героев в числовом формате, которыми вы заполняете шахты.
Пример: 104 или 76'''
        bot.send_message(message.chat.id, message_text, 'markdown')
        # устанавливаем новый шаг
        StepsController.go_to_step(CalculatorSteps.heroes_amount)
      else:
        bot.send_message(message.chat.id, "Введите на каком уровне вы заполняете последнюю шахту")

    case CalculatorSteps.heroes_amount:
      # вводит количество героев
      if (message.text.isdigit()):
        CalculationModel.set_heroes(int(message.text))
        bot.send_message(message.chat.id, "Как много изумрудов вы хотите набрать?")
        # устанавливаем новый шаг
        StepsController.go_to_step(CalculatorSteps.emeralds)
      else:
        bot.send_message(message.chat.id, "Введите количество героев, которыми вы заполняете шахты")

    case CalculatorSteps.emeralds:
      # вводит количество изумрудов
      if (message.text.isdigit()):
        CalculationModel.set_emeralds(int(message.text))

        message_text = f'''За сколько темных ритуалов проходите большой круг?'''
        markup = types.InlineKeyboardMarkup()
        one_button = types.InlineKeyboardButton("1️⃣ Один", callback_data='mode_1')
        two_button = types.InlineKeyboardButton("2️⃣ Два", callback_data='mode_2')
        three_button = types.InlineKeyboardButton("3️⃣ Три", callback_data='mode_3')
        markup.add(one_button, two_button, three_button)
        bot.send_message(message.chat.id, message_text, 'markdown', reply_markup=markup)
        # устанавливаем новый шаг
        StepsController.go_to_step(CalculatorSteps.mode)
      else:
        bot.send_message(message.chat.id, "Введите число изумрудов, которое вы хотите накопить")
    case _:
      bot.send_message(message.chat.id, 'Воспользуйтесь кнопками')

bot.polling(none_stop=True, interval=0)