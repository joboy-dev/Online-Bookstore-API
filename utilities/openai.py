from openai import OpenAI

from utilities import files


def generate_answer(prompt: str):
    '''Function to get answers to a prompt from openai API'''
    
    openai = OpenAI(api_key=files.get_env_value('OPENAI_API_KEY'))
    response = openai.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt
            },
        ]
    )
    content = response.choices[0].message.content
    
    # response = openai.completions.create(
    #     model='gpt-3.5-turbo-16k',
    #     prompt=prompt,
    # )
    # content = response.choices[0].text
    
    return content