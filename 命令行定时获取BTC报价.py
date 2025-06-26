import requests
import time

def okx_get_price():
    symbol = "BTC-USDT" # 可以是ETH-USDT SOL-USDT
    url = "https://www.okx.com/api/v5/market/ticker" # okx
    try:
        response = requests.get(url, params={"instId": symbol})
        response.raise_for_status()
        data = response.json()
        last_price = float(data["data"][0]["last"])
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{ts}] {symbol} ：{last_price}")
    except Exception as e:
        print("获取失败：", e)

# 循环轮询
while True:
    okx_get_price()
    time.sleep(5)
