import requests
import json
headers={
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "Accept": "*/*"
}
def get_data_file(headers):
    url="https://www.landingfolio.com/"
    r=requests.get(url=url, headers=headers)
    with open("index.html", 'w', encoding="utf-8") as file:
        file.write(r.text)

    page=0
    result_list=[]
    img_count=0
    while True:
        url=f'https://www.landingfolio.com/api/inspiration?page={page}&sortBy=most-popular'
        responce=requests.get(url=url,headers=headers)
        data=responce.json()

        for item in data:
            if 'screenshots' in item:
                images=item.get('images')


                for img in images:
                    img.update({"url": f"https://landingfoliocom.imgix.net/{img.get('url')}"})
                result_list.append(
                {
                    'title': item.get('title'),
                    'url': item.get('url'),
                    'images': images

                }
                )
            else:
                with open('result_list.json', 'a',encoding='utf-8') as file:
                    json.dump(result_list,file, ensure_ascii=False,indent=4)
                return f"'[INFO]' Work finished."

        print(f"[+] Proceesed {page}")
        page += 1



def download_imgs(file_path):
    pass


def main():
   get_data_file(headers=headers)


if __name__ == '__main__':
    main()