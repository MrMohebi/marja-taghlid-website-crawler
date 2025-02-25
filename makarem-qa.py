import threading
import requests
from bs4 import BeautifulSoup

FILE_NAME = "files/makarem-qa.yml"
URL = "https://makarem.ir/ahkam/fa/home/index?page={}"
LAST_PAGE = 1258

cookies = {
    'makarem_token': 'blah-blah-blah',
    '__RequestVerificationToken_L2Foa2Ft0': 'blah-blah-blah',
    'ASP.NET_SessionId': 'blah-blah-blah',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
}


# for i in range(1, LAST_PAGE):
for i in range(913, LAST_PAGE):
    response = requests.get(URL.format(i), cookies=cookies, headers=headers)
    if response.status_code != 200:
        print("till page ==> ", i)
        exit(1)
    print("page ==> ", i)
    s = BeautifulSoup(response.text, 'html.parser')
    articles = s.find_all('article')
    for article in articles:
        brif = article.find('header').find('h3').find('a').text
        question = article.find('header').find('h2').find('a').text
        res = article.find('p').text
        cat = article.find( class_='cats').text
        with open(FILE_NAME, 'a') as file:
            file.write(f"- question: '{question}'" + '\n')
            file.write(f"  response: '{res}'" + '\n')
            file.write(f"  brif: '{brif}'" + '\n')
            file.write(f"  category: '{cat}'" + '\n')
