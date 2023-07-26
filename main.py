import json
import datetime
import requests

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Is-Ajax-Request": "X-Is-Ajax-Request",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"

}

spisok = []


def get_data():
    start_time=datetime.datetime.now()

    url = 'https://roscarservis.ru/catalog/legkovye/?sort%5Bprice%5D=asc&form_id=catalog_filter_form&filter_mode=params&filter_type=tires&diskType=1&arCatalogFilter_458_1500340406=Y&set_filter=Y&PAGEN_1=1'
    r = requests.get(url=url, headers=headers)

    # with open("index.html", 'w', encoding='utf-8') as file:
    #     file.write(req.text)
    # print(req.json())
    # with open("r.json", 'w') as file:
    #     json.dump(req.json(), file, indent=4, ensure_ascii=False )

    pages_count = r.json()["pageCount"]
    for page in range(1, pages_count+1):
        url = f'https://roscarservis.ru/catalog/legkovye/?sort%5Bprice%5D=asc&form_id=catalog_filter_form&filter_mode=params&filter_type=tires&diskType=1&arCatalogFilter_458_1500340406=Y&set_filter=Y&PAGEN_1={page}'
        r = requests.get(url=url, headers=headers)
        data = r.json()
        items = data['items']
        possible_stores=["discountStores", "fortochkiStores", "commonStores"]

        for item in items:
            total_amount=0
            item_name = item['name']
            item_price = item['price']
            item_img = 'https://roscarservis.ru/' + item['imgSrc']
            item_url = 'https://roscarservis.ru/' + item['url']
            stores=[]
            for ps in possible_stores:
                if ps in item:
                    if item[ps] is None or len(item[ps]) <1 :
                        continue
                    else:
                        for store in item[ps]:
                            store_name=store['STORE_NAME']
                            store_price=store["PRICE"]
                            store_amount=store["AMOUNT"]
                            total_amount+=int(store["AMOUNT"])

                            stores.append({
                                "store_name" : store_name,
                                "store_price": store_price,
                                "store_amount": store_amount

                            })










            spisok.append({
                "Name": item_name,
                "Price": item_price,
                "IMG": item_img,
                "URL": item_url,
                "Stores": stores,
                "total_amount": total_amount

    })
        print(f'[INFO] ОБРАБОТАНА СТРАНИЦА {page} ИЗ {pages_count}')
    cur_time = datetime.datetime.now().strftime("%D_%M_%Y_%H")

    with open(f"spisok.json", 'w', encoding='utf-8') as file:
        json.dump(spisok, file, indent=4, ensure_ascii=False)
    diff_time=datetime.datetime.now()-start_time
    print(diff_time)


def main():
    get_data()


if __name__ == "__main__":
    main()
