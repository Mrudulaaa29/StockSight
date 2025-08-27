import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.title("StockSight📈")

# Sidebar input for stock ticker
stock_symbol = st.sidebar.text_input("Enter Stock Ticker", value="AAPL").upper()
days = st.sidebar.slider("Days of History", min_value=1, max_value=30, value=7)

def get_stock_data(ticker, period):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    return hist

data = get_stock_data(stock_symbol, f"{days}d")

if data.empty:
    st.error("No data found for this ticker symbol.")
else:
    st.subheader(f"Stock price data for {stock_symbol} - Last {days} days")

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Candlesticks'
    ))

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        xaxis_rangeslider_visible=False,
        template='plotly_dark'
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Key Financial Indicators")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Opening Price", value=f"${data['Open'][-1]:.2f}")
    with col2:
        st.metric(label="Closing Price", value=f"${data['Close'][-1]:.2f}")
    with col3:
        st.metric(label="Volume", value=f"{int(data['Volume'][-1]):,}")

    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['MA50'] = data['Close'].rolling(window=50).mean()

    st.line_chart(data[['Close', 'MA20', 'MA50']].dropna())
