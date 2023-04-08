from telegram.ext import ContextTypes
import telegram_bot.states as states
from telegram import ReplyKeyboardMarkup, Update
import open_ai as openai
import constants.messages as messages
import constants.system_messages as system_messages
import constants.keyboards as keyboards


async def set_translate_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Checking if translate from language is set 
    if context.user_data['translate_from'] == "":
        # If not then we asking to set it up and changing state to get language
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=messages.select_language_from_message,
            reply_markup=ReplyKeyboardMarkup(keyboards.language_keyboard)
            )
        return states.TRANSLATE_SET_FROM_STATE
    
    # Checking if translate to language is set 
    if context.user_data['translate_to'] == "":
        # If not then we asking to set it up and changing state to get language
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=messages.select_language_to_message.format(language_from = context.user_data['translate_from']),
                reply_markup=ReplyKeyboardMarkup(keyboards.language_keyboard)
                )
        return states.TRANSLATE_SET_TO_STATE
    
    # Starting translation if both languages were already set up
    return await start_translate(update=update, context=context)
    
async def set_language_from(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Setting "from" language to variable and asking about language "to"
    context.user_data['translate_from'] = update.message.text
    await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=messages.select_language_to_message.format(from_language = context.user_data['translate_from']),
                reply_markup=ReplyKeyboardMarkup(keyboards.language_keyboard)
                )
    return states.TRANSLATE_SET_TO_STATE
    
async def set_language_to(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Setting "to" language to variable and starting translation
    context.user_data['translate_to'] = update.message.text
    return await start_translate(update=update, context=context)

async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Removing selected languages
    context.user_data['translate_from']: str = ""
    context.user_data['translate_to']: str = ""
    # Setting up languages
    return await set_translate_language(update=update, context=context)
    
async def start_translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Setting system message which contains instruction for AI to be a translator,
    # from and to which language it should translate
    context.user_data['conversation_with_ai']: list[map] = [
        {
            "role": "system",
            "content": system_messages.translate_message.format(language_from=context.user_data['translate_from'], language_to=context.user_data['translate_to'])
        }
    ]
    
    # Sending request to get greetings to user
    response: str = openai.send_message(context.user_data['conversation_with_ai'])
    
    # Saving AI answer
    context.user_data['conversation_with_ai'].append(
        {
            "role": "assistant",
            "content": response
        }
    )
    
    # Sending message with greetings to chat
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
        reply_markup=ReplyKeyboardMarkup(keyboards.translator_keyboard)
        )
    
    # Setting translate state
    return states.TRANSLATE_STATE

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Main translate function
    # Saving user message
    context.user_data['conversation_with_ai'].append(
        {
            "role": "user",
            "content": update.message.text
        }
    )
    
    # Sending request to AI
    response: str = openai.send_message(context.user_data['conversation_with_ai'])
    
    # Saving AI response
    context.user_data['conversation_with_ai'].append(
        {
            "role": "assistant",
            "content": response
        }
    )
    
    # Sending AI response to chat
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
        reply_markup=ReplyKeyboardMarkup(keyboards.translator_keyboard)
        )

    # Returning translate state
    return states.TRANSLATE_STATE