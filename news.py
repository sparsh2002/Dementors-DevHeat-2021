import requests
import streamlit as st


STOCK_NAME = ''

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
SYMBOL_ENDPOINT = "https://api.iextrading.com/1.0/ref-data/symbols#"

STOCK_API_KEY = "E4FRAX6OLKKJ2WJV"
NEWS_API_KEY = "18887424b625474d9d4ff26f0f133e1a"
TWILIO_SID = "ACb28949638a23ee329a3f81c746fd427f"
TWILIO_AUTH_TOKEN = "743fd998dbe5404d89ad74b9e12cb242"

def newspage():
    symbol_response = requests.get(SYMBOL_ENDPOINT)
    symbol_json = symbol_response.json()
    symbol_list = [''] + [x['name'] for x in symbol_json]
    symbol_tuple = tuple(symbol_list)
    COMPANY_NAME = st.selectbox('Select Stock Name',(symbol_tuple))

    company_json = symbol_response.json()
    for x in company_json:
        if x['name'] == COMPANY_NAME:
            STOCK_NAME = x['symbol']
            break

    def display():
        stock_params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": STOCK_NAME,
            "apikey": STOCK_API_KEY,
        }

        response = requests.get(STOCK_ENDPOINT, params=stock_params)
        # print(response.json())
        data = response.json()["Time Series (Daily)"]
        data_list = [value for (key, value) in data.items()]
        yesterday_data = data_list[0]
        yesterday_closing_price = yesterday_data["4. close"]
        # print(yesterday_closing_price)

        day_before_yesterday_data = data_list[1]
        day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
        # print(day_before_yesterday_closing_price)

       
        difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
        up_down = None
        if difference > 0:
            up_down = "🔺"
        else:
            up_down = "🔻"

        
        diff_percent = round((difference / float(yesterday_closing_price)) * 100)
        print(diff_percent)

        news_params = {
            "apiKey": NEWS_API_KEY,
            "qInTitle": COMPANY_NAME,
        }

        news_response = requests.get(NEWS_ENDPOINT, params=news_params)
        articles = news_response.json()["articles"]

        st.write(f"{STOCK_NAME}: {up_down}{diff_percent}")
        for x in articles:
                    st.title(x['title'])
                    st.subheader(x['description'])
                    st.caption(f"Source: {x['source']['name']}")
                    st.write(f"For full article visit [link]({x['url']})")

        return

    if st.button(label='check'):
        display()