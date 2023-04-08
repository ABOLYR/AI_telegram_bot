class ConversationHandlerState:
    def __init__(self, caller_button_text, theme):
        self.caller_button_text = caller_button_text
        self.theme = theme

    def changeButton(self, caller_button_text):
        self.caller_button_text = caller_button_text
        return self

    def changeTheme(self, theme):
        self.theme = theme
        return self

    def changeButtonAndTheme(self, caller_button_text, theme):
        self.caller_button_text = caller_button_text
        self.theme = theme
        return self

# General

INIT_STATE = ConversationHandlerState(caller_button_text=[], theme='Init'),


# New states

GET_USER_INPUT = ConversationHandlerState(caller_button_text=[], theme='Get user input')
TRANSLATE_SET_FROM_STATE = ConversationHandlerState(caller_button_text=[], theme='Translate set from')
TRANSLATE_SET_TO_STATE = ConversationHandlerState(caller_button_text=[], theme='Translate set to')
TRANSLATE_STATE = ConversationHandlerState(caller_button_text=[], theme='Translate')