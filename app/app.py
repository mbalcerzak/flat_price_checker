import random
import streamlit as st
from itertools import cycle
import altair as alt

from process_ad_data import get_flat_info
from get_stats_waw import get_price_size_category, get_random_flat_links, get_flat_price_history

st.title("Am I overpaying for that flat? Probably.")
st.warning("Not an investment advice. I am just a project for a programming portfolio. Don't listen to me.")

random_flat_link = random.choice(get_random_flat_links())

if st.button("""Random flat"""):
     chosen_flat_link = random_flat_link
else:
     chosen_flat_link = ""

link_label = """Paste a link of a flat from Gumtree (Warsaw, Poland only so far)"""
chosen_flat_link = st.text_input(label=link_label, value=chosen_flat_link, max_chars=250)


if len(chosen_flat_link) > 0:  
    flat_info = get_flat_info(chosen_flat_link)

    st.subheader(flat_info['title'])
    st.write(f"Rooms: {flat_info['num_rooms']}, bathooms: {flat_info['num_bathrooms']}, flat size: {flat_info['flat_area']}")

    category_price = get_price_size_category(flat_info)
    flats_price_per_m = round(flat_info['price'] / int(flat_info['flat_area']))

    price_diff = round(abs(flats_price_per_m - category_price)/category_price * 100)

    if category_price < flats_price_per_m:
        price_diff_msg = "more expensive"      
    else:
        price_diff_msg = "cheaper"

    flat_location = flat_info['location'].split(',')[0]

    st.write(f"{category_price:,} PLN - Price per square metre for this size of flat that month in {flat_location}.".replace(',', ' '))
    st.write(f"{flats_price_per_m:,} PLN - The price per square metre for this apartment.")
    st.info(f"Price of square metre of this flat is {price_diff} % {price_diff_msg} than the average for this size, location and date of posting".replace(',', ' '))
    
    st.subheader("Has the price of that flat ever changed?")

    try:
        price_history = get_flat_price_history(flat_info['ad_id'])
        st.table(price_history)
        st.line_chart(price_history)
    except KeyError:
        st.write("No record of previous prices")
    
    filteredImages = flat_info['photos_links']

    cols = cycle(st.columns(3))
    for idx, filteredImage in enumerate(filteredImages):
        next(cols).image(filteredImage, use_column_width=True)