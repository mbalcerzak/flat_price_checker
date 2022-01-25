import requests
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime


def today_str():
    return datetime.today().strftime('%Y-%m-%d')


def get_ad_id(page_address):
    return f"{page_address.split('/')[-1]}"


def get_price(soup) -> int:
    try:
        results = soup.find('div', class_="vip-title clearfix")
        price = results.find('span', class_='amount')
        return int(re.sub("[^\d\.,]", "", price.text))
    except (AttributeError, ValueError):
        return 0


def get_description(soup) -> str:
    try:
        results = soup.find(id="wrapper")
        description = results.find('span', class_='pre')
        description = description.text.replace('\"', '\'').replace('\\', '')
    except AttributeError:
        description = 'NA'

    return description


def get_photos(soup):
    gallery = soup.find(id="vip-gallery-data")

    if gallery is None:
        return {"photos_links": ['No photos']}

    pattern = re.compile('\{.*\}')
    json_obj = json.loads(re.findall(pattern, str(gallery))[0])

    return json_obj['large']


def get_add_title(soup) -> str:
    results = soup.find('div', class_="vip-title clearfix")
    title = results.find('span', class_='myAdTitle').text.replace('\'', '')

    return title


def extract_num_rooms(text: str) -> int:
    if "Kawalerka" in text:
        return 1
    num_rooms = int(re.sub("[^\d]", "", text))

    return num_rooms if num_rooms > 0 else 1


def change_date_str(text: str) -> str:
    dd,mm,yyyy = text.split('/')
    return f"{yyyy}-{mm}-{dd}"


def get_attributes(soup) -> dict:
    results = soup.find(id="wrapper")
    attributes = results.find('ul', class_='selMenu')
    attributes_all = attributes.find_all('div', class_='attribute')

    attr_dict = {}

    for elem in attributes_all:

        attr_name = (elem.find('span', class_='name')).text
        attr_val = (elem.find('span', class_='value')).text

        if attr_name not in attr_dict:
            if attr_name in ['Liczba pokoi', 'Liczba łazienek']:
                attr_val = extract_num_rooms(attr_val)
            if attr_name == 'Data dodania':
                attr_val = change_date_str(attr_val)
            attr_dict[attr_name] = attr_val

    return attr_dict


keys_dict = {
    'Data dodania': 'date_posted',
    'Lokalizacja': 'location',
    'Na sprzedaż przez': 'seller',
    'Rodzaj nieruchomości': 'property_type',
    'Liczba pokoi': 'num_rooms',
    'Liczba łazienek': 'num_bathrooms',
    'Wielkość (m2)': 'flat_area',
    'Parking': 'parking'}


def get_flat_info(page_address):
    page = requests.get(page_address)
    soup = BeautifulSoup(page.content, 'html.parser')

    ad_id = get_ad_id(page_address)
    price = get_price(soup)
    title = get_add_title(soup)
    today = today_str()
    description = get_description(soup)
    photos_links = get_photos(soup)

    flat = {
        'ad_id': ad_id,
        'title': title,
        'date_posted': 'NA',
        'date_scraped': today,
        'location': 'NA',
        'price': price,
        'seller': 'NA',
        'property_type': 'NA',
        'num_rooms': 0,
        'num_bathrooms': 1,
        'flat_area': 0,
        'parking': 'Brak',
        'description': description,
        'photos_links': photos_links,
        'page_address': page_address
        }


    attributes = get_attributes(soup)

    for key, value in attributes.items():
        if key in keys_dict:
            key = keys_dict[key]
            flat[key] = value

    return flat


if __name__ == "__main__":
    link = "https://www.gumtree.pl/a-mieszkania-i-domy-sprzedam-i-kupie/zoliborz/sprzedam-dwupokojowe-zoliborz/1004956732620910480854909"
    print(get_flat_info(link))