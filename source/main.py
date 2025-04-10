from bot import * 
from handlers.command_handlers import *
from handlers.callback_handlers import *
from handlers.message_handlers import *

bot.infinity_polling(timeout=10, long_polling_timeout = 5)