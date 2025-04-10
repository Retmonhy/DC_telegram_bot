from bot import bot 
from telebot import types

# для меню
# /start - начать расчет заново
# /terms - термины и понятия
# /how_it_works - описание принципа работы бота
# /developer - разработчик

@bot.message_handler(commands=['start'])
def start_message(message):
  markup = types.InlineKeyboardMarkup()
  start_button = types.InlineKeyboardButton("🚀 Начать расчет", callback_data = 'start_calculating')
  markup.add(start_button)
  
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
  message_text = f'''Как работает калькулятор ❓
По введеным пользователем параметрам будет посчитано затрачиваемое количество банок и времени для достижения цели по изумрудам.
Список параметров, необходимых для рассчетов:
1) уровень последней шахты;
2) количество героев;
3) количество ТР на большой круг;
4) желаемое количество изумрудов.

🧮 Алгоритм рассчета:
1) определяем сколько шахт можем заполнить героями
2) заполняем большие шахты
3) оставшимися героями заполняем малые шахты
4) количество изумрудов с малых шахт умножаем на количество ТР за цикл
5) складываем количество изумрудов с больших и малых шахт
6) считаем количество циклов, необходимых для достижения цели по изумрудам(цель_по_изумрудам/кол-во_изумрудов_в_цикл)
7) считаем количество затраченных бутылок (кол-во_циклов * 480). 480 бут. тратится на большой круг
8) считаем затраченное время по кол-ву циклов и кол-ву ТР на большой круг
'''
  bot.send_message(message.chat.id, message_text, parse_mode='html')

@bot.message_handler(commands=['developer'])
def developer_message(message):
  message_text = f'''Разработчик: Кулешов Дмитрий
telegram: [@dev_dimcool](https://t.me/dev_dimcool)
'''
  bot.send_message(message.chat.id, message_text, parse_mode='markdown')

