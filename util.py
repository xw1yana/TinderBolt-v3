from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message, BotCommand, MenuButtonCommands, BotCommandScopeChat, MenuButtonDefault
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


def dialog_user_info_to_str(user) -> str:
    result = ""
    map = {"name": "Ім'я", "sex": "Стать", "age": "Вік", "city": "Місто", "occupation": "Професія", "hobby": "Хобі", "goals": "Цілі знайомства",
           "handsome": "Краса, привабливість у балах (максимум 10 балів)", "wealth": "Доход, багатство", "annoys": "У людях дратує"}
    for key, name in map.items():
        if key in user:
            result += name + ": " + user[key] + "\n"
    return result


async def send_text(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> Message:
    if text.count('_') % 2 != 0:
        message = f"Рядок '{text}' є невалідним з погляду markdown. Скористайтеся методом send_html()"
        print(message)
        return await update.message.reply_text(message)
    
    text = text.encode('utf16', errors='surrogatepass').decode('utf16')
    return await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.MARKDOWN)

async def send_html(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> Message:
    text = text.encode('utf16', errors='surrogatepass').decode('utf16')
    return await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)


async def send_text_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, buttons: dict) -> Message:
    text = text.encode('utf16', errors='surrogatepass').decode('utf16')
    keyboard = []
    for key, value in buttons.items():
        button = InlineKeyboardButton(str(value), callback_data=str(key))
        keyboard.append([button])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)


async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE, name: str) -> Message:
    with open('resources/images/' + name + ".jpg", 'rb') as photo:
        return await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, commands: dict):
    command_list = [BotCommand(key, value) for key, value in commands.items()]
    await context.bot.set_my_commands(command_list, scope=BotCommandScopeChat(chat_id=update.effective_chat.id))
    await context.bot.set_chat_menu_button(menu_button=MenuButtonCommands(), chat_id=update.effective_chat.id)

async def hide_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=update.effective_chat.id))
    await context.bot.set_chat_menu_button(menu_button=MenuButtonDefault(), chat_id=update.effective_chat.id)


def load_message(name):
    with open("resources/messages/" + name + ".txt", "r", encoding="utf8") as file:
        return file.read()


def load_prompt(name):
    with open("resources/prompts/" + name + ".txt", "r", encoding="utf8") as file:
        return file.read()


class Dialog:
    pass