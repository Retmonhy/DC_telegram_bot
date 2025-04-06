from bot import * 
from helpers import calculate_emeralds_per_cycle
import prettytable as pt
from telebot import types
from math import *
from steps import CalculatorSteps
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
        # переключаем шаг 
        StepsController.go_to_step(CalculatorSteps.heroes_amount)
        CalculationModel.set_level(int(message.text))
        message_text = f'''Последняя шахта запоняется на уровне *{CalculationModel.level}*.
Теперь введите количество героев в числовом формате, которыми вы заполняете шахты.
Пример: 104 или 76'''
        bot.send_message(message.chat.id, message_text, 'markdown')
      else:
        bot.send_message(message.chat.id, "Введите на каком уровне вы заполняете последнюю шахту")

    case CalculatorSteps.heroes_amount:
      # вводит количество героев
      if (message.text.isdigit()):
        StepsController.go_to_step(CalculatorSteps.emeralds)
        CalculationModel.set_heroes(int(message.text))
        bot.send_message(message.chat.id, "Как много изумрудов вы хотите набрать?")
      else:
        bot.send_message(message.chat.id, "Введите количество героев, которыми вы заполняете шахты")

    case CalculatorSteps.emeralds:
      # вводит количество изумрудов
      if (message.text.isdigit()):
        StepsController.go_to_step(CalculatorSteps.result)
        CalculationModel.set_emeralds(int(message.text))
        message_text = get_message_with_parameters()
        markup = types.InlineKeyboardMarkup()
        calculate_button = types.InlineKeyboardButton("🚀 Рассчитать", callback_data='get_result')
        markup.add(calculate_button)
        bot.send_message(message.chat.id, message_text, 'markdown', reply_markup=markup)
      else:
        bot.send_message(message.chat.id, "Введите число изумрудов, которое вы хотите накопить")

    case CalculatorSteps.result:
      if (message.text != "🚀 Рассчитать"):
        bot.send_message(message.chat.id, 'Воспользуйтесь кнопками')
    case CalculatorSteps.end:
      value=1
    case _:
      bot.send_message(message.chat.id, 'Воспользуйтесь кнопками')
    



def get_message_with_parameters():
    table = pt.PrettyTable(['Параметр', 'Значение'])
    table.align['Параметр'] = 'l'
    table.align['Значение'] = 'r'

    data = [
        ('Уровень', ceil(CalculationModel.level)),
        ('Герои', ceil(CalculationModel.heroes)),
        ('Изумруды', ceil(CalculationModel.emeralds)),
    ]
    for parameter, value in data:
        table.add_row([parameter, f'{value:.2f}'])

    return f'```Расчет будет осуществлен по следующим параметрам: \n{table}```'

bot.polling(none_stop=True, interval=0)