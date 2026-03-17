from telegram import *
from telegram.constants import ParseMode
from telegram.ext import *
import requests
from datetime import *

BOT_TOKEN = "8682452278:AAHi7CQC86R06CL3ZtqUVVF2sXfVtil5sEg"

async def start(update, context):
    await update.message.reply_text("""
👋 Добро пожаловать в Планировщик задач!

Я помогу вам организовать время: создавать задачи, устанавливать дедлайны и получать напоминания.

Чтобы начать, воспользуйтесь меню ниже или введите команду /help для ознакомления со всеми возможностями.

Что хотите сделать?

""")

async def help(update, context):
    await update.message.reply_text("""
📖 Справка по использованию Планировщика задач

Я умею:
• создавать новые задачи с дедлайнами;
• показывать списки задач (активные, выполненные, просроченные);
• редактировать и удалять задачи;
• напоминать о приближении сроков (за 1 час и 15 минут);
• уведомлять о просроченных задачах.

📋 Основные команды:
/start — перезапустить бота
/help — показать эту справку

🔧 Доступные действия через меню:
• «Мои задачи» — просмотреть все задачи
• «Добавить задачу» — создать новую задачу
• «Настройки» — настроить уведомления и часовой пояс

Просто нажмите на нужную кнопку в меню или введите команду!
""")

application = Application.builder().token(BOT_TOKEN).build()

application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('help', help))

application.run_polling()