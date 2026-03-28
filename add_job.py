from basic_functions import *
from add_job import *


async def send_reminder(context):
    task = task_from_file(context.job.data["user_id"], context.job.data["task_id"])
    if task["status"] != "complete":
        if context.job.data["status"] == "active":
            if context.job.data["time"].total_seconds() == 0:
                await context.bot.send_message(chat_id=context.job.chat_id, text=f'''
<b>⏰ Дедлайн на задачу \"{task["name"]}\" вышел!</b>

С этого момента она считается просроченной.
Вы можете отметить её выполненной или удалить, иначе вы будете получать уведомления о просроченном задании.
''', parse_mode=ParseMode.HTML)
            else:
                await context.bot.send_message(chat_id=context.job.chat_id, text=f'''
<b>⏰ До дедлайна осталось {context.job.data["time"].days} дней, {context.job.data["time"].seconds // 3600} час(ов), {context.job.data["time"].seconds // 60 % 60} минут(ы)!</b>

Если задача уже выполнена, её можно отметить выполненной.
''', parse_mode=ParseMode.HTML)
        elif context.job.data["status"] == "overdue":
            await context.bot.send_message(chat_id=context.job.chat_id, text=f'Это просроченное задание {task["name"]}')


async def set_reminder_tasks(context, update, task_id, delta_times):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    time = str_to_date(task_from_file(user_id, task_id)["date"])
    now_time = datetime.now()

    if task_from_file(user_id, task_id)["status"] == "complete":
        return 0


    for i in range(len(delta_times)):
        when_time = int(((time - delta_times[i]) - now_time).total_seconds())

        if when_time >= 0:
            context.job_queue.run_once(
                callback=send_reminder,
                name=f"{user_id}.{task_id}.{i}",
                chat_id=chat_id,
                when=when_time,
                data={
                    "task_id": task_id,
                    "user_id": user_id,
                    "time": delta_times[i],
                    "status": "active",
                },
        )