import requests
import jpg2pdf



def get_data():
    headers = {
        "accept": "image / avif, image / webp, image / apng, image / svg + xml, image / *, * / *;q = 0.8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    img_list = []
    for i in range(1, 49):
        url = f'https://www.recordpower.co.uk/flip/Winter2020/files/mobile/{i}.jpg'
        req = requests.get(url=url, headers=headers)
        responce = req.content

        with open(f'{i}.jpeg', 'wb') as file:
            file.write(responce)
            img_list.append(f'{i}.jpg')

            print(f"downloaded {i} of 48")
    print("#" * 20)






# create PFD file

    with open("result.pdf", 'wb') as f:
        f.write(img2pdf.convert(img_list))

    print("PDF was created")
def main():
    get_data()

if __name__ == "__main__":
    main()