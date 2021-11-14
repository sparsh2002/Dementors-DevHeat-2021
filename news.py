import requests
# from twilio.rest import Client
import streamlit as st

VIRTUAL_TWILIO_NUMBER = "+17633738499"
VERIFIED_NUMBER = "+917398816950"

STOCK_NAME = ''

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
SYMBOL_ENDPOINT = "https://api.iextrading.com/1.0/ref-data/symbols#"

STOCK_API_KEY = "E4FRAX6OLKKJ2WJV"
NEWS_API_KEY = "18887424b625474d9d4ff26f0f133e1a"
TWILIO_SID = "ACb28949638a23ee329a3f81c746fd427f"
TWILIO_AUTH_TOKEN = "743fd998dbe5404d89ad74b9e12cb242"

def newspage():
    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
    # When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
    symbol_response = requests.get(SYMBOL_ENDPOINT)
    symbol_json = symbol_response.json()
    symbol_list = [''] + [x['name'] for x in symbol_json]
    symbol_tuple = tuple(symbol_list)
    COMPANY_NAME = st.selectbox('Select HomeTeamName name:',(symbol_tuple))

    company_json = symbol_response.json()
    for x in company_json:
        if x['name'] == COMPANY_NAME:
            STOCK_NAME = x['symbol']
            break

    #Get yesterday's closing stock price
    def display():
        stock_params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": STOCK_NAME,
            "apikey": STOCK_API_KEY,
        }

        response = requests.get(STOCK_ENDPOINT, params=stock_params)
        print(response.json())
        data = response.json()["Time Series (Daily)"]
        data_list = [value for (key, value) in data.items()]
        yesterday_data = data_list[0]
        yesterday_closing_price = yesterday_data["4. close"]
        print(yesterday_closing_price)

        #Get the day before yesterday's closing stock price
        day_before_yesterday_data = data_list[1]
        day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
        print(day_before_yesterday_closing_price)

        #Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
        difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
        up_down = None
        if difference > 0:
            up_down = "🔺"
        else:
            up_down = "🔻"

        #Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
        diff_percent = round((difference / float(yesterday_closing_price)) * 100)
        print(diff_percent)


            ## STEP 2: Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

        #Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
        #If difference percentage is greater than 5 then print("Get News").
        # if abs(diff_percent) > 2:
        news_params = {
            "apiKey": NEWS_API_KEY,
            "qInTitle": COMPANY_NAME,
        }

        news_response = requests.get(NEWS_ENDPOINT, params=news_params)
        articles = news_response.json()["articles"]

                #Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
                # three_articles = articles[0:]

                ## STEP 3: Use Twilio to send a seperate message with each article's title and description to your phone number.

                #Create a new list of the first 3 article's headline and description using list comprehension.
                # formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in articles]
        st.write(f"{STOCK_NAME}: {up_down}{diff_percent}")
        for x in articles:
                    st.title(x['title'])
                    st.subheader(x['description'])
                    st.caption(f"Source: {x['source']['name']}")
                    st.write(f"For full article visit [link]({x['url']})")

                #Send each article as a separate message via Twilio.
                # client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

                #TODO 8. - Send each article as a separate message via Twilio.
                # for article in formatted_articles:
                #     message = client.messages.create(
                #         body=article,
                #         from_=VIRTUAL_TWILIO_NUMBER,
                #         to=VERIFIED_NUMBER
                #     )
        return

    if st.button(label='check'):
        display()