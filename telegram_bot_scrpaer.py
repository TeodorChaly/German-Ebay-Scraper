from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
API_KEY = ""

def exapmple_function():
    list_of_users = {
        "710680271": ["link1", "link2", "link3"],
        "710680275": ["link1", "link2", "link3"],
        "430680275": ["link1", "link2", "link3"],
        "324450275": ["link1", "link2", "link3"],
    }
    return list_of_users

async def start_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    text, dict_of_user_links = checker_function(update.message.chat)
    await update.message.reply_text(
            text
            # Checking function
    )

def checker_function(user_id):
    id = user_id["id"]
    first_name = user_id["first_name"]
    last_name = user_id["last_name"]
    try:
        list_of_users = exapmple_function()
        for vip_user in list_of_users:
            if str(vip_user) == str(id):
                dict_of_user_links = {str(vip_user): list_of_users[str(vip_user)]}
                print("User is in DB!")
                return f"Welcome back, {first_name} {last_name}!",dict_of_user_links

        print("User is not in DB!")
        return f"Sorry, {first_name}. You are not in the list:(\nIf you want to run bot go to https://www.kleinanzeigen.de/", 0
    except:
        print(id, first_name, last_name)
        return f"Sorry, there was an error :/", 0


async def handle_message(update:Update, context:ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f"User {update.message.chat.id} in {message_type}: {text}")


if __name__ == '__main__':
    print("Bot started")
    app = Application.builder().token(API_KEY).build()
    app.add_handler(CommandHandler('start', start_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.run_polling(poll_interval=1)
