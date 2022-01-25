import json
from typing import Dict
import requests
from datetime import datetime
import pandas as pd


def get_link_price_history():
    return "https://raw.githubusercontent.com/mbalcerzak/warsaw_flats_api/raspberry-updates/json_dir/latest_changes.json"


def get_link_random_links():
    return "https://raw.githubusercontent.com/mbalcerzak/warsaw_flats_api/raspberry-updates/json_dir/random_links.json"


def get_json(link: str) -> int:
    response = json.loads(requests.get(link).text)
    return response


def assign_area_category(flat_area: str) -> str:
    flat_area = int(flat_area)

    if flat_area < 20:
        category = '20_or_less'
    elif flat_area < 30:
        category = '20_30' 
    elif flat_area < 40:
        category = '30_40' 
    elif flat_area < 50:
        category = '40_50' 
    elif flat_area < 60:
        category = '50_60' 
    elif flat_area <=70:
        category = '60_70' 
    elif flat_area < 80:
        category = '70_80' 
    else:
        category = '80_or_more'
    return category


def get_month_num(date: str = None) -> str:
    str_date = datetime.strptime(date, '%Y-%m-%d')
    return str_date.strftime("%Y-%m")


def get_price_size_category(flat: Dict = None) -> str:
    link_stat_prices = "https://raw.githubusercontent.com/mbalcerzak/warsaw_flats_api/raspberry-updates/json_dir/flats.json"

    data = get_json(link_stat_prices)
    price_m_loc_area_cat = data['price_m_loc_area_cat']

    flat_location = flat['location'].split(', ')[0]
    flat_area_category = assign_area_category(flat['flat_area'])
    flat_month_num = get_month_num(flat['date_scraped'])

    # print(flat_area_category, flat_month_num, flat_location)
    for elem in price_m_loc_area_cat:
        if elem['location'] == flat_location:
            if elem['area_category'] == flat_area_category:
                if elem['month_num'] == flat_month_num:
                    return elem['avg_price_per_m']


def get_price_history() -> Dict:
    link_price_history = get_link_price_history()
    data = get_json(link_price_history)
    return data


def get_flat_price_history(ad_id: str) -> pd.DataFrame:
    data = get_price_history()
    plot_data = pd.DataFrame.from_dict(data[ad_id], orient='index', columns=['Price'])
    print(plot_data)
    return plot_data


def get_random_flat_links() -> list:
    link = get_link_random_links()
    data = get_json(link)
    return list(data)


if __name__ == "__main__":

    flat = {"location": "Ursus",
            "flat_area": 87,
            "month_num": "2021-01",
            "avg_price_per_m": 11601,
            "num_flats": 2,
            "month": "January2021",
            "date": '2022-01-01'
            }

    # print(get_price_size_category(flat))

    # print(get_flat_price_history("10010275453741012520720209"))