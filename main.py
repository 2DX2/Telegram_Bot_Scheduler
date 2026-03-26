from libraries import *

from basic_functions import *
from start_and_help import *
from add_task import *
from my_tasks import *
from add_job import *

def main():
    filterwarnings(action="ignore", message=r".*CallbackQueryHandler") # убирает предупреждение

    os.makedirs("users_data/tasks", exist_ok=True)



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


    conv_my_tasks_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(my_tasks, pattern="my_tasks")],
        states={"choice_type_my_tasks": [CallbackQueryHandler(beck_main_menu_my_tasks, pattern="beck_main_menu_my_tasks"), CallbackQueryHandler(choice_type_my_tasks)],
                "choice_task_my_tasks": [CallbackQueryHandler(choice_task_my_tasks)]
                },
        fallbacks=[CallbackQueryHandler(beck_main_menu_my_tasks, pattern="beck_main_menu_my_tasks")]
    )


    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))

    application.add_handler(conv_add_task_handler)
    application.add_handler(conv_my_tasks_handler)

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, create_main_menu))

    application.add_handler(CallbackQueryHandler(main_menu, pattern="main_menu"))

    application.run_polling()

if __name__ == "__main__":
    main()