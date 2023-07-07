import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from Bot_Folder.kleinanzeigen_scraper import loop_loops

API_KEY = ""

# Create an asyncio queue to handle user requests
user_queue = asyncio.Queue()

async def checker_list():
    list_of_users = {
        "7106802741": ["https://www.kleinanzeigen.de/s-berlin/bmw/k0l3331", "https://www.kleinanzeigen.de/s-berlin/apple/k0l3331", "https://www.kleinanzeigen.de/s-lego/k0"],
        "710680275": ["https://www.kleinanzeigen.de/s-berlin/bmw/k0l3331", "https://www.kleinanzeigen.de/s-berlin/apple/k0l3331", "https://www.kleinanzeigen.de/s-lego/k0"],
        "430680275": ["https://www.kleinanzeigen.de/s-berlin/bmw/k0l3331", "https://www.kleinanzeigen.de/s-berlin/apple/k0l3331", "https://www.kleinanzeigen.de/s-lego/k0"],
        "324450275": ["https://www.kleinanzeigen.de/s-berlin/bmw/k0l3331", "https://www.kleinanzeigen.de/s-berlin/apple/k0l3331", "https://www.kleinanzeigen.de/s-lego/k0"]
    }
    return list_of_users



async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.chat.id)
    await update.message.chat.send_message("Bot is started.")
    await user_queue.put(user_id)  # Put user ID into the queue


async def worker(user_id):
    while True:
        dict_list = await checker_list()
        if user_id in dict_list:
            print("Message")
            await loop_loops(user_id)

        else:
            print("123")
            await asyncio.sleep(1)
        # Add your logic here for processing the user's request




async def process_users():
    while True:
        user_id = await user_queue.get()  # Get user ID from the queue
        asyncio.create_task(worker(user_id))  # Create a worker task for the user
        user_queue.task_done()  # Mark task as done


if __name__ == '__main__':
    print("Bot started")

    # Create and configure the application
    app = Application.builder().token(API_KEY).build()
    app.add_handler(CommandHandler('start', start_command))

    # Start the user processing loop
    loop = asyncio.get_event_loop()
    loop.create_task(process_users())

    # Run the application
    app.run_polling(poll_interval=1)
