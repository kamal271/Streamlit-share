import yfinance as yf
import streamlit as st
import datetime
import pandas as pd

yf.pdr_override()

st.write("""
## Web app for financial data analysis
""")

st.sidebar.header('Input Parameters')

tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].values


today = datetime.date.today()
def user_input_features():
    ticker = st.sidebar.selectbox('Select a ticker', tickers)
    start_date = st.sidebar.date_input('Start', pd.to_datetime('2021-01-01'))
    end_date = st.sidebar.date_input('End', pd.to_datetime('today'))
    return ticker, start_date, end_date

symbol, start, end = user_input_features()


start = pd.to_datetime(start)
end = pd.to_datetime(end)

nb_days = st.sidebar.slider('Days (moving average)', 0, 50, value=20)

# Read data
ticker = yf.Ticker(symbol)
data = yf.download(symbol,start,end)
name_company = ticker.info['longName']
details_company = ticker.info['longBusinessSummary']

infos = pd.DataFrame.from_dict(ticker.info, orient='index', columns=['Information'])
infos = infos.loc[['longName', 'sector', 'fullTimeEmployees', 'city', 'country', 'website', 'ebitda', 'totalRevenue']].astype(str)

st.subheader(name_company)

st.dataframe(infos)

st.markdown("""<style>.big-font {
    font-size:12px !important;
}
</style>
""", unsafe_allow_html=True)


st.markdown('<p class="big-font">' + details_company  + '!!</p>', unsafe_allow_html=True)

st.subheader("Adjusted Close Price")
# Adjusted Close Price

st.line_chart(data['Adj Close'])

# # ## SMA and EMA

st.subheader("Moving averages")

# #Simple Moving Average
data['SMA'] = data['Adj Close'].rolling(nb_days).mean()

# # Exponential Moving Average
data['EMA'] = data['Adj Close'].ewm(nb_days).mean()


st.line_chart(data[['Adj Close','SMA','EMA']])


