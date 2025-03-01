import requests
import json
from bs4 import BeautifulSoup
from itertools import zip_longest
import html

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


def extract_questions_answers(html_text):
    if not html_text:
        return []  # Return an empty list if no text is provided

    decoded_html = html.unescape(html_text)
    soup = BeautifulSoup(decoded_html, "html.parser")

    elements = soup.find_all(class_=["matn", "answer"])

    qa_pairs = []
    current_question = None
    current_answers = []

    for elem in elements:
        text = elem.get_text(strip=True)
        if text:
            if 'matn' in elem.get('class', []):  # If it's a question
                # If there was a previous question with answers, save it
                if current_question and current_answers:
                    qa_pairs.append({"question": current_question, "answer": " | ".join(current_answers)})

                # Start a new question
                current_question = text
                current_answers = []  # Reset answers list

            elif 'answer' in elem.get('class', []):  # If it's an answer
                if current_question:  # Only collect answers if there's an active question
                    current_answers.append(text)

    # Add the last valid question-answer pair if it has answers
    if current_question and current_answers:
        qa_pairs.append({"question": current_question, "answer": " | ".join(current_answers)})

    return qa_pairs

# Note: parentTitle could be None, then title will be the prime
def formatContent(parentTitle, title, question, answer):
    return {'question': question, 'answer': answer , 'category' : parentTitle + " " + title if parentTitle is not None else title}


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

            qaList = extract_questions_answers(content2  )
            for qa in qaList:
                questions.append(
                    formatContent(title, title2, qa['question'], qa['answer'])
                )


    else:
        qaList = extract_questions_answers(content )
        for qa in qaList:
            questions.append(formatContent(None, title, qa['question'], qa['answer']))


with open("files/questions.jsonl", "w", encoding="utf-8") as f:
    for q in questions:
        f.write(json.dumps(q, ensure_ascii=False) + "\n")