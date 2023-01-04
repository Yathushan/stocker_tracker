import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st

from PIL import Image
import urllib.request

import altair as alt

def display_img(url):
    with urllib.request.urlopen(url) as url:
        with open('temp.jpg', 'wb') as f:
            f.write(url.read())
    img = Image.open('temp.jpg')
    return img

st.header('Stock Tracker')


ticker_name = st.text_input('What stock are you interested in tracking?', 'APPL', max_chars=7)
ticket = yf.Ticker(ticker_name)

news_items = []
art_num = 0
for i in ticket.news:
    news_items.append("Article " + str(art_num))
    art_num+=1

col1, col2, col3 = st.columns(3)
with col2:
    ticker_img = ticket.info['logo_url']
    st.image(display_img(ticker_img), use_column_width='auto')

with st.expander("Detailed Description of " + str(ticker_name)):
    st.write(ticket.info['longBusinessSummary'])

met1, met2, met3 = st.columns(3)
with met1:
    if ticket.info['currentPrice']:
        st.metric("Current Price",ticket.info['currentPrice'])
with met2:
    if ticket.shares.iat[0,-1].any():
        st.metric("Number of Shares",ticket.shares.iat[0,-1])
with met3:
    if ticket.splits.any():
        st.metric("Stock Splits",ticket.splits[2])

stock_price, quarter_balance, recommendations = st.tabs(["Historic Price", "Quarterly Balance", "Analyst Recommendation"])
with stock_price:
    hist = ticket.history(period="max")
    st.line_chart(hist, y=['Close'])
with quarter_balance:
    st.dataframe(ticket.quarterly_balance_sheet, use_container_width=True)
with recommendations:
    st.dataframe(ticket.recommendations_summary, use_container_width=True)


# st.write(ticket.news)

tabs = st.tabs(news_items)
counter = 0
for i in tabs:
    with i:
        if 'thumbnail' in ticket.news[counter]:
            article_img = ticket.news[counter]['thumbnail']['resolutions'][0]['url']
        st.image(display_img(article_img), use_column_width='auto', caption=st.write(ticket.news[counter]['title']))
        st.write(ticket.news[counter]['link'])
    counter+=1