import openai
import config

# You need to create config.py file in root directory and provide api key there
openai.api_key = config.OPEN_AI_API_KEY

def send_message(messages: list[map]) -> str:
    count_of_tries = 0
    response = None

    while response == None and count_of_tries < 5:
        print('Fetching AI answer. count of tries: ' + str(count_of_tries))
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        count_of_tries += 1

    if response == None:
        response = 'Error, could`t fetch data from AI'
        
    return response.choices[0].message.content