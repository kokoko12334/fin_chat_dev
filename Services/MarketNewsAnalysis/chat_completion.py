import openai

def make_chat_completion(system_prompt, data_prompt):
    model = "gpt-4-1106-preview"
    # model="gpt-3.5-turbo-16k-0613"

    # res = openai_client.chat.completions.create(
    res = openai.ChatCompletion.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            # {"role": "user", "content": "write a report about the stock by given data"},
            # {"role": "assistant", "content": "write report"},
            {"role": "user", "content": data_prompt}
        ]
    )
    
    new_report = res.choices[0].message.content
    print(res.usage)
    return new_report