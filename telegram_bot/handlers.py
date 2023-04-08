from telegram.ext import (
    filters,
    CommandHandler,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
)
import telegram_bot.dispatches.main_dispatches as main_dispatches
import telegram_bot.dispatches.translator_dispatches as translator_dispatches
import telegram_bot.states as states
import constants.keys as keys

conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', main_dispatches.start)],
        allow_reentry=True,
        states={
            states.GET_USER_INPUT: [
                CommandHandler('reset', main_dispatches.start_new_context),
                MessageHandler(filters.Regex(keys.translate_key.text), translator_dispatches.set_translate_language),
                MessageHandler(filters.TEXT, main_dispatches.send_user_answer),
            ],
            states.TRANSLATE_SET_FROM_STATE: [
                MessageHandler(filters.TEXT, translator_dispatches.set_language_from),
            ],
            states.TRANSLATE_SET_TO_STATE: [
                MessageHandler(filters.TEXT, translator_dispatches.set_language_to),
            ],
            states.TRANSLATE_STATE: [
                MessageHandler(filters.Regex(keys.return_key.text), main_dispatches.start_new_context),
                MessageHandler(filters.Regex(keys.change_languages_key.text), translator_dispatches.change_language),
                MessageHandler(filters.TEXT, translator_dispatches.translate),
            ],
            states.INIT_STATE: [
                CommandHandler('start', main_dispatches.start),
            ],
        },
        fallbacks=[CommandHandler('start', main_dispatches.start)],
    )