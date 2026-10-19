import streamlit as st
import yfinance as yf
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

# 1. ڈیش بورڈ کا پیج سیٹ اپ
st.set_page_config(page_title="AI Trading Signal Board", page_icon="🤖", layout="centered")

st.title("🤖 اے آئی ٹریڈنگ سگنل بورڈ")
st.write("یہ بورڈ ریئل ٹائم مارکیٹ ڈیٹا اور تکنیکی انڈیکیٹرز کی بنیاد پر ٹریڈنگ سگنل جنریٹ کرتا ہے۔")

st.markdown("---")

# 2. کرنسی یا اثاثہ منتخب کریں
asset = st.selectbox(
    "کرنسی پیئر (Currency Pair) منتخب کریں:",
    ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "BTC-USD"]
)

timeframe = st.selectbox("ٹائم فریم (Timeframe):", ["1m", "5m", "15m", "1h"])

# 3. بٹن دبانے پر مارکیٹ کا تجزیہ
if st.button("📊 مارکیٹ کا تجزیہ کریں (Analyze)"):
    st.info("مارکیٹ کا لائیو ڈیٹا ڈاؤن لوڈ ہو رہا ہے...")
    data = yf.download(tickers=asset, period="1d", interval=timeframe)
    if 'Close' in data and len(data) > 20:
        close_data = data['Close'].iloc[:, 0] if hasattr(data['Close'], 'iloc') and len(data['Close'].shape) > 1 else data['Close']
        
        rsi_class = RSIIndicator(close=close_data, window=14)
        data['RSI'] = rsi_class.rsi()
        
        ema_fast = EMAIndicator(close=close_data, window=9)
        data['EMA_9'] = ema_fast.ema_indicator()
        
        last_rsi = round(data['RSI'].iloc[-1], 2)
        last_close = round(data['Close'].iloc[-1], 4)
        
        st.markdown("---")
        st.subheader("📈 تجزیہ کا نتیجہ:")
        st.write(f"**موجودہ قیمت (Price):** {last_close}")
        st.write(f"**موجودہ RSI ویلیو:** {last_rsi}")
        
        st.markdown("### 🎯 اے آئی سگنل:")
        if last_rsi < 35:
            st.success("🟢 **CALL / BUY سگنل**: مارکیٹ اوور سولڈ (Over-Sold) زون میں ہے، اوپر جانے کے امکانات ہیں۔")
        elif last_rsi > 65:
            st.error("🔴 **PUT / SELL سگنل**: مارکیٹ اوور باؤٹ (Over-Bought) زون میں ہے، نیچے آنے کے امکانات ہیں۔")
        else:
            st.warning("⚪ **WAIT (انتظار کریں)**: مارکیٹ درمیان میں ہے، فی الحال کوئی واضح سگنل نہیں ہے۔")
    else:
        st.error("ڈیٹا حاصل نہیں ہو سکا۔")
      
