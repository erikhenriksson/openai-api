import json
import openai
import re

model = "gpt-3.5-turbo-0613"
openai.api_key = "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"
input_file_path = "input_texts.txt"
output_file_path = "output_responses.json"


with open("system_prompt.txt", "r") as f:
    system_prompt = f.read().replace("\n", " ")

system_message = [
    {
        "role": "system",
        "content": system_prompt,
    }
]


def get_response(input_text):
    prompt = f"Respond in the json format: {{'response': classification}}\nText: {input_text}\nQuestion or answer (question, answer):"
    response = openai.ChatCompletion.create(
        model=model,
        messages=system_message + [{"role": "user", "content": prompt}],
        max_tokens=40,
        n=1,
        stop=None,
        temperature=0.5,
    )
    response_text = response.choices[0].message["content"].strip()

    # Add input_text back in for the result
    return {"text": input_text, "response": response_text.lower()}


with open(input_file_path, "r") as input_file, open(
    output_file_path, "w"
) as output_file:
    examples = []
    for line in input_file:
        text = line.strip()
        if text:
            examples.append(get_response(text))
    output_file.write(json.dumps(examples, ensure_ascii=False))

    exit()
