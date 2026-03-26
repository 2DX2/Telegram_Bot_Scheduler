from add_job import *

async def my_tasks(update, context):
    create_user_data_file(update)
    await update.callback_query.edit_message_text("""
📋 Мои задачи

Выберите тип задач для просмотра:
""", reply_markup=markups["my_tasks"])
    return "choice_type_my_tasks"

async def choice_type_my_tasks(update, context):
    keyboards = []

    update_status_user_data_file(update.effective_user.id)
    file = open(f"users_data/tasks/{update.effective_user.id}_tasks.json", "r", encoding="utf-8")

    query = update.callback_query
    await query.answer()

    for task in json.load(file):
        if task["status"] == query.data:
            keyboards.append([InlineKeyboardButton(task["name"], callback_data=task["id"])])

    keyboards.append([InlineKeyboardButton("🔙 Назад", callback_data="beck_main_menu_my_tasks")])

    markup = InlineKeyboardMarkup(keyboards)

    if query.data == "active":
        word = "✅ Ваши активные"
    elif query.data == "complete":
        word = "✔️ Ваши выполненные"
    elif query.data == "overdue":
        word = "⏰ Ваши просроченные"


    if len(keyboards) == 1:
        await update.callback_query.edit_message_text(f"""
🔎 У вас нет задач этого вида
""", reply_markup=markup)
    else:
        await update.callback_query.edit_message_text(f"""
{word} задачи:
""", reply_markup=markup)

    return "choice_task_my_tasks"

async def choice_task_my_tasks(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "beck_main_menu_my_tasks":
        await main_menu(update, context)
        return ConversationHandler.END
    elif query.data.split("|", 1)[0] == "reminder_off":
        if task_from_file(update.effective_user.id, int(query.data.split("|", 1)[1]))["notification"]:
            jobs = context.job_queue.get_jobs_by_name(f"{update.effective_user.id}.{query.data.split("|", 1)[1]}")

            if not jobs:
                pass
            else:
                for job in jobs:
                    job.schedule_removal()

            await update.callback_query.edit_message_text(f"""
    🔇 Уведомления отключены!
    """, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="beck_main_menu_my_tasks")]]))

            file = open(f"users_data/tasks/{update.effective_user.id}_tasks.json", "r", encoding="utf-8")
            tasks = json.load(file)
            file.close()
            for i in range(len(tasks)):
                if tasks[i]["id"] == int(query.data.split("|", 1)[1]):
                    task = tasks[i]
                    number_task = i
                    break

            file = open(f"users_data/tasks/{update.effective_user.id}_tasks.json", "w", encoding="utf-8")
            tasks[number_task]["notification"] = False
            json.dump(tasks, file, indent=4, ensure_ascii=False)
        else:
            await set_reminder_tasks(
                context=context,
                update=update,
                task_id=query.data.split("|", 1)[1],
                delta_times=[
                    timedelta(
                        minutes=15,
                    ),
                    timedelta(
                        hours=1,
                    )
                ]
            )

            file = open(f"users_data/tasks/{update.effective_user.id}_tasks.json", "r", encoding="utf-8")
            tasks = json.load(file)
            file.close()
            for i in range(len(tasks)):
                if tasks[i]["id"] == int(query.data.split("|", 1)[1]):
                    task = tasks[i]
                    number_task = i
                    break


            file = open(f"users_data/tasks/{update.effective_user.id}_tasks.json", "w", encoding="utf-8")
            tasks[number_task]["notification"] = True
            json.dump(tasks, file, indent=4, ensure_ascii=False)

            await update.callback_query.edit_message_text(f"""
🔊 Уведомления включены!
""", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="beck_main_menu_my_tasks")]]))

    elif query.data.split("|", 1)[0] == "delete_task":
        file = open(f"users_data/tasks/{update.effective_user.id}_tasks.json", "r", encoding="utf-8")
        tasks = json.load(file)
        file.close()
        for i in range(len(tasks)):
            if tasks[i]["id"] == int(query.data.split("|", 1)[1]):
                task = tasks[i]
                number_task = i
                break

        del tasks[number_task]

        file = open(f"users_data/tasks/{update.effective_user.id}_tasks.json", "w", encoding="utf-8")
        json.dump(tasks, file, indent=4, ensure_ascii=False)
        file.close()

        if task["description"] is None:
            await update.callback_query.edit_message_text(f"""
<b>❌ Задача удалена!</b>

🏷️ <b>Название:</b> {task["name"]}
📝 <b>Описания нет</b>
⏰ <b>Дедлайн:</b> {task["date"]}
""", parse_mode=ParseMode.HTML, reply_markup=markups["back_main_menu_my_tasks"])
        else:
            await update.callback_query.edit_message_text(f"""
<b>❌ Задача удалена!</b>

🏷️ <b>Название:</b> {task["name"]}
📝 <b>Описание:</b>
{task["description"]}
⏰ <b>Дедлайн:</b> {task["date"]}
""", parse_mode=ParseMode.HTML, reply_markup=markups["back_main_menu_my_tasks"])
    elif query.data.split("|", 1)[0] == "complete_task":
        file = open(f"users_data/tasks/{update.effective_user.id}_tasks.json", "r", encoding="utf-8")
        tasks = json.load(file)
        file.close()
        for i in range(len(tasks)):
            if tasks[i]["id"] == int(query.data.split("|", 1)[1]):
                task = tasks[i]
                number_task = i
                break

        tasks[number_task]["status"] = "complete"

        file = open(f"users_data/tasks/{update.effective_user.id}_tasks.json", "w", encoding="utf-8")
        json.dump(tasks, file, indent=4, ensure_ascii=False)
        file.close()

        if task["description"] is None:
            await update.callback_query.edit_message_text(f"""
<b>✔️ Задача выполнена!</b>

🏷️ <b>Название:</b> {task["name"]}
📝 <b>Описания нет</b>
⏰ <b>Дедлайн:</b> {task["date"]}
""", parse_mode=ParseMode.HTML, reply_markup=markups["beck_main_menu_my_tasks"])
        else:
            await update.callback_query.edit_message_text(f"""
<b>✔️ Задача выполнена!</b>

🏷️ <b>Название:</b> {task["name"]}
📝 <b>Описание:</b>
{task["description"]}
⏰ <b>Дедлайн:</b> {task["date"]}
""", parse_mode=ParseMode.HTML, reply_markup=markups["back_main_menu_my_tasks"])

    else:
        file = open(f"users_data/tasks/{update.effective_user.id}_tasks.json", "r", encoding="utf-8")
        tasks = json.load(file)
        file.close()
        for i in tasks:
            if i["id"] == int(query.data):
                task = i
                break

        if task["status"] == "active":
            word = "✅ Ваша активная задача"
        elif task["status"] == "complete":
            word = "✔️ Ваша выполненная задача"
        elif task["status"] == "overdue":
            word = "⏰ Ваша просроченная задача"

        if task_from_file(update.effective_user.id, int(task["id"]))["notification"]:
            reminder_name = "🔇 Отключить уведомления"
        else:
            reminder_name = "🔊 Включить уведомления"


        if task["status"] == "complete":
            markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Удалить задачу", callback_data=f"delete_task|{task['id']}")],
                [InlineKeyboardButton(reminder_name, callback_data=f"reminder_off|{task['id']}")],
                [InlineKeyboardButton("🔙 Назад", callback_data="beck_main_menu_my_tasks")]
            ])
        else:
            markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("✔️ Отметить выполненной", callback_data=f"complete_task|{task['id']}")],
                [InlineKeyboardButton("❌ Удалить задачу", callback_data=f"delete_task|{task['id']}")],
                [InlineKeyboardButton(reminder_name, callback_data=f"reminder_off|{task['id']}")],
                [InlineKeyboardButton("🔙 Назад", callback_data="beck_main_menu_my_tasks")]
            ])

        if task["description"] is None:
            await update.callback_query.edit_message_text(f"""
<b>{word}</b>

🏷️ <b>Название:</b> {task["name"]}
📝 <b>Описания нет</b>
⏰ <b>Дедлайн:</b> {task["date"]}
""", parse_mode=ParseMode.HTML, reply_markup=markup)
        else:
            await update.callback_query.edit_message_text(f"""
<b>{word}</b>

🏷️ <b>Название:</b> {task["name"]}
📝 <b>Описание:</b>
{task["description"]}
⏰ <b>Дедлайн:</b> {task["date"]}
""", parse_mode=ParseMode.HTML, reply_markup=markup)

async def beck_main_menu_my_tasks(update, context):
    await main_menu(update, context)
    return ConversationHandler.END