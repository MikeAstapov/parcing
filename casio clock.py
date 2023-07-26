from bs4 import BeautifulSoup

clock_list = []


def get_all_pages():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

    }

    r = requests.get(url="https://shop.casio.ru/catalog/", headers=headers)

    if not os.path.exists("data2"):
        os.mkdir('data2')

    with open("data2/page.html", 'w', encoding='utf-8') as file:
        file.write(r.text)

    with open("data2/page.html", encoding='utf-8') as f:
        src = f.read()

    soup = BeautifulSoup(src, 'lxml')
    pages_count = int(soup.find('div', class_='bx-pagination-container').find_all('a')[-2].text)

    for i in range(1,pages_count +1):
        url= f"https://shop.casio.ru/catalog/?PAGEN_1={i}"
        r=requests.get(url)

        with open(f'data2/page_{i}.html', 'w', encoding='utf-8') as file:
            file.write(r.text)

        sleep(2)
    return pages_count + 1


def collect_data(pages_count):
    for page in range(1, 2):
        with open(f'data2/page_{page}.html') as f:
            src = f.read()

        soup = BeautifulSoup(src, 'lxml')
        items_cards = soup.find_all('a', class_='product-item')
        for item in items_cards:
            clock_url = item.get('href')
            clock_brand = item.find('p', class_='product-item__brand').text
            clock_price = item.find('p', class_='product-item__price').text
            print(f'Brand: {clock_brand},Ссылка: {clock_url}, Стоимость: {clock_price}')


def main():
    pages_count = get_all_pages()
    collect_data(pages_count=pages_count)


if __name__ == "__main__":
    main()


