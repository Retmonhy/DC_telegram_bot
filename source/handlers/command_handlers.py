from bot import bot 
from telebot import types
from model_singleton import model_singleton
from telebot import types
from enums import CalculatorSteps

# для меню
# /start - начать расчет заново
# /terms - термины и понятия
# /how_it_works - описание принципа работы бота
# /developer - разработчик

@bot.message_handler(commands=['start'])
def start_message(message: types.Message):
  markup = types.InlineKeyboardMarkup()
  start_button = types.InlineKeyboardButton("🚀 Начать расчет", callback_data = 'start_calculating')
  markup.add(start_button)
  model = model_singleton.get_model_by_id(message.chat.id)
  model.go_to_step(CalculatorSteps.start)
  message_text = f'''Привет, {message.from_user.first_name} 👋\nНу что, начнем расчет?'''
  bot.send_message(message.chat.id, message_text, reply_markup=markup)

@bot.message_handler(commands=['terms'])
def write_terms(message):
  message_text = f'''Термины и понятия
*Темный ритуал(ТР)* - перерождение со сбросом всех героев
*Тайм тревел(ТТ)* - механизм получения изумрудов путём заполнения шахт героями и перемотки времени.
*Шахта* - место, куда отправляются герои для майнинга изумрудов. Для заполнени яодной шахты требуется 4 героя.
*Изумруды* - игровой ресурс, необходимый для открытия новых героев.
*Бутылки* - игровой ресурс, необходимый для выполнения тайм тревела.
*Большой круг* - большой цикл шахт равный 192 часам, за который отработают все 192-часовые шахты.
*Малый круг* - малый цикл шахт равный 64 часам, за который отработают все 60-часовые шахты.
'''
  bot.send_message(message.chat.id, message_text, parse_mode='markdown')

@bot.message_handler(commands=['how_it_works'])
def how_it_works_message(message):
  message_text = f'''❓<b>Как работает калькулятор</b> 
По введеным пользователем параметрам будет посчитано затрачиваемое количество банок иил выхлоп изумрудов, в зависимости от выбранной стратегии рассчета. 

📐<b>Две стратегии рассчета:</b>
— <u>задать количество бутылок</u>, которое пользователь хочет потратить и посчитать сколько изумрудов получится;
— <u>задать желаемое количество</u> изумрудов и посчитать сколько бутылок и времени потребуется для этого. 
Так же в результатах рассчета можно будет увидеть затраты по времени на процесс ТТ.
Уже произведено <b>{model_singleton.total_calculations} расчетов</b>

📋<b>Список параметров, необходимых для рассчетов:</b>
1) уровень последней шахты;
2) количество героев;
3.1) желаемое количество изумрудов или
3.2) затрачиваемые банки
4) количество ТР на большой круг;
'''
  bot.send_message(message.chat.id, message_text, parse_mode='html')

@bot.message_handler(commands=['developer'])
def developer_message(message):
  message_text = f'''👨‍💻Разработчик: Кулешов Дмитрий
telegram: [@dev_dimcool](https://t.me/dev_dimcool)
'''
  bot.send_message(message.chat.id, message_text, parse_mode='markdown')

