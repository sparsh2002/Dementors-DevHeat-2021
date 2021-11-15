import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
from keras.models import load_model
import streamlit as st
import requests
from datetime import date
from datetime import timedelta

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

def show_predict_page():
    start = '2010-01-01'
    today = date.today()
    end = today - timedelta(days = 1)

    st.title('Stock Trend Prediction')

    symbol_response = requests.get(SYMBOL_ENDPOINT)
    symbol_json = symbol_response.json()
    symbol_list = [''] + [x['name'] for x in symbol_json]
    symbol_tuple = tuple(symbol_list)
    COMPANY_NAME = st.selectbox('Select Stock name:',(symbol_tuple))

    company_json = symbol_response.json()
    for x in company_json:
        if x['name'] == COMPANY_NAME:
            STOCK_NAME = x['symbol']
            break

    # user_input = st.text_input('Enter Stock Ticket' , 'AAPL')
    user_input = STOCK_NAME
    df = data.DataReader(user_input,'yahoo',start, end)

    #Describing Data
    st.subheader('Data from 2010 - to present')
    st.write(df.describe())


    # visualization
    st.subheader('Closing Price Vs Time Chart')
    fig = plt.figure(figsize = (12,6))
    plt.plot(df.Close)
    st.pyplot(fig)


    st.subheader('Closing Price Vs Time Chart with 100MA')
    ma100 = df.Close.rolling(100).mean()
    fig = plt.figure(figsize = (12,6))
    plt.plot(ma100)
    plt.plot(df.Close)
    st.pyplot(fig)

    st.subheader('Closing Price Vs Time Chart with 100MA and 200MA')
    ma100 = df.Close.rolling(100).mean()
    ma200 = df.Close.rolling(200).mean()
    fig = plt.figure(figsize = (12,6))
    plt.plot(ma100 ,'r')
    plt.plot(ma200 , 'g')
    plt.plot(df.Close, 'b')
    st.pyplot(fig)


    # Splitting data into x_train and y_train

    data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
    data_testing = pd.DataFrame(df['Close'][int(len(df)*.70):int(len(df))])

    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range = (0,1))

    data_training_array = scaler.fit_transform(data_training)



    # Load my model
    model = load_model('keras_model.h5')

    # Testing Part

    past_100_days = data_training.tail(100)
    final_df = past_100_days.append(data_testing,ignore_index = True)
    input_data = scaler.fit_transform(final_df)

    x_test = []
    y_test = []

    for i in range(100, input_data.shape[0]):
        x_test.append(input_data[i-100:i])
        y_test.append(input_data[i,0])
        
    x_test,y_test = np.array(x_test),  np.array(y_test)

    y_predicted = model.predict(x_test)
    scaler = scaler.scale_
    scale_factor = 1/scaler[0]
    y_predicted = y_predicted*scale_factor
    y_test = y_test*scale_factor


    # Final Graph

    # st.subheader('Prediction vs Original')
    # fig2 = plt.figure(figsize=(12,6))
    # plt.plot(y_test ,'b' , label = 'Original Price')
    # plt.plot(y_predicted ,'r' , label = 'Predicted Price')
    # plt.xlabel('Time')
    # plt.ylabel('Price')
    # plt.legend()
    # st.pyplot(fig2)