from libraries import *

BOT_TOKEN = "8682452278:AAHi7CQC86R06CL3ZtqUVVF2sXfVtil5sEg"

markups = {
    "main_menu": InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Мои задачи", callback_data="my_tasks")],
        [InlineKeyboardButton("➕ Добавить задачу", callback_data="add_task")],
        [InlineKeyboardButton("⚙️ Настройки", callback_data="settings")]
    ]),
    "my_tasks": InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Активные", callback_data="active")],
        [InlineKeyboardButton("⏰ Просроченные", callback_data="overdue")],
        [InlineKeyboardButton("✔️ Выполненные", callback_data="complete")],
        [InlineKeyboardButton("🔙 Назад", callback_data="beck_main_menu_my_tasks")]
    ]),
    "add_task": InlineKeyboardMarkup([
        [InlineKeyboardButton("Отмена", callback_data="cancel_add_task")]
    ]),
    "add_task_name": InlineKeyboardMarkup([
        [InlineKeyboardButton("⏩ Пропустить", callback_data="skip_description_add_task")],
        [InlineKeyboardButton("Отмена", callback_data="cancel_add_task")]
    ]),
    "task_info": InlineKeyboardMarkup([
        [InlineKeyboardButton("✔️ Отметить выполненной", callback_data="delete_task")],
        [InlineKeyboardButton("❌ Удалить задачу", callback_data="delete_task")],
        [InlineKeyboardButton("🔙 Назад", callback_data="beck_main_menu_my_tasks")]
    ]),
    "back_main_menu_my_tasks": InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Назад", callback_data="beck_main_menu_my_tasks")]
    ]),
}