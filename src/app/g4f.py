from g4f.client import Client
from g4f.Provider import OpenaiChat

tool_calls = [
    {
        "function": {
            "arguments": {
                "query": "Latest advancements in AI",
                "max_results": 1,
                "max_words": 500,
                "backend": "api",
                "add_text": True,
                "timeout": 7
            },
            "name": "search_tool"
        },
        "type": "function"
    }
]

client = Client(
    provider=OpenaiChat,
    # Add any other necessary parameters
    tool_calls=tool_calls
)


def get_g4f_formula(promt):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": promt + "Напиши ТІЛЬКИ ОДНУ формулу текстом!!"
            }],
        # Add any other necessary parameters
    )
    return response.choices[0].message.content


def get_g4f_answer(promt):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": promt + "Напиши текст-відповідь БЕЗ РОЗВ'ЯЗКУ!"
            }],
        # Add any other necessary parameters
    )
    return response.choices[0].message.content


def get_g4f_stucture(promt):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": promt + "Напиши ТЕКСТ Покроково без розвязку задачі!"
            }],
        # Add any other necessary parameters
    )
    return response.choices[0].message.content
