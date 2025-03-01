import json

last_data=0
limit=200

FILE_PATH="files/khamenei-qa.jsonl"
OUTPUT_PATH="files/openai-tuning/khamenei-qa.jsonl"

APPENDS=[
    "طبق نظر ایت الله خامنه ای",
    # "بر اساس فتوای خامنه ای",
    # "بر اساس نظر علی خامنه ای",
]

template={
    "messages": [
        {
            "role": "system",
            "content": "اسلام یار یک ربات پاسخگویی به سوالات شرعی مسلمانان است."
        },
        {
            "role": "user",
            "content": ""
        },
        {
            "role": "assistant",
            "content": ""
        }
    ]
}

with open(FILE_PATH, 'r') as json_file:
    json_list = list(json_file)

count = 0
with open(OUTPUT_PATH, 'w', encoding='utf8') as output_file:
    for json_str in json_list[last_data:]:
        result = json.loads(json_str)
        for addon in APPENDS:
            c = dict(template)
            c['messages'][1]['content'] = addon + " " + result['question']
            c['messages'][2]['content'] = addon + " " + result['answer']
            json.dump(c, output_file, ensure_ascii=False)
            output_file.write('\n')
            count += 1
        # if count >= limit:
        #     break

