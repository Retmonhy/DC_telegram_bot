from bot import * 
from telebot import types
from math import *
from enums import CalculatorSteps
from handlers.command_handlers import *
from handlers.callback_handlers import *
from model_singleton import model_singleton
from constants import ADMIN_CHAT_ID

@bot.message_handler(content_types=['text'])
def message_handlers(message):
 try:
  model: CalculationModel = model_singleton.get_model_by_id(message.chat.id)
  match model.current_step:
    case CalculatorSteps.level_input:
      # вводит уровень
      if (message.text.isdigit()):
        if (int(message.text) < 35):
          bot.send_message(message.chat.id, f'''В диапазон от 0 до {int(message.text)} не попадает ни одна шахта. Введите корректный уровень''')  
        else:
          # если входные данные нас удовлетворили, то мы сеттим уровень и идем дальше
          model.set_level(int(message.text))
          message_text = f'''Последняя шахта запоняется на уровне *{model.level}*.
Теперь введите количество героев в числовом формате, которыми вы заполняете шахты.

*Пример*: 104 или 76'''
          bot.send_message(message.chat.id, message_text, 'markdown')
          # устанавливаем новый шаг
          model.go_to_step(CalculatorSteps.heroes_input)
      else:
        bot.send_message(message.chat.id, "Введите на каком уровне вы заполняете последнюю шахту")

    case CalculatorSteps.heroes_input:
      # вводит количество героев
      if (message.text.isdigit()):        
        if (int(message.text) < 4):
          bot.send_message(message.chat.id, f'''Количество героев {int(message.text)} не способно заполнить ни одну шахту. Введите корректное значение''')  
        else:
          model.set_heroes(int(message.text))
          message_text = f'''❗️<u>Выберите стратегию расчета:</u>
— <b>Указать количество бутылок</b> и посчитать сколько изумрудов получится
— <b>Указать количество изумрудов</b> и узнать сколько бутылок потребуется, чтобы их набрать'''
          bottles_button = types.InlineKeyboardButton('🍾Указать булытки', callback_data='specify_bottles')
          emeralds_button = types.InlineKeyboardButton('💎Указать изумруды', callback_data='specify_emeralds')
          markup = types.InlineKeyboardMarkup([
            [bottles_button],
            [emeralds_button]
          ])
          model.go_to_step(CalculatorSteps.mode_selection)
          bot.send_message(message.chat.id, message_text, reply_markup=markup, parse_mode='html')
      else:
        bot.send_message(message.chat.id, "Введите количество героев, которыми вы заполняете шахты")
    
    case CalculatorSteps.mode_selection:
      bot.send_message(message.chat.id, "Воспользуйтесь кнопками и выберите стратегию расчета")

    case CalculatorSteps.emeralds_input:
      # вводит количество изумрудов
      if (message.text.isdigit()):
        model.set_emeralds(int(message.text))
        # спросим сколько темных ритуалов за большой круг делает пользователь
        how_much_dark_rit(message)
        model.go_to_step(CalculatorSteps.dr_amount_selection)
      else:
        bot.send_message(message.chat.id, "Введите количество изумрудов, которое вы хотите накопить")
    
    case CalculatorSteps.bottles_input:
      # вводит количество бутылок
      if (message.text.isdigit()):
        model.set_bottles(int(message.text))
        # спросим сколько темных ритуалов за большой круг делает пользователь
        how_much_dark_rit(message)
        model.go_to_step(CalculatorSteps.dr_amount_selection)
      else:
        bot.send_message(message.chat.id, "Введите количество бутылок, которые вы готовы потратить на ТТ")

    case CalculatorSteps.dr_amount_selection:
      bot.send_message(message.chat.id, "Воспользутесь кнопками, чтобы указать сколько ТР вы делаете за большой круг")

    case _:
      bot.send_message(message.chat.id, 'Воспользуйтесь кнопками')
 except Exception as e:
   bot.send_message(ADMIN_CHAT_ID, e)
   print(f"Не удалось отправить сообщение пользователю: {e}")


# спросим сколько темрых ритуалов за большой круг делает пользователь
def how_much_dark_rit(message: types.Message):
  message_text = f'''За сколько темных ритуалов проходите большой круг?'''
  markup = types.InlineKeyboardMarkup()
  one_button = types.InlineKeyboardButton("1️⃣ Один", callback_data='mode_1')
  two_button = types.InlineKeyboardButton("2️⃣ Два", callback_data='mode_2')
  three_button = types.InlineKeyboardButton("3️⃣ Три", callback_data='mode_3')
  markup.add(one_button, two_button, three_button)
  bot.send_message(message.chat.id, message_text, 'markdown', reply_markup=markup)