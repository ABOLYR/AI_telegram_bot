from telegram.ext import ContextTypes
import telegram_bot.states as states
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, Update, Message
import open_ai as openai
import random
import constants.messages as messages
import constants.system_messages as system_messages
import constants.keyboards as keyboards

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # Creating variables
    context.user_data['translate_from']: str = ""
    context.user_data['translate_to']: str = ""
    
    # Starting conversation
    # Setting system message to say AI how it should behave
    context.user_data['conversation_with_ai']: list[map] = [
        {
            "role": "system",
            "content": system_messages.start_message
        }
    ]
    
    # Sending request to AI to get greetings to user
    response: str = openai.send_message(context.user_data['conversation_with_ai'])
    
    # Saving AI answer
    context.user_data['conversation_with_ai'].append(
        {
            "role": "assistant",
            "content": response
        }
    )

    # Sending AI greetings to user
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
        reply_markup=ReplyKeyboardMarkup(keyboards.main_keyboard)
        )

    # Setting get user input state
    return states.GET_USER_INPUT

async def start_new_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This function uses when user wants to reset conversation
    
    # Removing all messages except system message and AI greetings
    context.user_data['conversation_with_ai'] = context.user_data['conversation_with_ai'][:2]
    
    # Adding system message to ask AI to create message for user that will explain for him 
    # that he can ask another question.
    context.user_data['conversation_with_ai'].append(
        {
            "role": "system",
            "content": system_messages.new_context_message
        }
    )
    
    # Sending request to AI
    response: str = openai.send_message(context.user_data['conversation_with_ai'])
    
    # Saving AI answer
    context.user_data['conversation_with_ai'].append(
        {
            "role": "assistant",
            "content": response
        }
    )
    
    # Sending AI answer to chat
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
        reply_markup=ReplyKeyboardMarkup(keyboards.main_keyboard)
        )
    
    # Returning get user input state
    return states.GET_USER_INPUT

async def send_user_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This function sending user answer to AI, getting response and sending it back to user
    
    # It needs time for AI to create answer and some user may think that something went wrong,
    # so thats why we are sending wait message to explain that the AI is in the process of thinking
    # We using list of wait messages and can get one message using random function
    wait_message: str = get_random_massage(messages.wait_messages)
    
    # Sending wait message
    message = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=wait_message,
        reply_markup=ReplyKeyboardRemove()
        )
    
    # Adding user input to conversation
    context.user_data['conversation_with_ai'].append(
        {
            "role": "user",
            "content": update.message.text
        }
    )
    
    # Sending user input ot AI
    response = openai.send_message(context.user_data['conversation_with_ai'])

    # Saving AI answer
    context.user_data['conversation_with_ai'].append(
        {
            "role": "assistant",
            "content": response
        }
    )
    
    # Removing wait message
    await message.delete()
    
    # Sending AI answer to user
    await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response,
            reply_markup=ReplyKeyboardMarkup(keyboards.main_keyboard)
            )
    
    # Returning get user input state
    return states.GET_USER_INPUT

def get_random_massage(messages: list[str]) -> str:
    # Just simple random function that gets list of messages and returns one random message from it
    random_number = random.randint(0, len(messages) - 1)
    
    return messages[random_number]