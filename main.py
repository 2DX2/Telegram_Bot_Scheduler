from telegram import *
from telegram.constants import ParseMode
from telegram.ext import *
import requests
from datetime import *
import json
from warnings import *

filterwarnings(action="ignore", message=r".*CallbackQueryHandler") # убирает предупреждение, для удобства не удалять!

BOT_TOKEN = "8682452278:AAHi7CQC86R06CL3ZtqUVVF2sXfVtil5sEg"

new_task = {"name": None, "description": None, "date": None, "status": None}

markups = {
    "main_menu": InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Мои задачи", callback_data="my_tasks")],
        [InlineKeyboardButton("➕ Добавить задачу", callback_data="add_task")],
        [InlineKeyboardButton("⚙️ Настройки", callback_data="settings")]
    ]),
    "my_tasks": InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Активные", callback_data="active_tasks")],
        [InlineKeyboardButton("✔️ Выполненные", callback_data="completed_tasks")],
        [InlineKeyboardButton("⏰ Просроченные", callback_data="overdue_tasks")],
        [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
    ]),
    "add_task": InlineKeyboardMarkup([
        [InlineKeyboardButton("Отмена", callback_data="cancel_add_task")]
    ]),
    "add_task_name": InlineKeyboardMarkup([
        [InlineKeyboardButton("⏩ Пропустить", callback_data="skip_description_add_task")],
        [InlineKeyboardButton("Отмена", callback_data="cancel_add_task")]
    ])
}

def create_user_data_file(update):
    try:
        file = open(f"users_data/{update.effective_user.id}.json", "r")
        file.close()
    except FileNotFoundError:
        file = open(f"users_data/{update.effective_user.id}.json", "w+")
        json.dump([], file, indent=4, ensure_ascii=False)
        file.close()

async def create_main_menu(update, context):
    create_user_data_file(update)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="""
🏁 Главное меню

Что хотите сделать?
    """, reply_markup=markups["main_menu"])

async def start(update, context):
    create_user_data_file(update)
    await update.message.reply_text("""
👋 Добро пожаловать в Планировщик задач!

Я помогу вам организовать время: создавать задачи, устанавливать дедлайны и получать напоминания.

Чтобы начать, воспользуйтесь меню ниже или введите команду /help для ознакомления со всеми возможностями.
""")
    await create_main_menu(update, context)

async def add_task(update, context):
    global new_task
    new_task = {"name": None, "description": None, "date": None}
    await update.callback_query.edit_message_text("""
➕ Добавление новой задачи

Пожалуйста, введите название задачи (до 100 символов):
""", reply_markup=markups["add_task"])
    return "name_add_task"

async def name_add_task(update, context):
    global new_task
    new_task["name"] = update.message.text
    await update.message.reply_text("""
📝 Введите описание задачи:
""", reply_markup=markups["add_task_name"])
    return "description_add_task"

async def description_add_task(update, context):
    global new_task
    new_task["description"] = update.message.text
    await update.message.reply_text("""
Введите дату и время дедлайна (ДД-ММ-ГГГГ ЧЧ:ММ):
""", reply_markup=markups["add_task"])
    return "date_add_task"

async def skip_description_add_task(update, context):
    global new_task
    new_task["description"] = None
    await context.bot.send_message(chat_id=update.effective_chat.id, text="""
Введите дату и время дедлайна (ДД-ММ-ГГГГ ЧЧ:ММ):
""", reply_markup=markups["add_task"])
    return "date_add_task"



async def date_add_task(update, context):
    try:
        create_user_data_file(update)

        new_task["date"] = datetime.strptime(update.message.text, "%d-%m-%Y %H:%M").strftime("%d-%m-%Y %H:%M")

        if datetime.strptime(new_task["date"], "%d-%m-%Y %H:%M") <= datetime.now():
            new_task["status"] = "overdue"
        else:
            new_task["status"] = "active"
        
        file = open(f"users_data/{update.effective_user.id}.json", "r", encoding="utf-8")
        all_tasks = json.load(file)
        file.close()

        file = open(f"users_data/{update.effective_user.id}.json", "w+", encoding="utf-8")
        json.dump(all_tasks + [new_task], file, indent=4, ensure_ascii=False)
        file.close()

        if new_task["description"] == None:
            await update.message.reply_text(f"""
✅ <b>Задача добавлена!</b>

<b>Название:</b> {new_task["name"]}
<b>Описания нет</b>
<b>Дедлайн:</b> {new_task["date"]}
""", parse_mode=ParseMode.HTML)
        else:
            await update.message.reply_text(f"""
✅ <b>Задача добавлена!</b>

<b>Название:</b> {new_task["name"]}
<b>Описание:</b>
{new_task["description"]}
<b>Дедлайн:</b> {new_task["date"]}
""", parse_mode=ParseMode.HTML)

        await create_main_menu(update, context)
        return ConversationHandler.END

    except:
        await update.message.reply_text("""
❌ Неверный ввод
Верный формат: ДД-ММ-ГГГГ ЧЧ:ММ
Пример: 01-01-2000 12:00
""")
        await update.message.reply_text("""
Введите дату и время дедлайна (ДД-ММ-ГГГГ ЧЧ:ММ):
""", reply_markup=markups["add_task"])

async def cancel_add_task(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="""
😢 Создание задачи отменено!
""")
    await create_main_menu(update, context)
    return ConversationHandler.END

async def main_menu(update, context):
    create_user_data_file(update)
    await update.callback_query.edit_message_text("""
🏁 Главное меню

Что хотите сделать?
""", reply_markup=markups["main_menu"])

async def my_tasks(update, context):
    await update.callback_query.edit_message_text("""
📋 Мои задачи

Выберите тип задач для просмотра:
""", reply_markup=markups["my_tasks"])

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

conv_add_task_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(add_task, pattern="add_task")],
    states={
        "name_add_task": [MessageHandler(filters.TEXT & ~filters.COMMAND, name_add_task)],
        "description_add_task": [
            MessageHandler(filters.TEXT & ~filters.COMMAND, description_add_task),
            CallbackQueryHandler(skip_description_add_task, pattern="skip_description_add_task")
        ],
        "date_add_task": [MessageHandler(filters.TEXT & ~filters.COMMAND, date_add_task)]
    },
    fallbacks=[CallbackQueryHandler(cancel_add_task, pattern="cancel_add_task")]
)

application = Application.builder().token(BOT_TOKEN).build()

application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('help', help))

application.add_handler(conv_add_task_handler)

application.add_handler(CallbackQueryHandler(my_tasks, pattern="my_tasks"))
application.add_handler(CallbackQueryHandler(main_menu, pattern="main_menu"))

application.run_polling()