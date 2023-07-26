import json

import requests
from bs4 import BeautifulSoup

fest_list_result = []
fests_urls_list = []

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

for i in range(0, 192, 24):
    url = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=&to_date=&maxprice=500&o={i}&bannertitle=July'
    #
    req = requests.get(url=url, headers=headers)
    json_data = json.loads(req.text)

    html_response = json_data['html']

    with open(f'data/index_{i}.html', 'w', encoding='utf-8') as file:
        file.write(html_response)

    with open(f'data/index_{i}.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    cards = soup.find_all('a', class_='card-details-link')
    count = 0
    for item in cards:
        fest_url = item.get('href')
        fests_urls_list.append('https://www.skiddle.com/' + fest_url)

for url in fests_urls_list:
    count += 1
    print(count)
    print(url)
    req = requests.get(url=url, headers=headers)
    try:
        soup = BeautifulSoup(req.text, 'lxml')
        fest_info_block = soup.find('div', class_='top-info-cont')
        fest_name = fest_info_block.find('h1').text.strip()
        fest_date = fest_info_block.find('h3').text.strip()
        fest_location = "https://www.skiddle.com/" + fest_info_block.find('a').get('href')

        req = requests.get(url=fest_location, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        contact_details = soup.find('h2', string='Venue contact details and info').find_next()
        items = [item.text for item in contact_details.find_all('p')]
        contact_details_dict = {}
        for contact_details in items:
            contact_details_list = contact_details.split(':')

            if len(contact_details_list) == 3:
                contact_details_dict[contact_details_list[0].strip()] = contact_details_list[1].strip() + ":" \
                                                                        + contact_details_list[2].strip()
            else:
                contact_details_dict[contact_details_list[0]] = contact_details_list[1].strip()
            print(contact_details)

        fest_list_result.append({
            "Fest name": fest_name,
            "Fest Date": fest_date,
            "Contacts": contact_details_dict
        })
    except Exception as ex:
        print(ex)
        print("damn...card fest empty")

with open('fest_list_result.json', 'a', encoding='utf-8') as file:
    json.dump(fest_list_result, file, indent=4, ensure_ascii=False)
