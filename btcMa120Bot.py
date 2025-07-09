import time
import requests
import logging
from binance.client import Client
from config import BOT_TOKEN, CHAT_ID

# Binance行情客户端
client = Client()

# 日志配置
log_filename = time.strftime("./log/btc_ma_monitor_%Y%m%d.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# 发送Telegram消息
def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    resp = requests.post(url, json=data)
    logging.info("Telegram通知发送结果: %s", resp.text)

# 获取均线
def get_ma(symbol, interval, period):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=period)
    closes = [float(k[4]) for k in klines]
    return sum(closes) / len(closes)

# 获取最新价格
def get_latest_price(symbol="BTCUSDT"):
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker["price"])

# 记录上一次价格
prev_price = None

while True:
    try:
        # 最新价格
        price = get_latest_price()

        # 均线
        ma120 = get_ma("BTCUSDT", "1d", 120)
        ma30 = get_ma("BTCUSDT", "1d", 30)
        ma40 = get_ma("BTCUSDT", "1d", 40)

        log_msg = f"当前价格: {price:.2f} | MA30: {ma30:.2f} | MA40: {ma40:.2f} | MA120: {ma120:.2f}"
        logging.info(log_msg)

        # 只在不是第一次循环时判断
        if prev_price is not None:
            messages = []

            if prev_price < ma30 and price >= ma30:
                messages.append(f"⚡上穿 MA30 ({ma30:.2f})")
            if prev_price > ma30 and price <= ma30:
                messages.append(f"⚠️下穿 MA30 ({ma30:.2f})")

            if prev_price < ma40 and price >= ma40:
                messages.append(f"⚡上穿 MA40 ({ma40:.2f})")
            if prev_price > ma40 and price <= ma40:
                messages.append(f"⚠️下穿 MA40 ({ma40:.2f})")

            if prev_price < ma120 and price >= ma120:
                messages.append(f"⚡上穿 MA120 ({ma120:.2f})")
            if prev_price > ma120 and price <= ma120:
                messages.append(f"⚠️下穿 MA120 ({ma120:.2f})")

            if messages:
                ts = time.strftime("%Y-%m-%d %H:%M:%S")
                text = f"📊 {ts}\nBTC当前价格: {price:.2f}\n" + "\n".join(messages)
                logging.info("触发通知: %s", text)
                send_telegram(text)

        prev_price = price

    except Exception as e:
        logging.exception("出现错误:")

    time.sleep(60)
