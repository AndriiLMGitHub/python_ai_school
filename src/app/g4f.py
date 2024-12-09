from g4f.client import Client


def get_g4f_formula(promt):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": promt + "Напиши тільки!! формулу для розвязку цієї задачі!"
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
                "content": promt + "Напиши тільки відповідь на цю задачу без розвязку!"
            }],
        # Add any other necessary parameters
    )
    return response.choices[0].message.content
