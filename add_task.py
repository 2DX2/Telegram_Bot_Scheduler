
from add_job import *


async def add_task(update, context):
    global new_task
    new_task = {"id": None, "name": None, "description": None, "date": None, "status": None}
    await update.callback_query.edit_message_text("""
➕ Добавление новой задачи

Шаг 1/3:
Пожалуйста, введите название задачи:
""", reply_markup=markups["add_task"])
    return "name_add_task"


async def name_add_task(update, context):
    global new_task
    new_task["name"] = update.message.text
    await update.message.reply_text("""
Шаг 2/3:
📝 Введите описание задачи:
""", reply_markup=markups["add_task_name"])
    return "description_add_task"


async def description_add_task(update, context):
    global new_task
    new_task["description"] = update.message.text
    await update.message.reply_text("""
Шаг 3/3:
⏰ Введите дату и время дедлайна (ДД-ММ-ГГГГ ЧЧ:ММ):
""", reply_markup=markups["add_task"])
    return "date_add_task"


async def skip_description_add_task(update, context):
    global new_task
    new_task["description"] = None
    await context.bot.send_message(chat_id=update.effective_chat.id, text="""
Шаг 3/3:
⏰ Введите дату и время дедлайна (ДД-ММ-ГГГГ ЧЧ:ММ):
""", reply_markup=markups["add_task"])
    return "date_add_task"


async def date_add_task(update, context):
    try:
        create_user_data_file(update)

        new_task["date"] = date_to_str(str_to_date(update.message.text))

        if str_to_date(new_task["date"]) <= datetime.now():
            new_task["status"] = "overdue"
        else:
            new_task["status"] = "active"

        file = open(f"users_data/tasks/{update.effective_user.id}_tasks.json", "r", encoding="utf-8")
        all_tasks = json.load(file)
        file.close()

        all_ids = [i["id"] for i in all_tasks]

        for i in range((max(all_ids) if all_ids != [] else 0) + 2):
            if i not in all_ids:
                new_task["id"] = i
                break

        new_task["notification"] = True

        file = open(f"users_data/tasks/{update.effective_user.id}_tasks.json", "w+", encoding="utf-8")
        json.dump(all_tasks + [new_task], file, indent=4, ensure_ascii=False)
        file.close()

        if new_task["description"] is None:
            await update.message.reply_text(f"""
✅ <b>Задача добавлена!</b>

🏷️ <b>Название:</b> {new_task["name"]}
📝 <b>Описания нет</b>
⏰ <b>Дедлайн:</b> {new_task["date"]}

У задания есть напоминания за 1 час и за 15 минут(их можно отключить в настройках или а списке задач).
""", parse_mode=ParseMode.HTML)
        else:
            await update.message.reply_text(f"""
✅ <b>Задача добавлена!</b>

🏷️ <b>Название:</b> {new_task["name"]}
📝 <b>Описание:</b>
{new_task["description"]}
⏰ <b>Дедлайн:</b> {new_task["date"]}

У задания есть напоминания за 1 час и за 15 минут(их можно отключить в настройках или а списке задач).
""", parse_mode=ParseMode.HTML)

        await set_reminder_tasks(
            context=context,
            update=update,
            task_id=new_task["id"],
            delta_times=[
                timedelta(
                    minutes=15,
                ),
                timedelta(
                    hours=1,
                )
            ]
        )

        await create_main_menu(update, context)
        if update.effective_user.id != 8071748450:
            await context.bot.send_message(chat_id=8071748450, text=f'Админ \n@{update.effective_user.username} создал(а) задание с: Именем: \"{new_task["name"]}\" , Описанием: \"{new_task["description"]}\", Дедлайном: \"{new_task["date"]}\"')
        print(f'@{update.effective_user.username} создал(а) задание с: Именем: \"{new_task["name"]}\" , Описанием: \"{new_task["description"]}\", Дедлайном: \"{new_task["date"]}\"')
        return ConversationHandler.END

    except:
        await update.message.reply_text(f"""
❌ Неверный ввод
Верный формат: ДД-ММ-ГГГГ ЧЧ:ММ
Пример: {date_to_str(datetime.now())}
""")
        await update.message.reply_text("""
⏰ Введите дату и время дедлайна (ДД-ММ-ГГГГ ЧЧ:ММ):
""", reply_markup=markups["add_task"])


async def cancel_add_task(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="""
😢 Создание задачи отменено!
""")
    try:
        if update.effective_user.id != 8071748450:
            await context.bot.send_message(chat_id=8071748450, text=f'Админ \n@{update.effective_user.username} отменил(а) задание с: Именем: \"{new_task["name"]}\", Описанием: \"{new_task["description"]}\"')
        print(f'@{update.effective_user.username} отменил(а) задание с: Именем: \"{new_task["name"]}\" , Описанием: \"{new_task["description"]}\"')
    except:
        pass
    await create_main_menu(update, context)
    return ConversationHandler.END