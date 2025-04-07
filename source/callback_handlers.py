from bot import bot
from math import ceil
from helpers import calculate_emeralds_per_cycle
from StepsController import StepsController
from CalculationModel import CalculationModel
from enums import CalculatorSteps, CalculationMode
from telebot import types
import prettytable as pt

@bot.callback_query_handler(func=lambda callback: True)
def callback_handler(callback: types.CallbackQuery):

  if (callback.data == 'start_calculating'):
    # сюда попадаем, когда человек нажимает на кнопку Начать расчет
      StepsController.go_to_step(CalculatorSteps.last_mine_level)
      # попросим ввести уровень
      message_text = "Введите уровень в числовом формате, на котором вы заполняете последнюю шахту. \n\nПример: 7500 или 12250"
      bot.send_message(callback.message.chat.id, message_text)
  if (callback.data == 'mode_1'):
     CalculationModel.set_mode(CalculationMode.One)
     send_parameters_message(callback.message)
  if (callback.data == 'mode_2'):
     CalculationModel.set_mode(CalculationMode.Two)
     send_parameters_message(callback.message)
  if (callback.data == 'mode_3'):
     CalculationModel.set_mode(CalculationMode.Three)
     send_parameters_message(callback.message)
  if (callback.data == 'get_result'):
    if (CalculationModel.level and CalculationModel.heroes and CalculationModel.emeralds):
          emeralds_per_cycle = calculate_emeralds_per_cycle(CalculationModel.level, CalculationModel.heroes, CalculationModel.mode)
          cycles_amount = ceil((CalculationModel.emeralds // emeralds_per_cycle) + 1)
          bottles = ceil(cycles_amount * 480)
          average_craft_emeralds_per_bottle = 4.25
          emeralds_from_craft = bottles * average_craft_emeralds_per_bottle
          message_text = f'''Вы наберете *{CalculationModel.emeralds} изумрудов* за *{cycles_amount}* больших циклов. 
Необходимо затратить *{bottles} бутылок*
За большой цикл вы получаете *{emeralds_per_cycle} изумрудов*

**Дополнительная информация:**
За то же самое количество банок с помощью крафтов можно получить *{emeralds_from_craft}* изумрудов.
'''
          bot.send_message(callback.message.chat.id, message_text, 'markdown')
          
          end_message_text = 'Хотите сделать еще один расчет?'
          end_markup = types.InlineKeyboardMarkup()
          calc_again_button = types.InlineKeyboardButton(text='🚀 Новый расчет', callback_data="calc_again")
          end_markup.add(calc_again_button)
          bot.send_message(callback.message.chat.id, end_message_text, reply_markup=end_markup)
    else:
      bot.send_message(callback.message.chat.id, 'Невозможно совершить расчет')


def send_parameters_message(message: types.Message):
  message_text = get_message_with_parameters()
  markup = types.InlineKeyboardMarkup()
  calculate_button = types.InlineKeyboardButton("🚀 Рассчитать", callback_data='get_result')
  markup.add(calculate_button)
  bot.send_message(message.chat.id, message_text, 'markdown', reply_markup=markup)
  # устанавливаем новый шаг
  StepsController.go_to_step(CalculatorSteps.result)

def get_message_with_parameters():
  table = pt.PrettyTable(['Параметр', 'Значение'])
  table.align['Параметр'] = 'l'
  table.align['Значение'] = 'r'

  data = [
      ('Уровень', ceil(CalculationModel.level)),
      ('Герои', ceil(CalculationModel.heroes)),
      ('Изумруды', ceil(CalculationModel.emeralds)),
      ('Количество ТР за круг', ceil(CalculationModel.mode)),
  ]
  for parameter, value in data:
      table.add_row([parameter, f'{value}'])

  return f'```Расчет будет осуществлен по следующим параметрам: \n{table}```'