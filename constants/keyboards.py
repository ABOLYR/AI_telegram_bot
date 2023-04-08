import constants.keys as keys
from telegram import KeyboardButton

main_keyboard: list[list[KeyboardButton]] = [[keys.translate_key]]
language_keyboard: list[list[KeyboardButton]] = [[keys.english, keys.russian], [keys.serbian]]
translator_keyboard: list[list[KeyboardButton]] = [[keys.change_languages_key], [keys.return_key]]