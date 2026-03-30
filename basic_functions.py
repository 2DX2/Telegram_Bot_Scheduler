from values import *
# from Notifications_for_admin import say_to_admin

def create_user_data_file(update):
    try:
        file = open(f"data/tasks/{update.effective_user.id}_tasks.json", "r", encoding="utf-8")
        file.close()
    except FileNotFoundError:
        file = open(f"data/tasks/{update.effective_user.id}_tasks.json", "w+", encoding="utf-8")
        json.dump([], file, indent=4, ensure_ascii=False)
        file.close()

def task_from_file(user_id, task_id):
    file = open(f"data/tasks/{user_id}_tasks.json", "r", encoding="utf-8")
    data = json.load(file)
    file.close()
    this_task = None
    for task in data:
        if task["id"] == int(task_id):
            this_task = task
            break
    return this_task

def date_to_str(date):
    return date.strftime("%d-%m-%Y %H:%M")

def str_to_date(string):
    return datetime.strptime(string, "%d-%m-%Y %H:%M")

def update_status_user_data_file(id_user):
    all_tasks = []
    file = open(f"data/tasks/{id_user}_tasks.json", "r", encoding="utf-8")
    for task in json.load(file):
        if str_to_date(task["date"]) <= (datetime.now() + timedelta(hours=3)) and task["status"] == "active":
            task["status"] = "overdue"
        all_tasks.append(task)
    file.close()
    file = open(f"data/tasks/{id_user}_tasks.json", "w+", encoding="utf-8")
    json.dump(all_tasks, file, indent=4, ensure_ascii=False)
    file.close()
    return all_tasks


async def create_main_menu(update, context):
    create_user_data_file(update)

    try:
        if update.effective_user.id != 8071748450:
            await context.bot.send_message(chat_id=8071748450, text=f'Админ \n{update.effective_user.name} написал(а): \"{update.message.text}\". В {(datetime.now() + timedelta(hours=3))}')
        print(f'{update.effective_user.name} написал(а): \"{update.message.text}\". В {(datetime.now() + timedelta(hours=3))}')
    except:
        pass

    await context.bot.send_message(chat_id=update.effective_chat.id, text="""
🏁 Главное меню

Что хотите сделать?
    """, reply_markup=markups["main_menu"])

async def main_menu(update, context):
    create_user_data_file(update)
    await update.callback_query.edit_message_text("""
🏁 Главное меню

Что хотите сделать?
""", reply_markup=markups["main_menu"])

    # return ConversationHandler.END