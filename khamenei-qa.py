import requests
import json

url = "https://formx.khamenei.link/treatise/action/get-data"

payload = {
    "action": "get-ajvabeh",
    "category": "VkZST2IyTnRTbGxVYTFKWVVqRndZVlJ0Y0ZkVk1EQjZVbXQ0VkdKSGFHaFpla3B1VGxad05rMUVhejA9",
    "reference": None
}

payload2 = {
    "action": "get-ajvabeh",
    "category": "VkZST2IyTnRTbGxVYTFKWVVqRndZVlJ0Y0ZkVk1EQjZVbXQ0VkdKSGFHaFpla3B1VGxad05rMUVhejA9",
    "reference": None
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Referer": "https://formx.khamenei.link/",
    "Origin": "https://formx.khamenei.link",
    "Accept": "*/*"
}

from bs4 import BeautifulSoup
from itertools import zip_longest
import html


def extract_questions_answers(html_text):
    if not html_text:
        return []

    decoded_html = html.unescape(html_text)
    soup = BeautifulSoup(decoded_html, "html5lib")

    elements = soup.find_all(class_=["matn", "answer"])

    texts = [elem.get_text(strip=True) for elem in elements if elem.get_text(strip=True)]

    qs, ans = texts[::2], texts[1::2]  # Odd-indexed for questions, even-indexed for answers

    print(len(qs), len(ans))

    # Pair them together, ensuring all questions have answers
    qa_pairs = [{"question": q, "answer": a} for q, a in zip_longest(qs, ans, fillvalue="No answer provided")]

    return qa_pairs


# Note: parentTitle could be None, then title will be the prime
def formatContent(parentTitle, title, question, answer):
    q = f"- رساله خامنه ای {parentTitle + '/' if parentTitle is not None else ''}{title} - {question}"
    return {'question': q, answer: 'answer'}


session = requests.Session()
response = session.post(url, data=payload, headers=headers)

print(f"Status Code: {response.status_code}")

categories = response.json()

questions = []
count = 0

for cat in categories:
    ajax = cat['ajax']
    catId = cat['catid']
    content = cat['content']
    id = cat['id']
    parent = cat['parent']
    title = cat['title']

    if ajax:
        payload2.update({"reference": id})
        response2 = session.post(url, data=payload2, headers=headers)

        items = response2.json()

        for item in items:
            ajax2 = item['ajax']
            catId2 = item['catid']
            content2 = item['content']
            id2 = item['id']
            parent2 = item['parent']
            title2 = item['title']
            print(title2)

            qaList = extract_questions_answers(content2)
            for qa in qaList:
                questions.append(
                    formatContent(title, title2, qa['question'], qa['answer'])
                )


    else:
        qaList = extract_questions_answers(content)
        for qa in qaList:
            questions.append(formatContent(None, title, qa['question'], qa['answer']))

print(questions)

with open("questions.jsonl", "w", encoding="utf-8") as f:
    for q in questions:
        f.write(json.dumps(q, ensure_ascii=False) + "\n")