import random
import streamlit as st
from itertools import cycle
import altair as alt
import random

from process_ad_data import get_flat_info
from get_stats_waw import get_price_size_category, get_random_flat_links, get_flat_price_history


st.sidebar.warning("Not an investment advice. I am just a project for a programming portfolio. Don't listen to me.")
random_flat_link = random.choice(get_random_flat_links())

if st.sidebar.button("""Random flat"""):
     chosen_flat_link = random_flat_link
else:
     chosen_flat_link = ""

link_label = """Paste a link of a flat from Gumtree (Warsaw, Poland only so far)"""
chosen_flat_link = st.sidebar.text_input(label=link_label, value=chosen_flat_link, max_chars=250)


if len(chosen_flat_link) == 0:  
    st.title("Am I overpaying for that flat? Probably.")
    st.image("./warsaw.jpeg")
    st.markdown("[Photo by Victor Malyushev](https://unsplash.com/@malyushev?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)")
else:
    flat_info = get_flat_info(chosen_flat_link)

    if "Warszawa" not in flat_info['location']:
        st.error("!! So far the app works only for flats in Warsaw, Poland. Please enter a valid link")
    else: 
        st.image(flat_info['photos_links'][0])
        st.markdown(f"""
        # {flat_info['title']}

        Rooms: **{flat_info['num_rooms']}**  
        Bathooms: **{flat_info['num_bathrooms']}**   
        Flat size: **{flat_info['flat_area']}** m<sup>2</sup>  
        
        """, unsafe_allow_html=True)

        category_price = get_price_size_category(flat_info)
        flats_price_per_m = round(flat_info['price'] / int(flat_info['flat_area']))

        ### TODO change
        pred_price = random.choice([10_000, 20_000, 15_000])
        pred_diff = round((flats_price_per_m - pred_price)/pred_price * 100)
        flats_price_per_m_warsaw = 13_000
        ###

        price_diff_prc = round((flats_price_per_m - category_price)/category_price * 100)
        price_diff = flats_price_per_m - category_price

        flat_location = flat_info['location'].split(',')[0]

        st.subheader(f"Average prices in {flat_location} compared to previous month")
        col1, col2 = st.columns(2)
        col1.metric("Avg. price for that district", f"{category_price} PLN", "+5%")
        col2.metric("Avg, price for Warsaw", f"{flats_price_per_m_warsaw} PLN", "-7%")

        st.subheader(f"Price of this apartment vs. what the algoritm predicted")

        if pred_price < flats_price_per_m:
            price_diff_msg = st.markdown("""<span style="color:red">Seems like the advertised price is higher that the predicted one... Check out the price history, maybe the owner is willing to negotiate. </span>""", unsafe_allow_html=True)
        else:
            price_diff_msg = st.markdown("""<span style="color:green">Seems like that flat is worth more than it's advertised for :) </span>""", unsafe_allow_html=True)

        col3, col4 = st.columns(2)
        col3.metric("Price of this flat (m2)", f"{flats_price_per_m} PLN", "-7%")
        col4.metric("Predicted price", f"{pred_price} PLN", f"{pred_diff}%")

        with st.expander("PRICE HISTORY", expanded=False):
            # TODO: price history for that district of Warsaw and Warsaw in total too
            try:
                price_history = get_flat_price_history(flat_info['ad_id'])
                st.table(price_history)
                st.line_chart(price_history)
            except KeyError:
                st.write("No record of previous prices")   

        with st.expander("Description", expanded=False):
            # TODO: add
            pass

        with st.expander("See the photos of the apartment", expanded=False):
            filteredImages = flat_info['photos_links']
            cols = cycle(st.columns(3))
            for idx, filteredImage in enumerate(filteredImages):
                next(cols).image(filteredImage, use_column_width=True)

        st.markdown(f""" Go to the [gumtree advertisement]({chosen_flat_link})""")
