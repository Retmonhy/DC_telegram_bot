from helpers import calculate_emeralds_per_cycle
import telebot
from telebot import types
from secret_data import secret_data
from steps import CalculatorSteps;

token = secret_data.get('BOT_API_TOKEN')
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  start_calc_button = types.KeyboardButton("🚀 Начать расчет")
  markup.add(start_calc_button)
  bot.send_message(message.chat.id, text="Привет, {0.first_name} 👋\nНу что, начнем расчет?".format(message.from_user), reply_markup=markup)

level = 0
heroes = 0
prev_step = 0
current_step = CalculatorSteps.start
emeralds = 0


@bot.message_handler(content_types=['text'])
def buttons(message):
  global current_step, level, emeralds, heroes

  match current_step:
    case CalculatorSteps.start:
      # сюда попадаем, когда человек нажимает на кнопку Начать расчет
      current_step = CalculatorSteps.last_mine_level
      # отправим смс, чтобы он ввел уровень
      bot.send_message(message.chat.id, text="Введите уровень в числовом формате, на котором вы заполняете последнюю шахту. \nПример: 7500 или 12250")

    case CalculatorSteps.last_mine_level:
      # вводит уровень
      if (isinstance(int(message.text), int)):
        # если входные данные нас удовлетворили, то мы сеттим уровень и идем дальше
        # переключаем шаг 
        current_step = CalculatorSteps.heroes_amount
        level = (int(message.text) // 250) * 250
        message_text = f'''Последняя шахта запоняется на уровне {level}.
        Теперь введите количество героев в числовом формате, которыми вы заполняете шахты.
        Пример: 104 или 76'''
        bot.send_message(message.chat.id, message_text)
      else:
        bot.send_message(message.chat.id, "Пожалуйста, введите на каком уровне вы заполняете последнюю шахту")

    case CalculatorSteps.heroes_amount:
      # вводит количество героев
      if (isinstance(int(message.text), int)):
        current_step = CalculatorSteps.emeralds
        heroes = int(message.text)
        bot.send_message(message.chat.id, "Как много изумрудов вы хотите набрать?")
      else:
        bot.send_message(message.chat.id, "Пожалуйста, введите количество героев, которыми вы заполняете шахты")

    case CalculatorSteps.emeralds:
      # вводит количество изумрудов
      if (isinstance(int(message.text), int)):
        current_step = CalculatorSteps.result
        emeralds = int(message.text)
        message_text = f'''расчет будет осуществлен по следущим параметрам:
        Уровень, на котором забивается последняя шахта: {level}
        Количество героев, которыми забиваются шахты: {heroes}
        Цель: {emeralds} изумрудов'''
        bot.send_message(message.chat.id, message_text)
      else:
        bot.send_message(message.chat.id, "Пожалуйста, введите количество изумрудов, которое вы хотите накопить в виде числа.")

    case CalculatorSteps.result:
      if (level and heroes and emeralds):
        emeralds_per_cycle = calculate_emeralds_per_cycle(level, heroes)
        cycles_amount = (emeralds // emeralds_per_cycle) + 1
        bottles = cycles_amount * 480
        message_text = f'''Вы наберете изумруды за следующее количество циклов: {cycles_amount}. 
        Для этого необходимо затратить {bottles} бутылок
        За полный(большой цикл) вы получаете {emeralds_per_cycle} изумрудов'''
        bot.send_message(message.chat.id, message_text)
      else:
        bot.send_message(message.chat.id, 'Для расчетов чего-то не хватает')




bot.polling(none_stop=True, interval=0)