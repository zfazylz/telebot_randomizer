# import logging
#
# from aiogram import Bot, Dispatcher, types, executor
#
API_TOKEN = '1068275743:AAFL-pSGvVOJFbiZw64ewaFRp89JKYTfi7E'
adminlist = ['zfazylz', 'CastOnSquirt']
saved_members = []
winner = ''

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    global saved_members, winner

    if update.effective_chat.username in adminlist:
        members = update.message.text.split(',')
        for i in members:
            print(i.split())

        members = [member.lstrip().rstrip() for member in members]
        length = len(members)
        if length > 1:
            saved_members = members
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Список участников спешно импортирован. В списке %d участников' % length
            )
            update.message.reply_text('Для предустановки победителя отправьте имя участника из списка')

        if length == 1:
            if members[0] in saved_members:
                winner = members[0]
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Победитель выбран'
                )
            else:
                update.message.reply_text('Данного имени нет в списке')

    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Вас приветсвует бот рандомайзера, разработчик https://desite.pro')


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


from random import randint


def rand(update, context):
    if update.effective_user.username in adminlist:
        global saved_members, winner
        if len(saved_members) > 1:
            if not winner:
                winner = saved_members[randint(0, len(saved_members) - 1)]
            update.message.reply_text('Победитель %s' % winner)
            update.message.reply_text('Всего участников %d' % len(saved_members))
            update.message.reply_text('Список участников: %s' % str(*saved_members))
            saved_members = []
            winner = ''
        else:
            update.message.reply_text('Не достаточно учасников')
    else:
        update.message.reply_text('У вас не досттаточно прав для проведения розыгрышей')


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(API_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("rand", rand))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
