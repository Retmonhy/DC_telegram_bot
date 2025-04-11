from bot import bot
from math import ceil
from helpers import calculate_emeralds_per_cycle
from classes.CalculationModel import CalculationModel
from enums import CalculatorSteps, DarkRitualsAmount, Strategy
from telebot import types
import prettytable as pt
from classes.ModelStore import ModelStore

@bot.callback_query_handler(func=lambda callback: True)
def callback_handler(callback: types.CallbackQuery):
  # сюда попадаем, когда человек нажимает на кнопку Начать расчет
  if (callback.data == 'start_calculating'):
      # создаем расчетную модель для этого чата
      model = CalculationModel()
      ModelStore.add_model(callback.message.chat.id, model)
      model.go_to_step(CalculatorSteps.last_mine_level)
      message_text = "Введите уровень в числовом формате, на котором вы заполняете последнюю шахту. \n\nПример: 7500 или 12250"
      bot.send_message(callback.message.chat.id, message_text, reply_markup= types.ReplyKeyboardRemove())
  
  model: CalculationModel = ModelStore.get_model_by_id(callback.message.chat.id)
  
  # заполняет в модели мод расчета
  if (callback.data == 'mode_1'):
     model.set_dr_amount(DarkRitualsAmount.One)
     send_parameters_message(callback.message)
  if (callback.data == 'mode_2'):
     model.set_dr_amount(DarkRitualsAmount.Two)
     send_parameters_message(callback.message)
  if (callback.data == 'mode_3'):
     model.set_dr_amount(DarkRitualsAmount.Three)
     send_parameters_message(callback.message)
  
  #  выбираем по какому параметру будет рассчет: бутылки или изумруды
  if (callback.data == 'specify_bottles'):
     model.set_strategy(Strategy.bottles)
     message_text = "Введите количество бутылок, которые вы готовы потратить на ТТ"
     bot.send_message(callback.message.chat.id, message_text)
     model.go_to_step(CalculatorSteps.bottles)
  if (callback.data == 'specify_emeralds'):
     model.set_strategy(Strategy.emeralds)
     message_text = "Введите количество изумрудов, которое хотите накопить"
     bot.send_message(callback.message.chat.id, message_text)
     model.go_to_step(CalculatorSteps.emeralds)

  # показать результаты
  if (callback.data == 'get_result'):
    if (model.level >= 0 and model.heroes and (model.emeralds or model.bottles)):
          calc_result = get_result(model)
          
          average_craft_emeralds_per_bottle = 4.25
          time = get_readable_time((calc_result.get('cycles_amount') * 10 * model.dark_ritual_amount))
          emeralds_from_craft: int = 0 
          
          message_text: str = ''
          if (model.strategy == Strategy.bottles):
             emeralds_from_craft = ceil(model.bottles * average_craft_emeralds_per_bottle)
             message_text = f'''За *{model.bottles} бутылок* вы наберете *{calc_result.get('total_emeralds')} изумрудов*. 
Необходимо пройти *{calc_result.get('cycles_amount')}* больших циклов и затратить минимум *{time} часов*.
За большой цикл вы получаете *{calc_result.get('emeralds_per_cycle')} изумрудов*

**Дополнительная информация:**
За то же самое количество банок с помощью крафтов можно получить *{emeralds_from_craft}* изумрудов.
'''
          if (model.strategy == Strategy.emeralds):
             emeralds_from_craft = ceil(calc_result.get('total_bottles') * average_craft_emeralds_per_bottle)
             message_text = f'''Вы наберете *{model.emeralds} изумрудов* за *{calc_result.get('cycles_amount')}* больших циклов. 
Необходимо затратить *{calc_result.get('total_bottles')} бутылок*
За большой цикл вы получаете *{calc_result.get('emeralds_per_cycle')} изумрудов*
Затратите минимум *{time} часов*

**Дополнительная информация:**
За то же самое количество банок с помощью крафтов можно получить *{emeralds_from_craft}* изумрудов.
'''
          bot.send_message(callback.message.chat.id, message_text, 'markdown')
          
          end_message_text = 'Хотите сделать еще один расчет?'
          end_markup = types.InlineKeyboardMarkup()
          calc_again_button = types.InlineKeyboardButton(text='🚀 Новый расчет', callback_data="start_calculating")
          end_markup.add(calc_again_button)
          bot.send_message(callback.message.chat.id, end_message_text, reply_markup=end_markup)
    else:
      bot.send_message(callback.message.chat.id, 'Невозможно совершить расчет')
  
  # нажатие кнопки Новый расчет
  if (callback.data == 'calc_again'):
     model.reset_model()
     model.go_to_step(CalculatorSteps.start)


# отправляем резюме параметров
def send_parameters_message(message: types.Message):
  model = ModelStore.get_model_by_id(message.chat.id)
  message_text = get_message_with_parameters(model)
  markup = types.InlineKeyboardMarkup()
  calculate_button = types.InlineKeyboardButton("🧮 Показать результат", callback_data='get_result')
  markup.add(calculate_button)
  bot.send_message(message.chat.id, message_text, 'markdown', reply_markup=markup)
  # устанавливаем новый шаг
  model.go_to_step(CalculatorSteps.result)

# резюмируем параметры расчета
def get_message_with_parameters(model: CalculationModel):
  table = pt.PrettyTable(['Параметр', 'Значение'])
  table.align['Параметр'] = 'l'
  table.align['Значение'] = 'r'

  data = [
      ('Уровень', ceil(model.level)),
      ('Герои', ceil(model.heroes)),
  ]

  if (model.strategy == Strategy.bottles):  
   data.append(('Количество бутылок', model.bottles))
  else:
     data.append(('Желаемые изумруды', model.emeralds))

  data.append(('Количество ТР за круг', ceil(model.dark_ritual_amount)))
  for parameter, value in data:
      table.add_row([parameter, f'{value}'])

  return f'```Расчет будет осуществлен по следующим параметрам: \n{table}```'

# делаем рассчет и возвращаем результат 
def get_result(model: CalculationModel) -> dict[str, int]:
   emeralds_per_cycle = calculate_emeralds_per_cycle(model.level, model.heroes, model.dark_ritual_amount)
   cycles_amount: int = 0
   total_bottles: int = 0
   total_emeralds: int = 0
   if (model.strategy == Strategy.bottles):
      cycles_amount = ceil(model.bottles / 480)
      total_emeralds = ceil(emeralds_per_cycle * cycles_amount)
   else:
      if (emeralds_per_cycle > 0):
         cycles_amount = ceil(model.emeralds / emeralds_per_cycle)
      total_bottles = ceil(cycles_amount * 480)

   return {'emeralds_per_cycle': emeralds_per_cycle, 'cycles_amount': cycles_amount, 'total_bottles': total_bottles, 'total_emeralds': total_emeralds}

# превратит минуты в читаемое для пользователя время
def get_readable_time(time: float) -> str:
   hours = time // 60
   minutes = time % 60

   hours_string: str = f'''{hours}'''
   if (hours < 10):
      hours_string = f'''0{hours}'''
   
   minutes_string: str = f'''{minutes}'''
   if (minutes < 10):
      minutes_string = f'''0{minutes}'''

   return f'''{hours_string}:{minutes_string}'''