import logging
import re

from CovidAPI import fetch_data_from_API

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import ConversationHandler, CallbackQueryHandler

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ParseMode

BEGINMSG = "Hi. Welcome to Covid Relief Bot"

MENU, GET_LOCATION = range(2)

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text(
        BEGINMSG,
        reply_markup = ReplyKeyboardMarkup(
            [['Oxygen Cylinder'], ['Oxygen Bed'], ['Medicine'], ['Plasma'], ['Ambulance'], ['Exit']],
            one_time_keyboard=True,
            resize_keyboard=True
        ),
    )
    return MENU

def exit_convo(update, context):
    start(update, context)
    return MENU

def handle_menu(update, context):
    resource = update.message.text
    context.user_data['resource_wanted'] = resource
    update.message.reply_text("Please enter city")
    return GET_LOCATION

def fetch_info(update, context):
    if 'resource_wanted' not in context.user_data:
        return exit_convo(update, context)
    resource = context.user_data['resource_wanted']
    location = update.message.text
    #update.message.reply_text(fetch_data_from_API(resource, location))
    context.bot.send_message(chat_id=update.message.chat_id,
                      text=fetch_data_from_API(resource, location))
    return exit_convo(update, context)

def error(update, context):
    """Log Errors caused by Updates."""
    print(context.error)
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    import json
    with open('config.json') as fp:
        config = json.load(fp)
    updater = Updater(config["API_TOKEN"], use_context=True)
    dp = updater.dispatcher
    
    # Add Handlers
    #dp.add_handler(CommandHandler("start", start))

    login_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [
                MessageHandler(Filters.regex('^(Oxygen Cylinder)$'), handle_menu),
                MessageHandler(Filters.regex('^(Oxygen Bed)$'), handle_menu),
                MessageHandler(Filters.regex('^(Medicine)$'), handle_menu),
                MessageHandler(Filters.regex('^(Plasma)$'), handle_menu),
                MessageHandler(Filters.regex('^(Ambulance)$'), handle_menu)
            ],
            GET_LOCATION: [MessageHandler(Filters.text, fetch_info)],
        },
        fallbacks=[MessageHandler(Filters.regex('.*'), exit_convo)]
    )

    dp.add_handler(login_handler)
    
    # log all errors
    dp.add_error_handler(error)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
