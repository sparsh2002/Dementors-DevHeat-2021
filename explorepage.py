import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
from keras.models import load_model
import streamlit as st
import time

from datetime import date
from datetime import timedelta


def show_explore_page():
    st.subheader('Explore Page')
    start = '2010-01-01'
    today = date.today()
    end = today - timedelta(days = 1)

    user_input = st.text_input('Enter Stock Ticket' , 'AAPL')
    df = data.DataReader(user_input,'yahoo',start, end)

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

    st.subheader('Prediction Data based on last 100 days')
    fig2 = plt.figure(figsize=(12,6))
    plt.plot(y_test ,'b' , label = 'Original Price')
    plt.plot(y_predicted ,'r' , label = 'Predicted Price')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    st.pyplot(fig2)
    # st.write(type(y_predicted)) 
    # st.write(y_predicted.shape)
    st.write('Expected closing price tommorow')
    st.write('Predicted Price: ' , y_predicted[y_predicted.shape[0]-1][0])
    st.write('Current Price : ', y_test[y_test.shape[0]-1])


    # tables = []
    # for i in range(0, 3):
    #     url = 'https://www.marketwatch.com/tools/stockresearch/screener/results.asp?TradesShareEnable=True&TradesShareMin=10&TradesShareMax=50&PriceDirEnable=False&PriceDir=Up&LastYearEnable=False&TradeVolEnable=False&BlockEnable=False&PERatioEnable=False&MktCapEnable=False&MovAvgEnable=False&MovAvgType=Outperform&MovAvgTime=FiftyDay&MktIdxEnable=False&MktIdxType=Outperform&Exchange=All&IndustryEnable=False&Industry=Insurance&Symbol=True&CompanyName=True&Price=True&Change=True&ChangePct=True&Volume=True&LastTradeTime=True&FiftyTwoWeekHigh=False&FiftyTwoWeekLow=True&PERatio=True&MarketCap=True&MoreInfo=False&SortyBy=Symbol&SortDirection=Ascending&ResultsPerPage=OneHundred&PagingIndex={0}'.format(i*100)
    #     print('Processing Index {0}'.format(i*100))

    #     try:
    #         df1 = pd.read_html(url)[0]
    #         tables.append(df1)
    #         time.sleep(1)
    #     except Exception as e:
    #         print(e)
    #         continue

    # results = pd.concat(tables, axis=0)
    # results.to_excel('Screen Results.xlsx', index=False)    
    


    