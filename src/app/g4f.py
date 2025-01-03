from g4f.client import Client


def get_g4f_formula(promt):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": promt + "Напиши ТІЛЬКИ ОДНУ формулу для розвязку цієї задачі!"
            }],
        # Add any other necessary parameters
    )
    return response.choices[0].message.content


def get_g4f_answer(promt):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": promt + "Напиши тільки відповідь на цю задачу БЕЗ РОЗВ'ЯЗКУ!"
            }],
        # Add any other necessary parameters
    )
    return response.choices[0].message.content


def get_g4f_stucture(promt):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": promt + "Напиши ТЕКСТ ПРО СТРУКТУРУ для розвязку цієї задачі! ТІЛЬКИ ТЕКСТ!!!"
            }],
        # Add any other necessary parameters
    )
    return response.choices[0].message.content
